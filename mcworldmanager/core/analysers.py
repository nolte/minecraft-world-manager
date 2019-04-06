import logging
import time

import nbt.nbt as nbt
from nbt.region import (  # RegionFileFormatError,
    STATUS_CHUNK_OVERLAPPING,
    ChunkDataError,
    ChunkHeaderError,
    InconceivedChunk,
    MalformedFileError,
    NoRegionHeader,
    RegionFile,
    RegionHeaderError,
)

from mcworldmanager.core import models, util

logger = logging.getLogger(__name__)


class MCDataFileAnalyser(object):
    def analyse(self, data_file):
        try:
            if data_file.filename == "idcounts.dat":
                if util.is_gz_file(data_file.path):
                    dataFile = nbt.NBTFile(filename=data_file.path)
                else:
                    f = open(data_file.path)
                    dataFile = nbt.NBTFile(buffer=f)
            else:
                dataFile = nbt.NBTFile(filename=data_file.path)

            assert dataFile

        except MalformedFileError:
            data_file.scan_results.append(models.DATA_MALFORMED_FILE_ERROR)
        except IOError:
            data_file.scan_results.append(models.DATA_IO_ERROR)
        except Exception as e:
            print(e)
            print(data_file.filename)
            data_file.scan_results.append(models.DATA_UNEXPECTED)

        data_file.scan_time = time.time()
        data_file.scanned = True
        return data_file


class MCRegionFileAnalyser(object):
    def __init__(self, analyse_config):
        self.analyse_config = analyse_config

    def analyse(self, region):
        logger.debug("Start Analse Region File %s", region.filename)
        # analysedChunks = {}
        try:
            region_file = RegionFile(region.path)
            # self.chunks = region_file
            for x in range(32):
                for z in range(32):
                    # start the actual chunk scanning
                    chunk = models.MCRegionFileChunk(region, x, z)
                    if chunk:
                        chunk.scan_results.extend(self.scan_chunk(region_file, chunk))
                        region.chunks[(x, z)] = chunk

            # Now check for chunks sharing offsets:
            # Please note! region.py will mark both overlapping chunks
            # as bad (the one stepping outside his territory and the
            # good one). Only wrong located chunk with a overlapping
            # flag are really BAD chunks! Use this criterion to
            # discriminate
            metadata = region_file.metadata
            sharing = [
                k
                for k in metadata
                if (
                    metadata[k].status == STATUS_CHUNK_OVERLAPPING
                    and region.chunks[k].scan_results.isErrorExists(models.CHUNK_WRONG_LOCATED)
                )
            ]
            shared_counter = 0
            for k in sharing:
                region.chunks[k].scan_results.append(models.CHUNK_SHARED_OFFSET)
                region.chunks[k].scan_results.remove(models.CHUNK_WRONG_LOCATED)
                shared_counter += 1

            region.shared_offset = shared_counter
            del region_file
        except NoRegionHeader:  # The region has no header
            region.status = models.REGION_TOO_SMALL
        except IOError:
            region.status = models.REGION_UNREADABLE

        region.scan_time = time.time()
        region.scanned = True
        return region

    def scan_chunk(self, region_file, chunk):
        scan_results = []
        try:
            nbt_chunk = region_file.get_chunk(chunk.x, chunk.z)
            data_coords = util.get_chunk_data_coords(nbt_chunk)
            num_entities = len(nbt_chunk["Level"]["Entities"])
            global_coords = chunk.get_global_chunk_coords()

            if data_coords != global_coords:
                scan_results.append(models.CHUNK_WRONG_LOCATED)

            if (self.analyse_config["roles"]["chunk_entity_limit"] >= 0) and (
                num_entities > self.analyse_config["roles"]["chunk_entity_limit"]
            ):
                scan_results.append(models.CHUNK_TOO_MANY_ENTITIES)

            del nbt_chunk
        except InconceivedChunk:
            scan_results.append(models.CHUNK_NOT_CREATED)
        except (RegionHeaderError, ChunkDataError, ChunkHeaderError):
            scan_results.append(models.CHUNK_CORRUPTED)
        except KeyError:
            scan_results.append(models.CHUNK_MISSING_TAG)

        return scan_results

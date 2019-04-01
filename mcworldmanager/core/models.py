import logging
import ntpath
import os
import pathlib

from mcworldmanager.core import util

MC_FILE_TYPE_REGION = 1
MC_FILE_TYPE_DATA = 2
MC_FILE_TYPE_PLAYERS_OLD = 3
MC_FILE_TYPE_PLAYERS = 4


CHUNK_NOT_CREATED = -1
CHUNK_OK = 0
CHUNK_CORRUPTED = 1
CHUNK_WRONG_LOCATED = 2
CHUNK_TOO_MANY_ENTITIES = 3
CHUNK_SHARED_OFFSET = 4
CHUNK_MISSING_TAG = 5
CHUNK_SHARED_OFFSET_CROSS = 6

DATA_MALFORMED_FILE_ERROR = 10
DATA_IO_ERROR = 11
DATA_UNEXPECTED = 12

REGION_TOO_SMALL = 20
REGION_UNREADABLE = 21

SPECIAL_EYES_ERRORS = [
    REGION_TOO_SMALL,
    REGION_UNREADABLE,
    DATA_UNEXPECTED,
    DATA_IO_ERROR,
    DATA_MALFORMED_FILE_ERROR,
    CHUNK_SHARED_OFFSET_CROSS,
    CHUNK_CORRUPTED,
]

logger = logging.getLogger(__name__)


def build_old_player_file(path):
    return MCScannedFile(path, MC_FILE_TYPE_PLAYERS_OLD)


def build_player_file(path):
    return MCScannedFile(path, MC_FILE_TYPE_PLAYERS)


def build_mc_data_file(path):
    return MCDataFile(path)


def build_mc_region_file(path):
    return MCRegionFile(path)


class MCValidatesResultObject(list):
    def hasError(self):
        if len(self) > 0:
            return True
        else:
            return False

    def isErrorExists(self, error):
        if error not in self:
            return False
        else:
            return True

    def isOneOfErrorsExists(self, errors):
        for error in errors:
            if self.isErrorExists(error):
                return True

        return False


class MCWorlds(dict):
    """ Model Class for all Analyed worlds"""

    def __init__(self, worlds_directories):
        assert isinstance(worlds_directories, tuple)
        for world_directory in worlds_directories:
            currentWorld = MCWorld(world_directory)
            self[currentWorld.name] = currentWorld

    def all(self):
        allTasks = []
        for world in self:
            allTasks.extend(self[world].files.all())

        return allTasks


class MCWorld(object):
    def __init__(self, world_folder):
        assert isinstance(world_folder, str)
        assert os.path.isdir(world_folder)
        self.world_folder = world_folder
        self.name = pathlib.PurePath(world_folder).name
        self.files = self.MCFilesSet(self)

    class MCFilesSet(dict):
        """ Holder Class for the Analysed MC Files """

        def __init__(self, world):
            self[MC_FILE_TYPE_DATA] = util.scan_folder_content(
                os.path.join(world.world_folder, "data"), build_mc_data_file
            )
            self[MC_FILE_TYPE_REGION] = util.scan_folder_content(
                os.path.join(world.world_folder, "region"), build_mc_region_file
            )
            oldPlayerPath = os.path.join(world.world_folder, "players")
            if os.path.isdir(oldPlayerPath):
                self[MC_FILE_TYPE_PLAYERS_OLD] = util.scan_folder_content(oldPlayerPath, build_old_player_file)

            playerPath = os.path.join(world.world_folder, "playerdata")
            if os.path.isdir(playerPath):
                self[MC_FILE_TYPE_PLAYERS] = util.scan_folder_content(playerPath, build_player_file)

        def all(self):
            all = []
            for files in self.values():
                all.extend(files.values())
            return all

        def getFilesWithOneOfError(self, errors):
            faildFiles = []
            for fileType in self.keys():
                for fileName in self[fileType]:
                    if self[fileType][fileName].isOneOfErrorsExists(errors):
                        faildFiles.append(self[fileType][fileName])
            return faildFiles


class MCScannedElement(object):
    def __init__(self):
        self.scan_results = MCValidatesResultObject()

    def isOneOfErrorsExists(self, errors):
        return self.scan_results.isOneOfErrorsExists(errors)

    def getScan_Results(self):
        return self.scan_results


class MCScannedFile(MCScannedElement):
    def __init__(self, path, type):
        super().__init__()
        self.path = path
        self.type = type
        self.scanned = False
        self.scan_time = None
        self.filename = ntpath.basename(path)


class MCDataFile(MCScannedFile):
    def __init__(self, path):
        super().__init__(path, MC_FILE_TYPE_DATA)


class MCRegionFile(MCScannedFile):
    def __init__(self, path):
        super().__init__(path, MC_FILE_TYPE_REGION)
        coordX, coordZ = util.get_coords(self.filename)
        self.x = coordX
        self.z = coordZ
        self.chunks = {}

    def getScan_Results(self):
        results = self.scan_results
        for chunk in self.chunks:
            results.extend(self.chunks[chunk].scan_results)
        return list(dict.fromkeys(results))

    def isOneOfErrorsExists(self, errors):
        if super(MCRegionFile, self).isOneOfErrorsExists(errors):
            return True

        for chunk in self.chunks:
            if self.chunks[chunk].isOneOfErrorsExists(errors):
                return True

        return False

    def isManuelCheckRequired(self):
        if (len(self.chunksByFail(CHUNK_SHARED_OFFSET)) > 0) or (len(self.chunksByFail(CHUNK_CORRUPTED)) > 0):
            return True
        else:
            return False

    def chunksByFail(self, expected_fail):
        machedChunks = []
        for chunk in self.chunks:
            if expected_fail == CHUNK_OK:
                if len(self.chunks[chunk].scan_results) == 0:
                    machedChunks.append(self.chunks[chunk])

            elif expected_fail in self.chunks[chunk].scan_results:
                machedChunks.append(self.chunks[chunk])
        return machedChunks

    def countChunksByFail(self):
        faildMap = self.groupChunksByFail()
        fails = {}
        for fail in faildMap:
            fails[fail] = len(faildMap[fail])

        return fails

    def groupChunksByFail(self):
        fails = {}
        for chunk in self.chunks:
            currentChunk = self.chunks[chunk]
            if not currentChunk.scan_results or len(currentChunk.scan_results) == 0:
                if 0 in fails:
                    successfullChunks = fails[0]
                else:
                    successfullChunks = []

                successfullChunks.append(currentChunk)
                fails[0] = successfullChunks
            else:
                for fail in currentChunk.scan_results:
                    if fail in fails:
                        failedChunks = fails[fail]
                    else:
                        failedChunks = []
                    failedChunks.append(currentChunk)
                    fails[fail] = failedChunks
        return fails

    def chunksOk(self):
        chunks = []
        for chunk in self.chunks:
            if not chunk.hasErrors():
                chunks.append(self.chunks[chunk])

        return chunks


class MCRegionFileChunk(MCScannedElement):
    def __init__(self, region, x, z):
        super().__init__()
        self.region = region
        self.x = x
        self.z = z

    def get_global_chunk_coords(self):
        return util.get_global_chunk_coords(self.x, self.z, self.region.x, self.region.z)

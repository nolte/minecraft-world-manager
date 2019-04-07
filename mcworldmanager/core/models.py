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
    CHUNK_SHARED_OFFSET,
    CHUNK_CORRUPTED,
]

REGION_DIMENSION_NAME_OVERWORLD = "overworld"
REGION_DIMENSION_NAME_THE_END = "the_end"
REGION_DIMENSION_NAME_NETHER = "nether"

# Dimension names:
DIMENSION_NAMES = {
    "region": REGION_DIMENSION_NAME_OVERWORLD,
    "DIM1": REGION_DIMENSION_NAME_THE_END,
    "DIM-1": REGION_DIMENSION_NAME_NETHER,
}


logger = logging.getLogger(__name__)


def build_old_player_file(path):
    return MCScannedFile(path, MC_FILE_TYPE_PLAYERS_OLD)


def build_player_file(path):
    return MCScannedFile(path, MC_FILE_TYPE_PLAYERS)


def build_mc_data_file(path):
    return MCDataFile(path)


def build_mc_region_file_overworld(path):
    return MCRegionFile(path, REGION_DIMENSION_NAME_OVERWORLD)


def build_mc_region_file_nether(path):
    return MCRegionFile(path, REGION_DIMENSION_NAME_NETHER)


def build_mc_region_file_the_end(path):
    return MCRegionFile(path, REGION_DIMENSION_NAME_THE_END)


def build_mc_region_file(path, REGION_DIMENSION):
    return MCRegionFile(path, REGION_DIMENSION)


class FileSetHolder(dict):
    def isOneOfErrorsExists(self, errors):
        for element in self.values():
            if element.isOneOfErrorsExists(errors):
                return True
        return False
        # for region_dimension in self.keys():

    def getFilesWithOneOfError(self, errors):
        faildFiles = []
        for currentFile in self.keys():
            if self[currentFile].isOneOfErrorsExists(errors):
                faildFiles.append(self[currentFile])
        return faildFiles

    def getScan_Results(self):
        results = []
        for currentFile in self.keys():
            results.extend(self[currentFile].getScan_Results())
        return list(dict.fromkeys(results))


class MCValidatesResultObject(list):
    def hasError(self):
        if self:
            return True
        if not self:
            return False

    def isErrorExists(self, error):
        return error in self

    def isOneOfErrorsExists(self, errors):
        if isinstance(errors, list):
            for error in errors:
                if self.isErrorExists(error):
                    return True
        else:
            return self.isErrorExists(errors)


class MCWorlds(dict):
    """ Model Class for all Analyed worlds"""

    def __init__(self, worlds_directories):
        assert isinstance(worlds_directories, list)
        for world_directory in worlds_directories:
            currentWorld = MCWorld(world_directory)
            self[currentWorld.name] = currentWorld

    def all(self):
        allTasks = []
        for world in self:
            allTasks.extend(self[world].files.all())

        return allTasks

    def hasCorruptedWorld(self):
        return True


class MCWorld(object):
    def __init__(self, world_folder):
        assert isinstance(world_folder, str)
        assert os.path.isdir(world_folder)
        self.world_folder = world_folder
        self.name = pathlib.PurePath(world_folder).name
        self.files = self.MCFilesSet(self)

    class WorldRegionDimensionHolder(FileSetHolder):
        def __init__(self, world_folder):
            overworld_path = os.path.join(world_folder, "region")
            if os.path.isdir(overworld_path):
                self[REGION_DIMENSION_NAME_OVERWORLD] = FileSetHolder()
                self[REGION_DIMENSION_NAME_OVERWORLD] = util.scan_folder_content(
                    overworld_path, build_mc_region_file_overworld, self[REGION_DIMENSION_NAME_OVERWORLD]
                )
            nether_path = os.path.join(world_folder, "DIM-1/region")
            if os.path.isdir(nether_path):
                self[REGION_DIMENSION_NAME_NETHER] = FileSetHolder()
                self[REGION_DIMENSION_NAME_NETHER] = util.scan_folder_content(
                    nether_path, build_mc_region_file_nether, self[REGION_DIMENSION_NAME_NETHER]
                )
            the_end_path = os.path.join(world_folder, "DIM1/region")
            if os.path.isdir(the_end_path):
                self[REGION_DIMENSION_NAME_THE_END] = FileSetHolder()
                self[REGION_DIMENSION_NAME_THE_END] = util.scan_folder_content(
                    the_end_path, build_mc_region_file_the_end, self[REGION_DIMENSION_NAME_THE_END]
                )

        def all(self):
            allFiles = []
            for fileType in self.values():
                allFiles.extend(fileType.values())
            return allFiles

        def getFilesWithOneOfError(self, errors):
            faildFiles = []
            for currentFile in self.keys():
                if self[currentFile].isOneOfErrorsExists(errors):
                    faildFiles.extend(self[currentFile].getFilesWithOneOfError(errors))
            return faildFiles

        def getScan_Results(self):
            results = []
            for currentFile in self.keys():
                results.extend(self[currentFile].getScan_Results())
            return list(dict.fromkeys(results))

    class MCFilesSet(FileSetHolder):
        """ Holder Class for the Analysed MC Files """

        def __init__(self, world):
            self[MC_FILE_TYPE_DATA] = FileSetHolder()
            util.scan_folder_content(
                os.path.join(world.world_folder, "data"), build_mc_data_file, self[MC_FILE_TYPE_DATA]
            )
            # Load the Regions
            self[MC_FILE_TYPE_REGION] = MCWorld.WorldRegionDimensionHolder(world.world_folder)
            oldPlayerPath = os.path.join(world.world_folder, "players")
            if os.path.isdir(oldPlayerPath):
                self[MC_FILE_TYPE_PLAYERS_OLD] = FileSetHolder()
                self[MC_FILE_TYPE_PLAYERS_OLD] = util.scan_folder_content(
                    oldPlayerPath, build_old_player_file, self[MC_FILE_TYPE_PLAYERS_OLD]
                )

            playerPath = os.path.join(world.world_folder, "playerdata")
            if os.path.isdir(playerPath):
                self[MC_FILE_TYPE_PLAYERS] = FileSetHolder()
                self[MC_FILE_TYPE_PLAYERS] = util.scan_folder_content(
                    playerPath, build_player_file, self[MC_FILE_TYPE_PLAYERS]
                )

        def all(self):
            allMCFiles = []
            for files in self.keys():
                if files == MC_FILE_TYPE_REGION:
                    for regiontype in self[MC_FILE_TYPE_REGION]:
                        files = self[MC_FILE_TYPE_REGION][regiontype].values()
                        allMCFiles.extend(files)
                else:
                    allMCFiles.extend(self[files].values())
            return allMCFiles

        def getFilesWithOneOfError(self, errors):
            faildFiles = []
            for fileType in self.keys():
                holder = self[fileType]
                faildFiles.extend(holder.getFilesWithOneOfError(errors))
            return faildFiles

    def hasFilesWithOneOfError(self, expectedErrors):
        return self.files.getFilesWithOneOfError(expectedErrors)


class MCScannedElement(object):
    def __init__(self):
        self.scan_results = MCValidatesResultObject()

    def isOneOfErrorsExists(self, errors):
        return self.scan_results.isOneOfErrorsExists(errors)

    def getScan_Results(self):
        return self.scan_results

    def hasErrors(self):
        return self.scan_results.hasError()

    def isManuelCheckRequired(self):
        return self.isOneOfErrorsExists(SPECIAL_EYES_ERRORS)


class MCScannedFile(MCScannedElement):
    def __init__(self, path, mcFileType):
        super().__init__()
        self.path = path
        self.type = mcFileType
        self.scanned = False
        self.scan_time = None
        self.filename = ntpath.basename(path)


class MCDataFile(MCScannedFile):
    def __init__(self, path):
        super().__init__(path, MC_FILE_TYPE_DATA)


class MCRegionFile(MCScannedFile):
    def __init__(self, path, dimension_tag=None):
        super().__init__(path, MC_FILE_TYPE_REGION)
        self.dimension_tag = dimension_tag
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
        return self.isOneOfErrorsExists(SPECIAL_EYES_ERRORS)

    def chunksByFail(self, expected_fail):
        machedChunks = []
        for chunk in self.chunks:
            currentChunk = self.chunks[chunk]
            if expected_fail == CHUNK_OK:
                if not currentChunk.scan_results:
                    machedChunks.append(currentChunk)
            elif currentChunk.scan_results.isOneOfErrorsExists(expected_fail):
                machedChunks.append(currentChunk)
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
            if not currentChunk.scan_results:
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
            currentChunk = self.chunks[chunk]
            if not currentChunk.scan_results:
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

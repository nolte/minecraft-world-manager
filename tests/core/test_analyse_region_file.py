import os

from mcworldmanager.core import models
from mcworldmanager.core.analysers import MCRegionFileAnalyser

TEST_DIR = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, myPath + '/../')


def test_read_regionfile():
    regionFilePath = os.path.join(TEST_DIR, "data/regions/r.-1.-2.mca")
    regionFile = models.MCRegionFile(regionFilePath)
    assert regionFile.filename == "r.-1.-2.mca"
    assert -1 == regionFile.x
    assert -2 == regionFile.z
    assert regionFile.type == models.MC_FILE_TYPE_REGION
    assert regionFile.path == regionFilePath
    assert not regionFile.scanned


def test_scan_regionfile():
    regionFilePath = os.path.join(TEST_DIR, "data/regions/r.0.0.mca")
    regionFile = models.MCRegionFile(regionFilePath)
    assert regionFile.filename == "r.0.0.mca"
    assert 0 == regionFile.x
    assert 0 == regionFile.z
    assert regionFile.type == models.MC_FILE_TYPE_REGION
    assert regionFile.path == regionFilePath
    config = {"roles": {"chunk_entity_limit": -1}}

    analyser = MCRegionFileAnalyser(config)
    analyser.analyse(regionFile)
    assert regionFile.scanned
    assert 1024 == len(regionFile.chunks)
    assert 2 == len(regionFile.chunksByFail(models.CHUNK_CORRUPTED))
    assert 11 == len(regionFile.chunksByFail(models.CHUNK_WRONG_LOCATED))
    assert 33 == len(regionFile.chunksByFail(models.CHUNK_SHARED_OFFSET))

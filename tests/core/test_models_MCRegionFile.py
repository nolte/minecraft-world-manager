import pytest

from mcworldmanager.core import models


@pytest.fixture
def regionFile():
    region = models.MCRegionFile("r.-1.-2.mca")
    chunkNoErrors = models.MCRegionFileChunk(region, 0, 0)
    chunkCriticalError = models.MCRegionFileChunk(region, 0, 1)
    chunkCriticalError.scan_results = models.MCValidatesResultObject([models.CHUNK_SHARED_OFFSET])
    chunkNonCriticalError = models.MCRegionFileChunk(region, 0, 2)
    chunkNonCriticalError.scan_results = models.MCValidatesResultObject([models.CHUNK_MISSING_TAG])
    region.chunks = {(0, 0): chunkNoErrors, (0, 1): chunkCriticalError, (0, 2): chunkNonCriticalError}
    return region


def test_CheckExtractedCoordinates(regionFile):
    assert regionFile.x == -1
    assert regionFile.z == -2


def test_CheckScanResultsKey(regionFile):
    assert regionFile.getScan_Results() == [models.CHUNK_SHARED_OFFSET, models.CHUNK_MISSING_TAG]
    assert regionFile.isManuelCheckRequired()


def test_CheckScanResultsKey_non_critical_errors(regionFile):
    chunkNoErrors = models.MCRegionFileChunk(regionFile, 0, 0)
    chunkNonCriticalError = models.MCRegionFileChunk(regionFile, 0, 2)
    chunkNonCriticalError.scan_results = models.MCValidatesResultObject([models.CHUNK_MISSING_TAG])
    regionFile.chunks = {(0, 0): chunkNoErrors, (0, 2): chunkNonCriticalError}
    assert not regionFile.isManuelCheckRequired()


def test_select_chunks_without_errors(regionFile):
    assert len(regionFile.chunks) == 3
    assert len(regionFile.chunksOk()) == 1
    assert regionFile.chunksOk()[0].x == 0
    assert regionFile.chunksOk()[0].z == 0


def test_select_chunks_with_error(regionFile):
    assert len(regionFile.chunksByFail(models.CHUNK_SHARED_OFFSET)) == 1
    assert not regionFile.chunksByFail(models.CHUNK_NOT_CREATED)


def test_select_chunks_with_error_as_Array(regionFile):
    assert len(regionFile.chunksByFail([models.CHUNK_SHARED_OFFSET])) == 1
    assert not regionFile.chunksByFail([models.CHUNK_NOT_CREATED])


def test_select_chunks_with_one_of_errors(regionFile):
    assert len(regionFile.chunksByFail([models.CHUNK_SHARED_OFFSET, models.CHUNK_NOT_CREATED])) == 1

import pytest

from mcworldmanager.core import models
from mcworldmanager.report import report_manager
from unittest.mock import MagicMock



@pytest.fixture
def reporter():
    return report_manager.MarkdownReporter({"report":{"details_level":"MINIMAL"}})    

def test_create_yaml_report_from_successfull_element(reporter):
    regionFile = models.MCRegionFile("r.-1.-2.mca")
    report = reporter.createReport(regionFile)
    expectedReport = { "successfull": True ,"filename":"r.-1.-2.mca"}

    assert report == expectedReport


def test_create_yaml_report_from_faild_element(reporter):
    regionFile = models.MCRegionFile("r.-1.-2.mca")
    regionFile.isOneOfErrorsExists = MagicMock(return_value=True)
    corruptedChunk = models.MCRegionFileChunk(regionFile,0,0)
    corruptedChunk.scan_results = [models.CHUNK_SHARED_OFFSET]
    chunks = [corruptedChunk]
    regionFile.chunksByFail = MagicMock(return_value=chunks)
    
    report = reporter.createReport(regionFile)
    expectedReport = { "successfull": False ,"filename":"r.-1.-2.mca", "chunks": [{"x": 0,"z":0,'global_x': -32, 'global_z': -64,"reasons":[4] }] }

    assert report == expectedReport    
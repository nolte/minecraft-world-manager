import pytest
import os
from yaml import load, dump
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from mcworldmanager.core import models
from mcworldmanager.report import report_manager
from unittest.mock import MagicMock


TEST_DIR = os.path.dirname(os.path.abspath(__file__))

@pytest.fixture
def reporter():
    return report_manager.YamlReporter({"report":{"details_level":"MINIMAL"}})    

def test_create_yaml_report_from_successfull_element(reporter):
    regionFile = models.MCRegionFile("r.-1.-2.mca")
    report = reporter.createReport(regionFile)
    expectedReport = open(os.path.join(TEST_DIR, "golden_files/region-minimal-successfull.yml")).read()
    assert report == expectedReport


def test_create_yaml_report_from_faild_element(reporter):
    regionFile = models.MCRegionFile("r.-1.-2.mca")
    regionFile.isOneOfErrorsExists = MagicMock(return_value=True)
    corruptedChunk = models.MCRegionFileChunk(regionFile,0,0)
    corruptedChunk.scan_results = [models.CHUNK_SHARED_OFFSET]
    chunks = [corruptedChunk]
    regionFile.chunksByFail = MagicMock(return_value=chunks)
    
    report = reporter.createReport(regionFile)
    expectedReport = open(os.path.join(TEST_DIR, "golden_files/region-minimal-faild.yml")).read()
    assert report == expectedReport
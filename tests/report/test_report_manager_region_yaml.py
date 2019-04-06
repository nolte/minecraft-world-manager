import os
from unittest.mock import MagicMock

import pytest

from mcworldmanager.core import models
from mcworldmanager.report import region_reporter

TEST_DIR = os.path.dirname(os.path.abspath(__file__))


@pytest.fixture
def config():
    return {"report": {"details_level": "MINIMAL"}}


def test_create_yaml_report_from_successfull_element(config):
    regionFile = models.MCRegionFile("r.-1.-2.mca")
    regionFile.isManuelCheckRequired = MagicMock(return_value=False)
    reporter = region_reporter.RegionReport(config, regionFile)
    report = reporter.toYaml()
    expectedReport = open(os.path.join(TEST_DIR, "golden_files/region-minimal-successfull.yml")).read()
    assert report == expectedReport


def test_create_yaml_report_from_faild_element(config):
    regionFile = models.MCRegionFile("r.-1.-2.mca")
    regionFile.isManuelCheckRequired = MagicMock(return_value=True)

    corruptedChunk = models.MCRegionFileChunk(regionFile, 0, 0)
    corruptedChunk.scan_results = [models.CHUNK_SHARED_OFFSET]
    chunks = [corruptedChunk]
    regionFile.chunksByFail = MagicMock(return_value=chunks)
    reporter = region_reporter.RegionReport(config, regionFile)
    report = reporter.toYaml()
    print(report)
    expectedReport = open(os.path.join(TEST_DIR, "golden_files/region-minimal-faild.yml")).read()
    assert report == expectedReport

from mcworldmanager.core import models
from mcworldmanager.report import region_reporter

REPORT_TYPE_YAML = "YAML"
REPORT_TYPE_MARKDOWN = "MARKDOWN"
REPORT_TYPE_COMMAND_LINE = "COMMANDLINE"
# from mcworldmanager.report import reportmarkdown, reportyaml

REPORT_DETAIL_LEVEL_MINIMAL = "MINIMAL"


def createReport(config, reportedObject):
    if isinstance(reportedObject, models.MCRegionFile):
        print(region_reporter.RegionReport(config, reportedObject).toCommandline())
    if isinstance(reportedObject, models.MCWorlds):
        print(region_reporter.WorldsReporter(config, reportedObject).toCommandline())

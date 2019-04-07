import yaml

from mcworldmanager.core import models
from mcworldmanager.report import region_reporter

REPORT_TYPE_YAML = "YAML"
REPORT_TYPE_COMMAND_LINE = "COMMANDLINE"

OUTPUT_FORMATS = [REPORT_TYPE_YAML, REPORT_TYPE_COMMAND_LINE]
# from mcworldmanager.report import reportmarkdown, reportyaml

REPORT_DETAIL_LEVEL_MINIMAL = "MINIMAL"


def createReport(config, reportedObject):
    reporter = None
    if isinstance(reportedObject, models.MCRegionFile):
        reporter = region_reporter.RegionReport(config, reportedObject)
    elif isinstance(reportedObject, models.MCWorlds):
        reporter = region_reporter.WorldsReporter(config, reportedObject)

    if reporter:
        if config["report"]["format"] == REPORT_TYPE_COMMAND_LINE:
            print(reporter.toCommandline())
        elif config["report"]["format"] == REPORT_TYPE_YAML:
            print(reporter.toYaml())

        if "path" in config["report"]:
            with open(config["report"]["path"], "w") as outfile:
                yaml.dump(reporter.toYamlObject(), outfile, default_flow_style=False)

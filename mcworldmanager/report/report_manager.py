
import os
from yaml import load, dump
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper


from mcworldmanager.core import models
from mcworldmanager.core.util import colors,special_chars
from mcworldmanager.report import reportmarkdown
REPORT_TYPE_YAML = "YAML"
REPORT_TYPE_MARKDOWN = "MARKDOWN"
REPORT_TYPE_COMMAND_LINE = "COMMANDLINE"
#from mcworldmanager.report import reportmarkdown, reportyaml

REPORT_DETAIL_LEVEL_MINIMAL = "MINIMAL"

def createReport(config, reportedObject):
    formatter = {
        REPORT_TYPE_YAML: YamlReporter(config),
        REPORT_TYPE_MARKDOWN: MarkdownReporter(config),
        REPORT_TYPE_COMMAND_LINE: CommandLineReporter(config),
    }

    reports = {}
    for report_format in config["report"]["formats"]:
        reports[report_format] = formatter[report_format].createReport(reportedObject)



class ReportModel(dict):
    def __init__(self, config, objectForReport):
        self["successfull"] = not objectForReport.isOneOfErrorsExists(models.SPECIAL_EYES_ERRORS)


class RegionReportModel(ReportModel):
    def __init__(self, config, objectForReport):
        super().__init__(config, objectForReport)
        self["filename"] = objectForReport.filename
        if config["report"]["details_level"] == REPORT_DETAIL_LEVEL_MINIMAL:
            if not self["successfull"]:
                chunks = objectForReport.chunksByFail(models.SPECIAL_EYES_ERRORS)
                self["chunks"] = []
                for chunk in chunks:
                    globalCords = chunk.get_global_chunk_coords()
                    chunkObj = {
                        "x": chunk.x,
                        "z": chunk.z,
                        "global_x": globalCords[0],
                        "global_z": globalCords[1],                        
                        "reasons": chunk.scan_results
                    }
                    self["chunks"].append(chunkObj)

class Reporter(object):
    def __init__(self, config, report_type):
        self.type = report_type
        self.config = config

    def createReport(self, objectForReport):
        if objectForReport.type == models.MC_FILE_TYPE_REGION:
            model = RegionReportModel(self.config, objectForReport)        
        else: 
            model = ReportModel(self.config, objectForReport)
        
        return model

class YamlReporter(Reporter):
    def __init__(self,config):
        super().__init__(config, REPORT_TYPE_YAML)

    def createReport(self, objectForReport):
        report_model = super().createReport(objectForReport)
        #yaml.add_representer(dict, lambda self, data: yaml.representer.SafeRepresenter.represent_dict(self, data.items()))
        return yaml.dump(dict(report_model))

class CommandLineReporter(Reporter):
    def __init__(self,config):
        super().__init__(config, REPORT_TYPE_MARKDOWN)

    def createReport(self, objectForReport):
        report_model = super().createReport(objectForReport)
        reporter = reportmarkdown.RegionReporter(self.config["report"]["details_level"], objectForReport)
        report = reporter.report("")

        print(report)


        return report

class MarkdownReporter(Reporter):
    def __init__(self,config):
        super().__init__(config, REPORT_TYPE_MARKDOWN)

    def createReport(self, objectForReport):
        report_model = super().createReport(objectForReport)
        print("markdown hallo")
        return report_model
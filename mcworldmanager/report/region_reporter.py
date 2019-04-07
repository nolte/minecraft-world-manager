import os

import yaml
from terminaltables import AsciiTable

from mcworldmanager.core import models
from mcworldmanager.core.util import colors
from mcworldmanager.report import report_utils

REPORT_DETAIL_LEVEL_MINIMAL = "MINIMAL"


class Report(object):
    def __init__(self, config, successfull):
        self.config = config
        self.successfull = successfull

    def wasSuccessfull(self):
        return self.successfull

    def toYaml(self):
        return {"successfull": self.successfull}


class RegionReport(Report):
    def __init__(self, config, region):
        super().__init__(config, not region.isManuelCheckRequired())
        self.region = region

    def getRegionRow(self):
        chunksResultColums = [
            len(self.region.chunksByFail(models.CHUNK_CORRUPTED)),
            len(self.region.chunksByFail(models.CHUNK_WRONG_LOCATED)),
            len(self.region.chunksByFail(models.CHUNK_TOO_MANY_ENTITIES)),
            len(self.region.chunksByFail(models.CHUNK_SHARED_OFFSET)),
            len(self.region.chunksByFail(models.CHUNK_MISSING_TAG)),
            len(self.region.chunksByFail(models.CHUNK_OK)),
            len(self.region.chunks),
            len(self.region.chunksByFail(models.CHUNK_NOT_CREATED)),
        ]
        return chunksResultColums

    def toCommandline(self):
        report = ""
        report += report_utils.text_blod("Region Report") + os.linesep
        report += report_utils.line_sperator()

        if self.wasSuccessfull():
            statusIcon = report_utils.icon_success()
        else:
            statusIcon = report_utils.icon_fail()

        report += "file: {:} {:}".format(report_utils.text_blod(self.region.filename), statusIcon)
        report += os.linesep

        table_data = [report_utils.WORLD_REGION_TABLE_HEADLINE]
        row = ["Counts"]
        row.extend(self.getRegionRow())
        table_data.append(row)
        table = AsciiTable(table_data)
        report += table.table
        report += os.linesep
        if self.region.isManuelCheckRequired():
            report += os.linesep + "{:}Corrupted Chunks: {:} ".format(colors.bold, colors.reset) + os.linesep
            report += report_utils.build_chunkTable(self.region.chunksByFail(models.SPECIAL_EYES_ERRORS))

        return report

    def toYamlObject(self):
        baseYaml = super().toYaml()
        if self.region.getScan_Results():
            baseYaml["reasons"] = list(self.region.getScan_Results())

        baseYaml["path"] = self.region.path
        if self.config["report"]["details_level"] == REPORT_DETAIL_LEVEL_MINIMAL:
            if not baseYaml["successfull"] and self.region.type == models.MC_FILE_TYPE_REGION:
                chunks = self.region.chunksByFail(models.SPECIAL_EYES_ERRORS)
                baseYaml["chunks"] = []
                for chunk in chunks:
                    globalCords = chunk.get_global_chunk_coords()
                    chunkObj = {
                        "x": chunk.x,
                        "z": chunk.z,
                        "global_x": globalCords[0],
                        "global_z": globalCords[1],
                        "reasons": list(chunk.scan_results),
                    }
                    baseYaml["chunks"].append(chunkObj)
        return baseYaml

    def toYaml(self):
        return yaml.dump(self.toYamlObject())


class WorldReporter(Report):
    def __init__(self, config, world):
        super().__init__(config, not world.hasFilesWithOneOfError(models.SPECIAL_EYES_ERRORS))
        self.world = world

    def toYaml(self):
        baseYaml = super().toYaml()
        corruptedFiles = []
        corruptedFilesList = self.world.files.getFilesWithOneOfError(models.SPECIAL_EYES_ERRORS)
        for file in corruptedFilesList:
            corruptedFiles.append(RegionReport(self.config, file).toYamlObject())
        if corruptedFiles:
            baseYaml["corrupted"] = corruptedFiles
        return baseYaml

    def regionCollectedRow(self):
        worldRegionRow = {}
        worldRegionRow[models.CHUNK_CORRUPTED] = 0
        worldRegionRow[models.CHUNK_WRONG_LOCATED] = 0
        worldRegionRow[models.CHUNK_TOO_MANY_ENTITIES] = 0
        worldRegionRow[models.CHUNK_SHARED_OFFSET] = 0
        worldRegionRow[models.CHUNK_MISSING_TAG] = 0
        worldRegionRow[models.CHUNK_OK] = 0
        worldRegionRow["all"] = 0
        worldRegionRow[models.CHUNK_NOT_CREATED] = 0

        for regionDimension in self.world.files[models.MC_FILE_TYPE_REGION]:
            holder = self.world.files[models.MC_FILE_TYPE_REGION][regionDimension]
            for region in holder.values():
                worldRegionRow[models.CHUNK_CORRUPTED] += len(region.chunksByFail(models.CHUNK_CORRUPTED))
                worldRegionRow[models.CHUNK_WRONG_LOCATED] += len(region.chunksByFail(models.CHUNK_WRONG_LOCATED))
                worldRegionRow[models.CHUNK_TOO_MANY_ENTITIES] += len(
                    region.chunksByFail(models.CHUNK_TOO_MANY_ENTITIES)
                )
                worldRegionRow[models.CHUNK_SHARED_OFFSET] += len(region.chunksByFail(models.CHUNK_SHARED_OFFSET))
                worldRegionRow[models.CHUNK_MISSING_TAG] += len(region.chunksByFail(models.CHUNK_MISSING_TAG))
                worldRegionRow[models.CHUNK_OK] += len(region.chunksByFail(models.CHUNK_OK))
                worldRegionRow["all"] += len(region.chunks)
                worldRegionRow[models.CHUNK_NOT_CREATED] += len(region.chunksByFail(models.CHUNK_NOT_CREATED))

        return worldRegionRow.values()


class WorldsReporter(Report):
    def __init__(self, config, worlds):
        super().__init__(config, not worlds.hasCorruptedWorld())
        self.worlds = worlds

    def toYamlObject(self):
        baseYaml = super().toYaml()
        worlds = {}
        for world in self.worlds:
            currentWorld = self.worlds[world]
            worlds[world] = WorldReporter(self.config, currentWorld).toYaml()

        baseYaml["worlds"] = worlds
        return baseYaml

    def toYaml(self):
        return yaml.dump(self.toYamlObject())

    def toCommandline(self):
        report = ""
        report += report_utils.text_blod("Worlds Analyse Report") + os.linesep
        report += report_utils.line_sperator()

        table_data = []
        overview_table_headline = ["World", "Region Files", "Data Files", "Player Files"]
        overview_table_data = []
        special_eyes_data = []

        for world in self.worlds:
            row = []

            files = []

            currentWorld = self.worlds[world]
            if currentWorld.hasFilesWithOneOfError(models.SPECIAL_EYES_ERRORS):
                worldStatusIcon = report_utils.icon_fail()
            else:
                worldStatusIcon = report_utils.icon_success()

            currentName = "{:} {:}".format(currentWorld.name, worldStatusIcon)

            row.append(currentName)
            files.append(currentName)
            for failFile in currentWorld.files.getFilesWithOneOfError(models.SPECIAL_EYES_ERRORS):
                scan_results_list = failFile.scan_results
                if failFile.type == models.MC_FILE_TYPE_REGION:
                    scan_results_list = []
                    scan_results_list = failFile.getScan_Results()

                eyes_row = [
                    currentWorld.name,
                    failFile.filename,
                    str(report_utils.build_human_readable_errorList(scan_results_list)),
                ]
                special_eyes_data.append(eyes_row)

            files.append(str(len(currentWorld.files[models.MC_FILE_TYPE_REGION].all())))
            files.append(str(len(currentWorld.files[models.MC_FILE_TYPE_DATA])))
            if models.MC_FILE_TYPE_PLAYERS_OLD in currentWorld.files:
                files.append(str(len(currentWorld.files[models.MC_FILE_TYPE_PLAYERS_OLD])))
            else:
                files.append(str(len(currentWorld.files[models.MC_FILE_TYPE_PLAYERS])))

            row.extend(WorldReporter(self.config, currentWorld).regionCollectedRow())
            table_data.append(row)
            overview_table_data.append(files)

        report += report_utils.drawTable(overview_table_headline, overview_table_data) + os.linesep
        report += os.linesep
        report += report_utils.text_blod("Report Overview") + os.linesep
        report += report_utils.drawTable(report_utils.WORLD_REGION_TABLE_HEADLINE, table_data) + os.linesep

        if special_eyes_data:
            report += os.linesep
            report += report_utils.text_blod("Special Eye Files") + os.linesep
            SPECIAL_EYES_HEADLINE = ["World", "File", "Problems"]
            report += report_utils.drawTable(SPECIAL_EYES_HEADLINE, special_eyes_data) + os.linesep

        return report

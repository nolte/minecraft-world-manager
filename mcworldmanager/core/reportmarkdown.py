import logging

from terminaltables import AsciiTable

from mcworldmanager.core import models

logger = logging.getLogger(__name__)


WORLD_REGION_TABLE_HEADLINE = [
    "Problem",
    "Corrupted",
    "Wrong l.",
    "Entities",
    "Shared o.",
    "Missing tag",
    "Total chunks",
    "All Chunks",
    "Not Created",
]


class WorldsReporter(object):
    def __init__(self, worlds):
        self.worlds = worlds

    def report(self, reportText):
        reportText += "# Report\n\n"
        table_data = [WORLD_REGION_TABLE_HEADLINE]
        overview_table_data = [["World", "Region Files", "Data Files", "Player Files"]]

        specialWorldFiles = {}
        for world in self.worlds:
            row = []
            files = []
            currentWorld = self.worlds[world]
            row.append(currentWorld.name)
            files.append(currentWorld.name)
            specialWorldFiles[currentWorld.name] = currentWorld.files.getFilesWithOneOfError(models.SPECIAL_EYES_ERRORS)
            files.append(str(len(currentWorld.files[models.MC_FILE_TYPE_REGION])))
            files.append(str(len(currentWorld.files[models.MC_FILE_TYPE_DATA])))
            if models.MC_FILE_TYPE_PLAYERS_OLD in currentWorld.files:
                files.append(str(len(currentWorld.files[models.MC_FILE_TYPE_PLAYERS_OLD])))
            else:
                files.append(str(len(currentWorld.files[models.MC_FILE_TYPE_PLAYERS])))

            row.extend(WorldReporter(self.worlds[world]).regionValidation())
            table_data.append(row)
            overview_table_data.append(files)

        table = AsciiTable(overview_table_data)
        reportText += table.table
        reportText += "\n\n"

        table = AsciiTable(table_data)
        reportText += table.table
        reportText += "\n\n"

        reportText += "# Special Eye Files\n\n"
        for world in specialWorldFiles:
            reportText += "## World {:}".format(world) + "\n\n"
            brokenFiles = specialWorldFiles[world]
            reportText += "Broken Files: {:}".format(str(len(brokenFiles))) + "\n\n"
            for broken in brokenFiles:
                reportText += "Files: {:} fails {:}".format(broken.filename, str(broken.getScan_Results())) + "\n\n"

        return reportText


class WorldReporter(object):
    def __init__(self, world):
        self.world = world

    def report(self, report):
        report += "World {:}".format(self.world.name) + "\n\n"

    def regionValidation(self):
        worldRegionRow = {}
        worldRegionRow[models.CHUNK_CORRUPTED] = 0
        worldRegionRow[models.CHUNK_WRONG_LOCATED] = 0
        worldRegionRow[models.CHUNK_TOO_MANY_ENTITIES] = 0
        worldRegionRow[models.CHUNK_SHARED_OFFSET] = 0
        worldRegionRow[models.CHUNK_MISSING_TAG] = 0
        worldRegionRow[models.CHUNK_OK] = 0
        worldRegionRow["all"] = 0
        worldRegionRow[models.CHUNK_NOT_CREATED] = 0
        for regionName in self.world.files[models.MC_FILE_TYPE_REGION]:
            region = self.world.files[models.MC_FILE_TYPE_REGION][regionName]
            worldRegionRow[models.CHUNK_CORRUPTED] += len(region.chunksByFail(models.CHUNK_CORRUPTED))
            worldRegionRow[models.CHUNK_WRONG_LOCATED] += len(region.chunksByFail(models.CHUNK_WRONG_LOCATED))
            worldRegionRow[models.CHUNK_TOO_MANY_ENTITIES] += len(region.chunksByFail(models.CHUNK_TOO_MANY_ENTITIES))
            worldRegionRow[models.CHUNK_SHARED_OFFSET] += len(region.chunksByFail(models.CHUNK_SHARED_OFFSET))
            worldRegionRow[models.CHUNK_MISSING_TAG] += len(region.chunksByFail(models.CHUNK_MISSING_TAG))
            worldRegionRow[models.CHUNK_OK] += len(region.chunksByFail(models.CHUNK_OK))
            worldRegionRow["all"] += len(region.chunks)
            worldRegionRow[models.CHUNK_NOT_CREATED] += len(region.chunksByFail(models.CHUNK_NOT_CREATED))

        return worldRegionRow.values()


class RegionReporter(object):
    def __init__(self, region):
        self.region = region

    def report(self, report):
        report += "# Region " + "{:} ({:d},{:d})".format(self.region.filename, self.region.x, self.region.z) + "\n\n"
        table_data = [WORLD_REGION_TABLE_HEADLINE]

        row = ["Counts"]

        row.extend(self.getRegionRow())
        table_data.append(row)
        table = AsciiTable(table_data)
        report += table.table
        report += "\n\n## Chunks Report \n\n"
        faildGroups = self.region.groupChunksByFail()
        for resultGroup in faildGroups:
            report += "### Fails " + "{:}".format(resultGroup) + "\n\n"
            chunk_table_data = [["index", "x", "z", "Global X", "Global Y"]]
            chunk_table_data.extend(self.getChunksRows(faildGroups[resultGroup]))
            table = AsciiTable(chunk_table_data)
            report += table.table
            report += "\n\n"

        return report        

    def getChunksRows(self, chunks):
        chunk_rows = []
        index = 0
        for chunk in chunks:
            row = [index, chunk.x, chunk.z, chunk.get_global_chunk_coords()[0], chunk.get_global_chunk_coords()[1]]
            chunk_rows.append(row)

            index += 1
        return chunk_rows

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

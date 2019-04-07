import os

from terminaltables import AsciiTable

from mcworldmanager.core import models
from mcworldmanager.core.util import colors, special_chars

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

ERROR_TEXT_MAPPING = {
    models.CHUNK_CORRUPTED: "Corrupted",
    models.CHUNK_WRONG_LOCATED: "Wrong l.",
    models.CHUNK_TOO_MANY_ENTITIES: "Entities",
    models.CHUNK_SHARED_OFFSET: "Shared offset",
    models.CHUNK_MISSING_TAG: "Missing tag",
    models.CHUNK_NOT_CREATED: "Not Created",
}


def text_blod(text):
    return "{:}{:}{:}".format(colors.bold, text, colors.reset)


def icon_fail():
    return "{:}{:}{:}".format(colors.fg.red, special_chars.ballot_heavy, colors.reset)


def icon_success():
    return "{:}{:}{:}".format(colors.fg.green, special_chars.check_heavy, colors.reset)


def line_sperator():
    return "--------------------------------------------------" + os.linesep


def build_human_readable_errorList(errors):
    failString = ""
    for error in errors:
        if error in ERROR_TEXT_MAPPING:
            failString += "{:}, ".format(ERROR_TEXT_MAPPING[error])
        else:
            failString += "{:}, ".format(error)

    return failString


def build_chunkTable(chunks):

    CHUNKS_HEADLINE = ["x", "z", "global_x", "global_z", "Problems"]
    table_data = [CHUNKS_HEADLINE]
    for chunk in chunks:
        row = [
            chunk.x,
            chunk.z,
            chunk.get_global_chunk_coords()[0],
            chunk.get_global_chunk_coords()[1],
            build_human_readable_errorList(chunk.scan_results),
        ]
        table_data.append(row)
    table = AsciiTable(table_data)
    return table.table


def mediateTableHeadline(tableHeadline):
    headline = []
    for colum_headline in tableHeadline:
        headline.append(text_blod(colum_headline))
    return headline


def drawTable(headline, data_rows):
    table_data = [mediateTableHeadline(headline)]
    for data_row in data_rows:
        table_data.append(data_row)
    table = AsciiTable(table_data)
    return table.table

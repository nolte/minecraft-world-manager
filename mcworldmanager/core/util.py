import binascii
import logging
import os

logger = logging.getLogger(__name__)


def build_analyse_file(path, builder):
    assert isinstance(path, str)
    assert os.path.exists(path)
    return builder(path)


def scan_folder_content(path, builder, files):
    assert isinstance(path, str)
    assert os.path.isdir(path)
    for mcDirElement in os.listdir(path):
        mcfile = build_analyse_file(os.path.join(path, mcDirElement), builder)
        files[mcfile.filename] = mcfile

    logger.debug("Listened files from %s count: %i", path, len(files))
    return files


def get_chunk_data_coords(nbt_file):
    """ Gets the coords stored in the NBT structure of the chunk.

        Takes an nbt obj and returns the coords as integers.
        Don't confuse with get_global_chunk_coords! """

    level = nbt_file.__getitem__("Level")

    coordX = level.__getitem__("xPos").value
    coordZ = level.__getitem__("zPos").value

    return coordX, coordZ


def is_gz_file(filepath):
    with open(filepath, "rb") as test_f:
        return binascii.hexlify(test_f.read(2)) == b"1f8b"


def get_global_chunk_coords(chunkX, chunkZ, regionX, regionZ):
    """ Takes the region  coordinates and the chunk local
        coords and returns the global chunkcoords as integers. """
    chunkX += regionX * 32
    chunkZ += regionZ * 32
    return chunkX, chunkZ


def get_coords(filename):
    """ Splits the region filename (full pathname or just filename)
        and returns his region X and Z coordinates as integers. """
    splitted_filename = filename.split(".")
    try:
        coordX = int(splitted_filename[1])
        coordZ = int(splitted_filename[2])
        logger.debug("Analyse MC Data File Kords %s %i %i", filename, coordX, coordZ)
    except ValueError:
        logger.debug("faild to parse %s", filename)
        raise InvalidFileName()

    return coordX, coordZ


class InvalidFileName(IOError):
    pass


class special_chars:
    ballot = "\u2717"
    ballot_heavy = "\u2718"
    check_heavy = "\u2714"
    exclamation_mark = "\u0021"


# colored text and background
class colors:
    """Colors class:reset all colors with colors.reset; two
        sub classes fg for foreground
        and bg for background; use as colors.subclass.colorname.
        i.e. colors.fg.red or colors.bg.greenalso, the generic bold, disable,
        underline, reverse, strike through,
        and invisible work with the main class i.e. colors.bold
    """

    reset = "\033[0m"
    bold = "\033[01m"
    disable = "\033[02m"
    underline = "\033[04m"
    reverse = "\033[07m"
    strikethrough = "\033[09m"
    invisible = "\033[08m"

    class fg:
        black = "\033[30m"
        red = "\033[31m"
        green = "\033[32m"
        orange = "\033[33m"
        blue = "\033[34m"
        purple = "\033[35m"
        cyan = "\033[36m"
        lightgrey = "\033[37m"
        darkgrey = "\033[90m"
        lightred = "\033[91m"
        lightgreen = "\033[92m"
        yellow = "\033[93m"
        lightblue = "\033[94m"
        pink = "\033[95m"
        lightcyan = "\033[96m"

    class bg:
        black = "\033[40m"
        red = "\033[41m"
        green = "\033[42m"
        orange = "\033[43m"
        blue = "\033[44m"
        purple = "\033[45m"
        cyan = "\033[46m"
        lightgrey = "\033[47m"

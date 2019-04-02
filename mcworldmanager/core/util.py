import binascii
import logging
import os

logger = logging.getLogger(__name__)


def build_analyse_file(path, builder):
    assert isinstance(path, str)
    assert os.path.exists(path)
    return builder(path)


def scan_folder_content(path, builder):
    assert isinstance(path, str)
    assert os.path.isdir(path)
    files = {}
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

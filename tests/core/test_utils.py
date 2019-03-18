import pytest

from mcworldmanager.core import util

testdata1 = [
    ("r.-1.-2.mca", -1, -2),
    ("r.-5.20.mca", -5, 20),
    ("r.5.-20.mca", 5, -20),
    ("r.5.20.mca", 5, 20),
    ("r.-1.-1.mca", -1, -1),
    ("r.-1.-2.mca", -1, -2),
]


@pytest.mark.parametrize("filename,expected_coordX, expected_coordZ", testdata1)
def test_get_coords(filename, expected_coordX, expected_coordZ):
    coordX, coordZ = util.get_coords(filename)
    assert coordX == expected_coordX
    assert coordZ == expected_coordZ


testdata2 = [("r.-1.-X.mca"), ("r.-X.20.mca"), ("r.5-20.mca"), ("r5.20.mca")]


@pytest.mark.parametrize("filename", testdata2)
def test_get_global_chunk_coords_invalidFileName(filename):
    with pytest.raises(util.InvalidFileName):
        util.get_coords(filename)


testdata = [(1, 1, -1, -1, -31, -31), (1, 1, 1, 1, 33, 33), (1, 1, -1, 1, -31, 33), (1, 1, 1, -1, 33, -31)]


@pytest.mark.parametrize("chunkX, chunkZ, regionX, regionZ ,expected_global_coordX, expected_global_coordZ", testdata)
def test_get_global_chunk_coords(chunkX, chunkZ, regionX, regionZ, expected_global_coordX, expected_global_coordZ):
    global_coordX, global_coordZ = util.get_global_chunk_coords(chunkX, chunkZ, regionX, regionZ)
    assert global_coordX == expected_global_coordX
    assert global_coordZ == expected_global_coordZ

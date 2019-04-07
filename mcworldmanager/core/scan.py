import os

from mcworldmanager.core import models


def build_internal_structure_world(path):
    assert isinstance(path, str)
    assert os.path.isdir(path)

    world = models.MCWorld(path)

import logging

logger = logging.getLogger(__name__)


class RegionReporter(object):
    def __init__(self, region):
        self.region = region


class YamlReport(object):
    def show(self, worlds):
        logger.debug("Start Yaml Report")

        for world in worlds:
            logger.debug("World %s", world)
            logger.debug("File Types %s", len(worlds[world].files))
            # logger.debug("File Types %s", len(worlds[world].files))

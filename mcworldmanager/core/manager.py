import logging
import os
from multiprocessing import JoinableQueue
from multiprocessing.pool import ThreadPool as Pool

import progressbar

from mcworldmanager.core import models
from mcworldmanager.core.analysers import MCDataFileAnalyser, MCRegionFileAnalyser

logger = logging.getLogger(__name__)


class Manager(object):
    def __init__(self, worlds, options):
        self.worlds = worlds
        self.import_options = options
        self.multiprocess_manager = self.MultiProcessManager(self)
        self.scannd_results = []
        self.scanned_file_count = 0

    class WorldFileTask(object):
        def __init__(self, world, mcFile):
            self.file = mcFile
            self.world = world

    def start(self):
        tasks = []
        for world in self.worlds:
            files = self.worlds[world].files.all()
            for mcFile in files:
                tasks.append(self.WorldFileTask(world, mcFile))

        logger.debug("Prepare queue with Scanning Tasks %s", len(tasks))
        # self.progress = progressbar.ProgressBar(min_val=1, max_val=len(tasks))
        self.progress = progressbar.ProgressBar(
            # widgets=[progressbar.SimpleProgress()],
            widgets=[
                progressbar.AnimatedMarker(),
                "  ",
                progressbar.FormatLabel("Processed: %(value)d of: %(max_value)d "),
                "Percent: ",
                progressbar.Percentage(),
                "  ",
                progressbar.ETA(),
                " ",
                progressbar.Bar(">"),
            ],
            redirect_stdout=True,
            max_value=len(tasks),
        ).start()
        self.multiprocess_manager.append_tasks(tasks)
        self.multiprocess_manager.queue.join()
        self.progress.finish()
        logger.debug("Finished %s", len(tasks))

        for task in self.scannd_results:
            logger.debug("Scanned %s", task.scanned)

    class MultiProcessManager(object):
        def __init__(self, manager):
            self.manager = manager
            self.dataFileAnalyser = MCDataFileAnalyser()
            self.regionFileAnalyser = MCRegionFileAnalyser(manager.import_options)
            self.queue = JoinableQueue()
            self.pool = Pool(manager.import_options["multiprocess"]["pool_size"], self.task_worker, (self.queue,))

        def task_worker(self, queue):
            logger.debug("Start Worker PID: %i", os.getpid())
            while True:
                item = queue.get(True)
                logger.debug("receive working task %s type %i", item.file.filename, item.file.type)
                try:
                    if item.file.type == models.MC_FILE_TYPE_REGION:
                        analyed = self.regionFileAnalyser.analyse(item.file)
                        self.manager.worlds[item.world].files[models.MC_FILE_TYPE_REGION][item.file.dimension_tag][
                            item.file.filename
                        ] = analyed
                    if item.file.type == models.MC_FILE_TYPE_DATA:
                        analyed = self.dataFileAnalyser.analyse(item.file)
                        self.manager.worlds[item.world].files[models.MC_FILE_TYPE_DATA][item.file.filename] = analyed
                except Exception:
                    logger.debug("fail to analse %s", item.file.filename)

                self.manager.scanned_file_count = self.manager.scanned_file_count + 1
                self.manager.progress.update(self.manager.scanned_file_count)
                queue.task_done()

        def append_tasks(self, tasks):
            logger.debug("Adding %s Tasks to queue for Scanning", len(tasks))
            for task in tasks:
                self.queue.put(task)

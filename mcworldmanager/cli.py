# -*- coding: utf-8 -*-

"""Main `mcworldmanager` CLI."""

import logging
import sys

import click

from mcworldmanager import __version__
from mcworldmanager.core import reportmarkdown
from mcworldmanager.core.analysers import MCRegionFileAnalyser, MCRegionFileAnalyserConfig
from mcworldmanager.core.manager import Manager, ScanningConfig
from mcworldmanager.core.models import MCRegionFile, MCWorlds
from mcworldmanager.log import configure_logger

logger = logging.getLogger(__name__)


@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Print debug information", default=False)
@click.option(u"--debug-file", type=click.Path(), default=None, help=u"File to be used as a stream for DEBUG logging")
def main(verbose, debug_file):
    """Console script for mcworldmanager."""
    configure_logger(stream_level="DEBUG" if verbose else "INFO", debug_file=debug_file)


@main.command(help="Display the current version.")
def version():
    """Display the current version."""
    click.echo(__version__)


@main.command(help="Analyse a single minecraft region file lile r.-1.-2.mca")
@click.argument("region_file_path", nargs=1, type=click.Path())
def region(region_file_path):
    click.echo("Analyse Single Region file")
    analyser = MCRegionFileAnalyser(MCRegionFileAnalyserConfig(-1))
    mcRegion = MCRegionFile(region_file_path)
    analyser.analyse(mcRegion)
    report = reportmarkdown.RegionReporter(mcRegion).report("")
    print(report)

    if mcRegion.isManuelCheckRequired():
        sys.exit(1)
    else:
        sys.exit(0)


@main.command(help="Analyse a List of World Directories", context_settings={"ignore_unknown_options": True})
@click.argument("worlds_directories", nargs=-1, type=click.Path())
def worlds(worlds_directories):
    options = ScanningConfig(2)
    options.analyse_config = MCRegionFileAnalyserConfig(-1)
    click.echo("start scanning")
    worlds = MCWorlds(worlds_directories)
    manager = Manager(worlds, options)
    manager.start()
    report = reportmarkdown.WorldsReporter(worlds).report("")
    print(report)

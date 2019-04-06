# -*- coding: utf-8 -*-

"""Main `mcworldmanager` CLI."""

import logging
import os
import sys

import anyconfig
import click

from mcworldmanager import __version__
from mcworldmanager.core.analysers import MCRegionFileAnalyser
from mcworldmanager.core.manager import Manager
from mcworldmanager.core.models import MCRegionFile, MCWorlds
from mcworldmanager.log import configure_logger
from mcworldmanager.report import report_manager

logger = logging.getLogger(__name__)


@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Print debug information", default=False)
@click.option("-o", "--output_format", type=click.Choice(report_manager.OUTPUT_FORMATS), required=False)
@click.option(u"--debug-file", type=click.Path(), default=None, help=u"File to be used as a stream for DEBUG logging")
@click.pass_context
def main(ctx, verbose, output_format, debug_file):
    """Console script for mcworldmanager."""
    configure_logger(stream_level="DEBUG" if verbose else "INFO", debug_file=debug_file)

    # ensure that ctx.obj exists and is a dict (in case `cli()` is called
    # by means other than the `if` block below
    ctx.ensure_object(dict)
    ctx.obj["config"] = anyconfig.load(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "./defaults-config.yml")
    )
    if output_format:
        ctx.obj["config"]["report"]["format"] = output_format


@main.command(help="Display the current version.")
@click.pass_context
def version(ctx):
    """Display the current version."""
    click.echo(__version__)


@main.command(help="Analyse a single minecraft region file lile r.-1.-2.mca")
@click.argument("region_file_path", nargs=1, type=click.Path())
@click.pass_context
def region(ctx, region_file_path):
    click.echo("Analyse Single Region file")
    config = ctx.obj["config"]
    analyser = MCRegionFileAnalyser(config)
    mcRegion = MCRegionFile(region_file_path)
    analyser.analyse(mcRegion)
    report_manager.createReport(config, mcRegion)
    # report = reportmarkdown.RegionReporter(mcRegion).report("")
    # print(report)

    if mcRegion.isManuelCheckRequired():
        sys.exit(1)
    else:
        sys.exit(0)


@main.command(help="Analyse a List of World Directories", context_settings={"ignore_unknown_options": True})
@click.argument("worlds_directories", nargs=-1, type=click.Path())
@click.pass_context
def worlds(ctx, worlds_directories):
    click.echo("start scanning")
    worlds = MCWorlds(worlds_directories)
    config = ctx.obj["config"]
    manager = Manager(worlds, config)
    manager.start()
    report_manager.createReport(config, worlds)
    # report = reportmarkdown.WorldsReporter(worlds).report("")
    # print(report)

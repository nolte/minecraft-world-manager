# -*- coding: utf-8 -*-

"""Main `mcworldmanager` CLI."""

import logging
import os
import sys

import anyconfig
import click
from pyfiglet import Figlet

from mcworldmanager import __version__
from mcworldmanager.core.analysers import MCRegionFileAnalyser
from mcworldmanager.core.manager import Manager
from mcworldmanager.core.models import MCRegionFile, MCWorlds
from mcworldmanager.log import configure_logger
from mcworldmanager.report import report_manager

logger = logging.getLogger(__name__)


@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Print debug information", default=False)
@click.option(
    "-o",
    "--output_format",
    type=click.Choice(report_manager.OUTPUT_FORMATS),
    help="Define the STDout Output format",
    default=None,
)
@click.option("-r", "--report_path", type=click.Path(), help="Path for the Report in Yaml Format", default=None)
@click.option(u"--debug-file", type=click.Path(), default=None, help=u"File to be used as a stream for DEBUG logging")
@click.pass_context
def main(ctx, verbose, output_format, report_path, debug_file):
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
    if report_path:
        ctx.obj["config"]["report"]["path"] = report_path


@main.command(help="Display the current version.")
@click.pass_context
def version(ctx):
    """Display the current version."""

    f = Figlet(font="slant")
    click.echo(f.renderText("Minecraft World Manager"))
    click.echo(__version__)


@main.command(help="Analyse a single minecraft region file like r.-1.-2.mca")
@click.argument("region_file_path", nargs=1, type=click.Path())
@click.pass_context
def region(ctx, region_file_path):
    """ Scanning a Region file and create a Report"""
    click.echo("Analyse Single Region file")
    config = ctx.obj["config"]
    analyser = MCRegionFileAnalyser(config)
    mcRegion = MCRegionFile(region_file_path)
    analyser.analyse(mcRegion)
    report_manager.createReport(config, mcRegion)

    if mcRegion.isManuelCheckRequired():
        sys.exit(1)
    else:
        sys.exit(0)


@main.command(help="Analyse a List of World Directories", context_settings={"ignore_unknown_options": True})
@click.argument("worlds_directories", nargs=-1, type=click.Path())
@click.pass_context
def worlds(ctx, worlds_directories):
    """Scanning a list of Worlds, and create a Report"""
    click.echo("start scanning")
    worlds = MCWorlds(list(worlds_directories))
    config = ctx.obj["config"]
    manager = Manager(worlds, config)
    manager.start()
    report_manager.createReport(config, worlds)


@main.command(help="Analyse a all Worlds in a Server Directories")
@click.argument("server_directory", type=click.Path(), required=True)
@click.pass_context
def server(ctx, server_directory):
    click.echo("start scanning")
    worlds_directories = []
    for server_dir in next(os.walk(server_directory))[1]:
        if server_dir.startswith("world"):
            worlds_directories.append(os.path.join(server_directory, server_dir))

    worlds = MCWorlds(worlds_directories)
    config = ctx.obj["config"]
    manager = Manager(worlds, config)
    manager.start()
    report_manager.createReport(config, worlds)

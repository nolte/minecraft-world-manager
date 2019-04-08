# Minecraft World Checker

[![Github Project Stars](https://img.shields.io/github/stars/nolte/minecraft-world-manager.svg?label=Stars&style=social)](https://github.com/nolte/minecraft-world-manager) [![Travis CI build status](https://travis-ci.org/nolte/minecraft-world-manager.svg?branch=master)](https://travis-ci.org/nolte/minecraft-world-manager) [![CircleCI build status](https://circleci.com/gh/nolte/minecraft-world-manager.svg?style=svg)](https://circleci.com/gh/nolte/minecraft-world-manager) [![Documentation Status](https://readthedocs.org/projects/minecraft-world-manager/badge/?version=latest)](https://minecraft-world-manager.readthedocs.io/en/stable/?badge=stable) [![Github Issue Tracking](https://img.shields.io/github/issues-raw/nolte/minecraft-world-manager.svg)](https://github.com/nolte/minecraft-world-manager) [![Github LatestRelease](https://img.shields.io/github/release/nolte/minecraft-world-manager.svg)](https://github.com/nolte/minecraft-world-manager) [![CodeFactor](https://www.codefactor.io/repository/github/nolte/minecraft-world-manager/badge)](https://www.codefactor.io/repository/github/nolte/minecraft-world-manager) [![microbadger image](https://images.microbadger.com/badges/image/nolte/minecraft-world-manager.svg)](https://microbadger.com/images/nolte/minecraft-world-manager) [![version](https://images.microbadger.com/badges/version/nolte/minecraft-world-manager.svg)](https://microbadger.com/images/nolte/minecraft-world-manager) [![docker stars](https://img.shields.io/docker/stars/nolte/minecraft-world-manager.svg?style=flat)](https://hub.docker.com/r/nolte/minecraft-world-manager) [![docker pulls](https://img.shields.io/docker/pulls/nolte/minecraft-world-manager.svg?style=flat)](https://hub.docker.com/r/nolte/minecraft-world-manager) [![pypi.org version](https://img.shields.io/pypi/v/mcworldmanager.svg?style=flat)](https://pypi.org/project/mcworldmanager)

A Small Tool for rescue and maintenance your Minecraft Worlds, insperated by [Fenixin/Minecraft-Region-Fixer](https://github.com/Fenixin/Minecraft-Region-Fixer), optimized for commandline usage, and integration into a Backup and Recovery Process.
Using [twoolie/NBT](https://github.com/twoolie/NBT) a Python Parser/Writer for the [NBT](https://minecraft.gamepedia.com/NBT_format) file format, for reading and fixing the World Data Files.

For more informations take a look to the [Documentation](https://nolte.github.io/minecraft-world-manager/).

## Features

- Scanning Region Files, for to many Entities, corrupted or wrong located Chunks. (*repairing planed*)
- Saving the Report as `YAML`, for later usage.
- Different commandline output formats.
  - `YAML`, for Script usage.
  - `COMMANDLINE`, as Human readable commandline Report.
- Configurable over Command Line Parameters (using [click](https://click.palletsprojects.com/en/7.x/)), or Config File (using [anyconfig](https://python-anyconfig.readthedocs.io/en/latest/))(*planed*).

## Supported Systems

For executing you need Python 3.5 or later, or you use the Preconfigured Docker Container from [DockerHub](https://hub.docker.com/r/nolte/minecraft-world-manager).
Tested with a Minecraft *1.13.2* World.

### Using as Python CLI

This Tool are published at [pypi.org](https://pypi.org/project/mcworldmanager/), and be install with [pip](https://packaging.python.org/tutorials/installing-packages/#installing-from-pypi). It is recommendet to use a [virtualenv](https://virtualenv.pypa.io/en/latest/) to avoid any Dependency correlations.

```bash
pip install mcworldmanager
```

### Using as Container

The Container is based on [python:3.7-alpine](https://hub.docker.com/_/python?tab=description), and automatical build on [DockerHub](https://hub.docker.com/r/nolte/minecraft-world-manager/builds).

```bash
docker run -it \
  --user=${UID}:$(id -g $(whoami)) \
  -w /tmp/worlds \
  -v /tmp/worlds:/tmp/worlds \
  nolte/minecraft-world-manager:latest -v worlds /tmp/worlds
```
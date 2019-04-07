# Minecraft World Checker

[![Github Project Stars](https://img.shields.io/github/stars/nolte/minecraft-world-manager.svg?label=Stars&style=social)](https://github.com/nolte/minecraft-world-manager) [![Travis CI build status](https://travis-ci.org/nolte/minecraft-world-manager.svg?branch=master)](https://travis-ci.org/nolte/minecraft-world-manager) [![CircleCI build status](https://circleci.com/gh/nolte/minecraft-world-manager.svg?style=svg)](https://circleci.com/gh/nolte/minecraft-world-manager) [![Documentation Status](https://readthedocs.org/projects/minecraft-world-manager/badge/?version=latest)](https://minecraft-world-manager.readthedocs.io/en/stable/?badge=stable) [![Github Issue Tracking](https://img.shields.io/github/issues-raw/nolte/minecraft-world-manager.svg)](https://github.com/nolte/minecraft-world-manager) [![Github LatestRelease](https://img.shields.io/github/release/nolte/minecraft-world-manager.svg)](https://github.com/nolte/minecraft-world-manager) [![CodeFactor](https://www.codefactor.io/repository/github/nolte/minecraft-world-manager/badge)](https://www.codefactor.io/repository/github/nolte/minecraft-world-manager) [![microbadger image](https://images.microbadger.com/badges/image/nolte/minecraft-world-manager.svg)](https://microbadger.com/images/nolte/minecraft-world-manager) [![version](https://images.microbadger.com/badges/version/nolte/minecraft-world-manager.svg)](https://microbadger.com/images/nolte/minecraft-world-manager) [![docker stars](https://img.shields.io/docker/stars/nolte/minecraft-world-manager.svg?style=flat)](https://hub.docker.com/r/nolte/minecraft-world-manager) [![docker pulls](https://img.shields.io/docker/pulls/nolte/minecraft-world-manager.svg?style=flat)](https://hub.docker.com/r/nolte/minecraft-world-manager) [![pypi.org version](https://img.shields.io/pypi/v/mcworldmanager.svg?style=flat)](https://pypi.org/project/mcworldmanager)

Insperated by [Fenixin/Minecraft-Region-Fixer](https://github.com/Fenixin/Minecraft-Region-Fixer), but a optimized commandline usage, and integration to your backup Process.

For more informations take a look to the [Documentation](https://nolte.github.io/minecraft-world-manager/).

## Features

- Scanning a single Region File
- Scanning a list of given Worlds
- Scanning all World Folders from a Minecraft Server Structure
- Saving the Report as yaml File

## Supported Systems

For executing you need Python 3.5 or later, or you use the Preconfigured Docker Container from [DockerHub](https://hub.docker.com/r/nolte/minecraft-world-manager).

## Example Calls

```bash
mcworldmanager server ~/repos-ansible/minecraft-server-project-repos/docker_compose-world-maps/worldfolder/world
```

```bash
mcworldmanager worlds ~/repos-ansible/minecraft-server-project-repos/docker_compose-world-maps/worldfolder/world
```

```bash
mcworldmanager region ~/repos-ansible/minecraft-server-project-repos/docker_compose-world-maps/worldfolder/world_flat/region/r.1.1.mca
```

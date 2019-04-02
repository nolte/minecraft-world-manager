Container Usage
=================================================


For easy and quickly usage you can use the Dockerfile from `Dockerhub <https://hub.docker.com/r/nolte/minecraft-world-manager>`_.

.. code:: bash

    docker pull nolte/minecraft-world-manager:latest

For wrapping the tool, and checkout to your local FS it is required that you define some additional :ref:`usage-container-run-parameters`.

.. literalinclude:: docker_call.txt
   :language: bash
   :caption: execute world check
   :name: minecraft-world-manager-command


.. _usage-container-run-parameters:


Container Run Parameters
--------------------------------------------------

``--user ${UID}:$(id -g $(whoami))``
    The Container User will mapped to your user and group from the Host System, see `User <https://docs.docker.com/engine/reference/run/#user>`_.

``-w /tmp/worlds``
  The Container `Workingdir <https://docs.docker.com/engine/reference/run/#workdir>`_.

``-v /tmp/worlds:/tmp/worlds``
  Some Folder mounted to your Host System, used as scanning base folder.

``[mcworldmanager command]``
  Using the :ref:`cli-parameters` commandline parameters.

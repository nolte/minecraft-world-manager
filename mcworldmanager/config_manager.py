import anyconfig
import os


def configure_conf():
    conf = anyconfig.load(os.path.join(os.path.dirname(os.path.abspath(__file__)),"./defaults-config.yml"))
    return conf
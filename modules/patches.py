from modules.basemodule import Basemodule
from pathlib import Path
import os
import shutil


config = {
    "service": 1,
    "username": "ITotalJustice",
    "reponame": "patches",
    "assetRegex": ".*hekate.*\\.zip",
}

class patches(Basemodule):
    def __init__(self, config):
        Basemodule.__init__(self, config)

package = patches(config)
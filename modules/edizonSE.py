from modules.basemodule import Basemodule
from pathlib import Path
import os
import shutil


config = {
    "service": 1,
    "username": "tomvita",
    "reponame": "EdiZon-SE",
    "assetRegex": ".*EdiZon.*\\.zip",
}

class EdizonSE(Basemodule):
    def __init__(self, config):
        Basemodule.__init__(self, config)

package = EdizonSE(config)
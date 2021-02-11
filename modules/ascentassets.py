from modules.basemodule import Basemodule
from pathlib import Path
import json, os


config = {
    "service": 1,
    "username": "exploitz86",
    "reponame": "Ascent-Assets",
    "assetRegex": ".*\\.zip"
}

class AscentAssets(Basemodule):
    def __init__(self, config):
        Basemodule.__init__(self, config)

    def handleModule(self):
        release = self.getLatestRelease()
        assetName = self.downloadAsset(release)
        extracted = self.unpackAsset(assetName)
        self.copyFolderContentToPackage(extracted)


package = AscentAssets(config)
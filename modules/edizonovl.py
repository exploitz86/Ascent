from modules.basemodule import Basemodule
from pathlib import Path
import os
import shutil


config = {
    "service": 1,
    "username": "WerWolv",
    "reponame": "EdiZon",
    "assetRegex": ".*ovlEdiZon.*\\.ovl",
}

def moveovl(workpath, assetName):
    Path(Path.joinpath(workpath, "switch", ".overlays")).mkdir(parents=True, exist_ok=True)
    shutil.move(Path.joinpath(workpath, assetName), Path.joinpath(workpath, "switch", ".overlays", assetName))

class Edizonovl(Basemodule):
    def __init__(self, config):
        Basemodule.__init__(self, config)
    
    def handleModule(self):
        release = self.getLatestRelease()
        assetName = self.downloadAsset(release)
        moveovl(self.workspaceFullPath, assetName)
        self.copyFolderContentToPackage(self.workspaceFullPath)

package = Edizonovl(config)
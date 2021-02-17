from modules.basemodule import Basemodule
from pathlib import Path
import os
import shutil


config = {
    "service": 1,
    "username": "XorTroll",
    "reponame": "Goldleaf",
    "assetRegex": ".*Goldleaf.*\\.nro",
}

def GoldleafPath(workpath, assetName):
    Path(Path.joinpath(workpath, "switch", "Goldleaf")).mkdir(parents=True, exist_ok=True)
    shutil.move(Path.joinpath(workpath, assetName), Path.joinpath(workpath, "switch", "Goldleaf", assetName))

class Goldleaf(Basemodule):
    def __init__(self, config):
        Basemodule.__init__(self, config)
    
    def handleModule(self):
        release = self.getLatestRelease()
        assetName = self.downloadAsset(release)
        GoldleafPath(self.workspaceFullPath, assetName)
        self.copyFolderContentToPackage(self.workspaceFullPath)

package = Goldleaf(config)
from modules.basemodule import Basemodule
from pathlib import Path
import shutil

config = {
    "service": 1,
    "username": "exploitz86",
    "reponame": "Ascent-Toolbox",
    "assetRegex": ".*\\.nro"
}

def modifyFiles(workpath, assetName):
    Path(Path.joinpath(workpath, "switch", "Ascent-Toolbox")).mkdir(parents=True, exist_ok=True)
    shutil.move(Path.joinpath(workpath, assetName), Path.joinpath(workpath, "switch", "Ascent-Toolbox", assetName))


class Ascenttoolbox(Basemodule):
    def __init__(self, config):
        Basemodule.__init__(self, config)

    def handleModule(self):
        release = self.getLatestRelease()
        assetName = self.downloadAsset(release)
        #extracted = self.unpackAsset(assetName)
        modifyFiles(self.workspaceFullPath, assetName)
        self.copyFolderContentToPackage(self.workspaceFullPath)

package = Ascenttoolbox(config)
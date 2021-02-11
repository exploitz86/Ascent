from modules.basemodule import Basemodule
from pathlib import Path
import shutil
import json

config = {
    "service": 1,
    "username": "exploitz86",
    "reponame": "Ascent-Updater",
    "assetRegex": ".*\\.nro",
    "assetPatterns": [".*\\.nro", ".*\\.db"]
}

def createStructure(workpath, assetNames):
    Path(Path.joinpath(workpath, "switch", "Ascent-Updater")).mkdir(parents=True, exist_ok=True)
    for i in assetNames:
        if i.endswith(".nro"):
            shutil.move(Path.joinpath(workpath, i), Path.joinpath(workpath, "switch", "Ascent-Updater", i))
        if i.endswith(".db"):
            internaldb = Path.joinpath(workpath, i)
            ver = json.loads(open("./VERSION").read())
            with open(internaldb, 'r') as file:
                data = file.read()
                data = data.replace('ASCENT_VERSION', ver["buildVersion"])
                data = data.replace('MESOOPT', "true")
            with open(internaldb, 'w') as file:
                file.write(data)
            shutil.move(Path.joinpath(workpath, i), Path.joinpath(workpath, "switch", "Ascent-Updater", i))


class Ascentupdater(Basemodule):
    def __init__(self, config):
        Basemodule.__init__(self, config)

    def handleModule(self):
        release = self.getLatestRelease()
        assetNames = self.downloadAssets(release)
        #extracted = self.unpackAsset(assetName)
        createStructure(self.workspaceFullPath, assetNames)
        self.copyFolderContentToPackage(self.workspaceFullPath)

package = Ascentupdater(config)
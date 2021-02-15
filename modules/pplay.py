from modules.basemodule import Basemodule
from pathlib import Path

config = {
    "service": 1,
    "username": "Cpasjuste",
    "reponame": "pplay",
    "assetRegex": ".*pplay.*\\.zip"
}


class pplay(Basemodule):
    def __init__(self, config):
        Basemodule.__init__(self, config)
    
    def handleModule(self):
        release = self.getLatestRelease()
        assetName = self.downloadAsset(release)
        extracted = self.unpackAsset(assetName)
        self.copyFolderContentToPackage(extracted, (Path.cwd(), "switch_out", "switch"))

package = pplay(config)
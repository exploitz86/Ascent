from modules.basemodule import Basemodule
from pathlib import Path
import configparser
import os, shutil
parser = configparser.ConfigParser()

config = {
    "service": 1,
    "username": "Atmosphere-NX",
    "reponame": "Atmosphere",
    "assetRegex": ".*WITHOUT_MESOSPHERE.*\\.zip",
    "assetPatterns": [".*WITHOUT_MESOSPHERE.*\\.zip", ".*fusee-primary.*\\.bin"]
}

def copyFusee(workpath):
    Path(Path.joinpath(Path.cwd(), "switch_out", "bootloader", "payloads")).mkdir(parents=True, exist_ok=True)
    shutil.move(Path.joinpath(workpath, "fusee-primary.bin"), Path.joinpath(Path.cwd(), "switch_out", "bootloader", "payloads", "fusee-primary.bin"))

def editSystemSettings(extracted):
    settings = Path.joinpath(extracted, "atmosphere", "config_templates", "system_settings.ini")
    settings_out = Path.joinpath(extracted, "atmosphere", "config", "system_settings.ini")

    with open(settings, 'r') as file:
        data = file.read()
        data = data.replace('; dmnt_cheats_enabled_by_default = u8!0x1', 'dmnt_cheats_enabled_by_default = u8!0x0')

    with open(settings_out, 'wb') as outp:
        outp.write(data.encode())

def removeRebootToPayload(extracted):
    os.remove(Path.joinpath(extracted, "switch", "reboot_to_payload.nro"))

class Atmosphere(Basemodule):
    def __init__(self, config):
        Basemodule.__init__(self, config)

    def handleModule(self):
        release = self.getLatestRelease()
        assetNames = self.downloadAssets(release)
        copyFusee(self.workspaceFullPath)
        for i in assetNames:
            if i.endswith(".zip"):
                extracted = self.unpackAsset(i)
        editSystemSettings(extracted)
        removeRebootToPayload(extracted)
        self.copyFolderContentToPackage(extracted)

package = Atmosphere(config)


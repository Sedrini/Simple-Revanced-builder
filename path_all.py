from pathlib import Path
import os 


def paths():
    revanced_folder = Path(os.environ["USERPROFILE"]) / "Documents" / "Simple Revanced"
    tools_folder = revanced_folder / "Tools"
    patched_folder = revanced_folder/ "Patched APK"
    folders = [revanced_folder,tools_folder,patched_folder]
    return folders
import sys
from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need fine tuning.
# "packages": ["os"] is used as example only
build_exe_options = dict(include_files = ["IMG/", "Saves/"])


# base="Win32GUI" should be used only for Windows GUI app
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name = "PPD Mover",
    description = "An app to help move files for using PPD",
    options = {
        "build_exe": build_exe_options, 
        },
    executables = [Executable("PPDmover_HatsuneMikuStyle.py", base=base)]
)
import os

START_MENU_PATHS = [
    r"C:\ProgramData\Microsoft\Windows\Start Menu\Programs",
    os.path.expandvars(r"%APPDATA%\Microsoft\Windows\Start Menu\Programs")
]


def scan_installed_apps():

    apps = {}

    for base_path in START_MENU_PATHS:

        for root, dirs, files in os.walk(base_path):

            for file in files:

                if file.endswith(".lnk"):

                    name = file.replace(".lnk", "").lower()
                    full_path = os.path.join(root, file)

                    apps[name] = full_path

    return apps
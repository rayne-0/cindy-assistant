import win32com.client

APP_REGISTRY = {}


def load_apps():

    global APP_REGISTRY

    if APP_REGISTRY:
        return APP_REGISTRY

    shell = win32com.client.Dispatch("Shell.Application")

    apps_folder = shell.Namespace("shell:AppsFolder")

    apps = {}

    for item in apps_folder.Items():

        name = item.Name.lower()

        try:
            app_id = item.Path
        except:
            continue

        apps[name] = app_id

    APP_REGISTRY = apps

    return apps
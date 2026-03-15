import os
import datetime


def shutdown_pc():
    os.system("shutdown /s /t 1")


def restart_pc():
    os.system("shutdown /r /t 1")


def get_time():
    now = datetime.datetime.now()
    return now.strftime("Current time: %H:%M")
import subprocess
from utils.constants import CHROME_PATH


def open_chrome():
    subprocess.Popen(CHROME_PATH)
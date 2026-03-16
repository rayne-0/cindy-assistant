import psutil
import os
import shutil
import getpass

def speed_up_system() -> str:
    """
    Terminates high-memory, non-essential background processes and clears Windows Temp caches
    to free up system resources.
    """
    freed_memory_mb = 0
    apps_closed = 0
    
    # Target applications that run heavily in the background
    target_processes = ['Discord.exe', 'Spotify.exe', 'Steam.exe', 'EpicGamesLauncher.exe', 'msedge.exe']
    
    # 1. Kill Target Apps
    for proc in psutil.process_iter(['name', 'memory_info']):
        try:
            if proc.info['name'] in target_processes:
                # Add up memory before killing
                mem = proc.info['memory_info'].rss / (1024 * 1024)
                freed_memory_mb += mem
                
                # Terminate
                proc.kill()
                apps_closed += 1
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass

    # 2. Clean Temporary Files
    temp_dirs = [
        r"C:\Windows\Temp",
        os.path.join(r"C:\Users", getpass.getuser(), r"AppData\Local\Temp")
    ]
    
    files_deleted = 0
    for tdir in temp_dirs:
        if os.path.exists(tdir):
            try:
                for filename in os.listdir(tdir):
                    file_path = os.path.join(tdir, filename)
                    try:
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                        files_deleted += 1
                    except Exception:
                        # Ignore files currently in use
                        pass
            except PermissionError:
                pass

    return f"System configured. Closed {apps_closed} background tasks, freeing {int(freed_memory_mb)}MB. Cleared {files_deleted} temporary files."

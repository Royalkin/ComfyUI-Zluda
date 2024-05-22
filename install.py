import os
import subprocess
import sys
import shutil
import time
from tqdm import tqdm
import itertools
import threading

def install_libraries():
    try:
        import tqdm
    except ImportError:
        print("tqdm not found. Installing tqdm...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "tqdm"])
    try:
        import winshell
    except ImportError:
        print("winshell not found. Installing winshell...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "winshell"])
    try:
        import win32com.client
    except ImportError:
        print("pywin32 not found. Installing pywin32...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pywin32"])
        import site
        site_packages = site.getsitepackages()[0]
        pywin32_postinstall = os.path.join(site_packages, 'pywin32_system32', 'pywin32_postinstall.py')
        subprocess.check_call([sys.executable, pywin32_postinstall, '-install'])

install_libraries()
from tqdm import tqdm
import winshell
import pythoncom
from win32com.client import Dispatch

def run_with_progress(command, description):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    with tqdm(total=100, desc=description, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]') as pbar:
        while process.poll() is None:
            pbar.update(10)
            time.sleep(1)
        pbar.update(100 - pbar.n)
    print("\nDone.")

def spinner():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rInstalling requirements... ' + c)
        sys.stdout.flush()
        time.sleep(0.1)

def create_shortcut(target, shortcut_path, icon_path, description):
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = target
    shortcut.WorkingDirectory = os.path.dirname(target)
    shortcut.IconLocation = icon_path
    shortcut.Description = description
    shortcut.save()

def main():
    global done
    done = False

    # Assume the install directory is the root directory where this script is located
    install_dir = os.path.dirname(os.path.abspath(__file__))
    venv_dir = os.path.join(install_dir, ".venv")

    # Step 1: CD into the install directory
    os.chdir(install_dir)
    print("\n")

    # Step 2: Create a virtual environment with Python 3.11
    print("Creating a virtual environment...")
    run_with_progress([sys.executable, "-m", "venv", venv_dir], "Creating venv")
    print("\n")

    # Detect if running in PowerShell or Command Prompt
    is_powershell = 'powershell' in os.environ.get('SHELL', '').lower() or 'pwsh' in os.environ.get('SHELL', '').lower()
    
    # Step 3: Install requirements.txt with pip
    if os.name == 'nt':
        activate_script = os.path.join(venv_dir, 'Scripts', 'activate')
        if is_powershell:
            activate_command = f"& '{activate_script}'"
        else:
            activate_command = f'cmd /c "{activate_script} && '
    else:
        activate_script = os.path.join(venv_dir, 'bin', 'activate')
        activate_command = f'source {activate_script} && '
        
    install_command = f'{activate_command}pip install -r requirements.txt'

    # Use spinner for indefinite process
    print("Installing requirements from requirements.txt. This might take a while, please be patient.")
    spinner_thread = threading.Thread(target=spinner)
    spinner_thread.start()

    subprocess.run(install_command, shell=True, check=True)

    done = True
    spinner_thread.join()
    print("\nDone.\n")

    # Step 4: Prompt if the user wants to create the bat file and add a shortcut
    create_shortcut_prompt = input("Do you want to create a batch file to run ComfyUI? (Y/n): ").strip().lower()
    if create_shortcut_prompt in ['', 'y', 'yes']:
        print("\n")
        # Step 5: Prompt for command line arguments
        print("Please refer to the command_line_arguments.md file in the comfyui directory for more information on available command line arguments.")
        cmd_args = input("Enter any command line arguments you wish to use (e.g., --auto-launch --lowvram): ").strip()

        # Step 6: Create bat file
        bat_file_path = os.path.join(install_dir, "run_comfyui.bat")
        with open(bat_file_path, 'w') as bat_file:
            bat_file.write(f'{activate_command}python main.py {cmd_args}\n')

        print("A bat file was created with your command line arguments in the install directory.")

        # Step 7: Create desktop shortcut with custom icon
        desktop = winshell.desktop()
        shortcut_path = os.path.join(desktop, "ComfyUI.lnk")
        icon_path = os.path.join(install_dir, "comfy_zluda_icon.ico")
        create_shortcut(bat_file_path, shortcut_path, icon_path, "Shortcut to run ComfyUI")
        print("A shortcut to the batch file was added to your desktop with a custom icon.")
    else:
        bat_file_path = None
    print("\n")

    # Step 8: Copy renamed DLL files from ZLUDA
    zluda_dir = os.path.join(install_dir, 'zluda', 'renamed_dlls')
    torch_lib_dir = os.path.join(venv_dir, 'Lib', 'site-packages', 'torch', 'lib')

    if not os.path.exists(zluda_dir):
        print(f"Error: ZLUDA directory {zluda_dir} does not exist.")
        return

    print("Copying renamed DLL files from ZLUDA...")
    dll_files = ['cublas64_11.dll', 'cusparse64_11.dll']
    with tqdm(total=len(dll_files), desc="Copying DLL files", bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]') as pbar:
        for dll in dll_files:
            src_path = os.path.join(zluda_dir, dll)
            dest_path = os.path.join(torch_lib_dir, dll)
            if os.path.exists(src_path):
                shutil.copy2(src_path, dest_path)
                print(f"Copied {dll} to {dest_path}")
            else:
                print(f"Error: {src_path} does not exist.")
            pbar.update(1)
    print("\n")

    # Final instructions
    print("\nComfyUI installation is complete.")
    if bat_file_path:
        print(f'To activate the virtual environment in the future, run:\n   {os.path.join(venv_dir, "Scripts", "activate.bat")}\n')
        print(f'To run ComfyUI with your specified command line arguments, use the batch file:\n   {bat_file_path}')

if __name__ == "__main__":
    main()

import os
import subprocess
import sys
import shutil
import time
from tqdm import tqdm

def run_with_progress(command, description):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    with tqdm(total=100, desc=description, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]') as pbar:
        while process.poll() is None:
            pbar.update(10)
            time.sleep(1)
        pbar.update(100 - pbar.n)
    print("Done.")

def main():
    # Assume the install directory is the root directory where this script is located
    install_dir = os.path.dirname(os.path.abspath(__file__))
    venv_dir = os.path.join(install_dir, ".venv")

    # Step 1: CD into the install directory
    os.chdir(install_dir)

    # Step 2: Create a virtual environment with Python 3.11
    print("Creating a virtual environment...")
    run_with_progress([sys.executable, "-m", "venv", venv_dir], "Creating venv")

    # Detect if running in PowerShell or Command Prompt
    is_powershell = 'powershell' in os.environ.get('SHELL', '').lower() or 'pwsh' in os.environ.get('SHELL', '').lower()
    
    # Step 3: Install requirements.txt with pip
    print("Installing requirements from requirements.txt. This might take a while, please be patient.")
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
    run_with_progress(install_command, "Installing requirements")

    # Step 4: Prompt if the user wants to create the bat file and add a shortcut
    create_shortcut_prompt = input("Do you want to create a batch file to run ComfyUI? (yes/no): ").strip().lower()
    if create_shortcut_prompt == 'yes':
        # Step 5: Prompt for command line arguments
        print("Please refer to the command_line_arguments.md file in the comfyui directory for more information on available command line arguments.")
        cmd_args = input("Enter any command line arguments you wish to use (e.g., --auto-launch --lowvram): ").strip()

        # Step 6: Create bat file
        bat_file_path = os.path.join(install_dir, "run_comfyui.bat")
        with open(bat_file_path, 'w') as bat_file:
            bat_file.write(f'{activate_command}python main.py {cmd_args}\n')

        print("A bat file was created with your command line arguments in the install directory.")
    else:
        bat_file_path = None

    # Step 7: Copy renamed DLL files from ZLUDA
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

    # Final instructions
    print("\nComfyUI installation is complete.")
    if bat_file_path:
        print(f'To activate the virtual environment in the future, run:\n   {os.path.join(venv_dir, "Scripts", "activate.bat")}\n')
        print(f'To run ComfyUI with your specified command line arguments, use the batch file:\n   {bat_file_path}')

if __name__ == "__main__":
    main()

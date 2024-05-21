import os
import subprocess
import sys
import shutil
import time
import pythoncom
import win32com.client

def run_with_progress(command, description):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    while process.poll() is None:
        sys.stdout.write('.')
        sys.stdout.flush()
        time.sleep(1)
    print("Done.")

def create_shortcut(target, shortcut_path, description):
    shell = win32com.client.Dispatch("WScript.Shell")
    shortcut = shell.CreateShortCut(shortcut_path)
    shortcut.TargetPath = target
    shortcut.WorkingDirectory = os.path.dirname(target)
    shortcut.IconLocation = target
    shortcut.Description = description
    shortcut.save()

def main():
    # Assume the install directory is the root directory where this script is located
    install_dir = os.path.dirname(os.path.abspath(__file__))

    # Step 1: CD into the install directory
    os.chdir(install_dir)

    # Step 2: Create a virtual environment with Python 3.11
    print("Creating a virtual environment...")
    run_with_progress([sys.executable, "-m", "venv", ".venv"], "Creating venv")

    # Step 3: Install requirements.txt with pip
    print("Installing requirements from requirements.txt. This might take a while, please be patient.")
    subprocess.run([os.path.join(install_dir, '.venv', 'Scripts', 'pip'), "install", "-r", "requirements.txt"], shell=True, check=True)

    # Step 4: Prompt if the user wants to create the bat file and add a shortcut
    create_shortcut_prompt = input("Do you want to create a batch file and add a shortcut to the desktop? (yes/no): ").strip().lower()
    if create_shortcut_prompt == 'yes':
        # Step 5: Prompt for command line arguments
        print("Please refer to the command_line_arguments.md file in the comfyui directory for more information on available command line arguments.")
        cmd_args = input("Enter any command line arguments you wish to use (e.g., --auto-launch --lowvram): ").strip()

        # Step 6: Create bat file and shortcut
        bat_file_path = os.path.join(install_dir, "run_comfyui.bat")
        with open(bat_file_path, 'w') as bat_file:
            bat_file.write(f'{os.path.join(install_dir, ".venv", "Scripts", "python.exe")} main.py {cmd_args}\n')

        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        shortcut_path = os.path.join(desktop, "ComfyUI.lnk")
        create_shortcut(bat_file_path, shortcut_path, "Shortcut to run ComfyUI")

        print("A bat file was created with your command line arguments in the install directory, and a shortcut to it was added to your desktop.")

    # Step 7: Copy renamed DLL files from ZLUDA
    zluda_dir = os.path.join(install_dir, 'zluda', 'renamed_dlls')
    torch_lib_dir = os.path.join(install_dir, '.venv', 'Lib', 'site-packages', 'torch', 'lib')

    if not os.path.exists(zluda_dir):
        print(f"Error: ZLUDA directory {zluda_dir} does not exist.")
        return

    print("Copying renamed DLL files from ZLUDA...")
    dll_files = ['cublas64_11.dll', 'cusparse64_11.dll']
    for dll in dll_files:
        src_path = os.path.join(zluda_dir, dll)
        dest_path = os.path.join(torch_lib_dir, dll)
        if os.path.exists(src_path):
            shutil.copy2(src_path, dest_path)
            print(f"Copied {dll} to {dest_path}")
        else:
            print(f"Error: {src_path} does not exist.")

    # Final instructions
    print("\nComfyUI installation is complete.")
    if create_shortcut_prompt != 'yes':
        print(f"To activate the virtual environment in the future, run:\n   {os.path.join(install_dir, '.venv', 'Scripts', 'activate')}\n")
        print(f"To run ComfyUI with your specified command line arguments, use the desktop shortcut or run the bat file:\n   {bat_file_path}")

if __name__ == "__main__":
    main()

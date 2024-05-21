import os
import subprocess
import sys
import shutil
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
    # Step 1: Prompt the user for the install directory
    install_dir = input("Enter the directory where you want to install ComfyUI: ").strip()
    comfyui_dir = os.path.join(install_dir, "comfyui")

    # Step 2: Clone the ComfyUI project
    if not os.path.exists(comfyui_dir):
        print("Cloning the ComfyUI project...")
        run_with_progress(["git", "clone", "https://github.com/Royalkin/ComfyUI-Zluda.git", comfyui_dir], "Cloning")
    else:
        print(f"The directory {comfyui_dir} already exists. Skipping cloning step.")

    # Step 3: CD into the ComfyUI directory
    os.chdir(comfyui_dir)

    # Step 4: Create a virtual environment with Python 3.11
    print("Creating a virtual environment...")
    run_with_progress([sys.executable, "-m", "venv", ".venv"], "Creating venv")

    # Step 5: Install requirements.txt with pip
    print("Installing requirements from requirements.txt. This might take a while, please be patient.")
    subprocess.run([os.path.join(comfyui_dir, '.venv', 'Scripts', 'pip'), "install", "-r", "requirements.txt"], shell=True, check=True)

    # Step 6: Prompt if the user wants to create the bat file and add a shortcut
    create_shortcut_prompt = input("Do you want to create a batch file and add a shortcut to the desktop? (yes/no): ").strip().lower()
    if create_shortcut_prompt == 'yes':
        # Step 7: Prompt for command line arguments
        print("Please refer to the command_line_arguments.md file in the comfyui directory for more information on available command line arguments.")
        cmd_args = input("Enter any command line arguments you wish to use (e.g., --auto-launch --lowvram): ").strip()

        # Step 8: Create bat file and shortcut
        bat_file_path = os.path.join(comfyui_dir, "run_comfyui.bat")
        with open(bat_file_path, 'w') as bat_file:
            bat_file.write(f'{sys.executable} main.py {cmd_args}\n')

        desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
        shortcut_path = os.path.join(desktop, "ComfyUI.lnk")
        create_shortcut(bat_file_path, shortcut_path, "Shortcut to run ComfyUI")

        print("A bat file was created with your command line arguments in the ComfyUI root folder, and a shortcut to it was added to your desktop.")

    # Step 9: Copy renamed DLL files from ZLUDA
    zluda_dir = os.path.join(comfyui_dir, 'zluda', 'renamed_dlls')
    torch_lib_dir = os.path.join(comfyui_dir, '.venv', 'Lib', 'site-packages', 'torch', 'lib')

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
        print("To activate the virtual environment in the future, run:\n   {os.path.join(comfyui_dir, '.venv', 'Scripts', 'activate')}\n")
        print(f"To run ComfyUI with your specified command line arguments, use the desktop shortcut or run the bat file:\n   {bat_file_path}")

if __name__ == "__main__":
    main()

import os
import shutil

def compile_code(EXE_NAME="DEFAULT_NAME"):
    args = [
    f"--name={EXE_NAME}",
    '--onefile',
    '--console',
    '--clean',
    '--icon=assets/AFK_Bot.ico',
    f"--add-data={os.path.abspath("assets")};assets",
    "main.py"
]   

    # Delete the old exe if it exits
    target_path = os.path.join("./", f"{EXE_NAME}.exe")
    if os.path.exists(target_path):
        os.remove(target_path)
    
    pyinstaller.run(args)

    # Finally clean up any left over files
    # Delete any Pycache files
    for root, dirs, files in os.walk("./"):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                shutil.rmtree(os.path.join(root, dir_name))
        for file_name in files:
            if file_name.endswith(('.pyc', '.pyo')):
                os.remove(os.path.join(root, file_name))

    # Delete build directory
    build_dir = os.path.join("./", "build")
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)

    # Delete the spec file
    spec_file = os.path.join("./", f"{EXE_NAME}.spec")
    if os.path.exists(spec_file):
        os.remove(spec_file)

    # Move exe to the current directory
    exe_file = os.path.join("dist", f"{EXE_NAME}.exe")
    if os.path.exists(exe_file):
        shutil.move(str(exe_file), str(target_path))

    # Remove the Dist directory
    if os.path.exists("dist"):
        shutil.rmtree("dist")

compile_code("R6_AFK_Bot")
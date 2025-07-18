from app.gui.main_window import MainWindow
import platform
import importlib

def is_linux() -> bool:
    return platform.system() == "Linux"

def has_module(module_name: str) -> bool:
    try:
        importlib.import_module(module_name)
        return True
    except ImportError:
        return False

def suggest_installation(module: str):
    print(f"⚠️ Missing required module: {module}")
    if module == "tkinter":
        print("To install tkinter on Linux:")
        print("  - Debian/Ubuntu: sudo apt-get install python3-tk")
        print("  - Fedora: sudo dnf install python3-tkinter")
        print("  - Arch: sudo pacman -S tk")
    else:
        print(f"You can install {module} with pip:")
        print(f"  pip install {module}")

def check_dependencies():
    print("Checking system and dependencies...\n")

    modules_to_check = ["tkinter", "bs4", "git", "PIL", "datetime", "json", "re", "shutil", "sys", "urllib"]  
    aliases = {"bs4": "beautifulsoup4", "git": "GitPython", "PIL":"Pillow"} 

    if is_linux():
        print("Linux system detected.")

    for module in modules_to_check:
        if not has_module(module):
            package_name = aliases.get(module, module)
            suggest_installation(package_name)
        else:
            print(f"{aliases.get(module, module)} is installed.")

if __name__ == "__main__":
    check_dependencies()
    main_window = MainWindow()
    main_window.mainloop()
    try:
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
    
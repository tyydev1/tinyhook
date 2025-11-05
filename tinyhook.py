import json
import argparse
import os
import shutil

from pathlib import Path

VERSION = "v0.1"
INSTALLED_JSON = 'data/installed.json'
REPO_JSON = 'repo.json'

########################################
# Database Control
########################################

def init_db(file_location):
    if not os.path.exists(file_location):
        with open(file_location, "w") as f:
            json.dump({}, f, indent=2)

def read_db(file_location):
    try:
        with open(file_location, "r") as f:
            return json.load(f)
    except: print(f"File '{file_location}' not found.")
    
def write_db(data, file_location):
    try:
        with open(file_location, "w") as f:
            json.dump(data, f, indent=2)
    except: 
        if data is None: print(f"Data empty")
        if file_location is None: print(f"File '{file_location}' not found")

def is_installed(name):
    try:
        with open(INSTALLED_JSON, "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}
    return name in data

def get_package_info(package_name, file_data_location=REPO_JSON):
    data = read_db(file_data_location)

    if package_name in data.get("packages", {}):
        return data["packages"][package_name]
    else:
        return None

init_db(INSTALLED_JSON)

########################################
# Argument Parsing
########################################

parser = argparse.ArgumentParser(prog="tinyhook", description="TinyHook Package Utils - A minimal package manager")
parser.add_argument(
    "--sandbox",
    action="store_true",
    help="Run Sandbox™ code"

)
parser.add_argument(
    "-v", "--version",
    action="store_true",
    help="Show TinyHook version"
)
parser.add_argument(
    "--debug",
    action="store_true",
    help="Enable debug mode"
)
parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Simulates action without executing it"
)
parser.add_argument(
    "-q", "--quiet",
    action="store_true",
    help="Supresses normal output behavior"
)

subparsers = parser.add_subparsers(dest="command")

hook_parser = subparsers.add_parser("hook", help="Install a package")
hook_parser.add_argument("package_name", help="Name of the package to install")
hook_parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Simulate installation without performing it"
)
hook_parser.add_argument(
    "-q", "--quiet",
    action="store_true",
    help="Supresses normal output behavior"
)

run_parser = subparsers.add_parser("run", help="Run an installed package")
run_parser.add_argument("package_name", help="Name of the package to run")
run_parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Simulates action without executing it"
)
run_parser.add_argument(
    "-q", "--quiet",
    action="store_true",
    help="Supresses normal output behavior"
)

list_parser = subparsers.add_parser("list", help="List installed packages")

remove_parser = subparsers.add_parser("remove", help="Removes a package")
remove_parser.add_argument("package_name", help="Name of the package to remove")
remove_parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Simulates action without executing it"
)
remove_parser.add_argument(
    "-q", "--quiet",
    action="store_true",
    help="Supresses normal output behavior"
)


args = parser.parse_args()

if args.version:
    print(f"TinyHook {VERSION} - Dev Build")

# elif args.command == "hook":
#     if args.quiet: pass
#     elif args.dry_run: print(f"[Dry Run] Would hook {args.package_name}")

#     else: print(f"Hooking {args.package_name}...")

# elif args.command == "run":
#     if args.quiet: pass
#     elif args.dry_run: print(f"[Dry Run] Would run {args.package_name}")

#     else: print(f"Running {args.package_name}...")


# elif args.command == "list":
#     if args.quiet: pass
#     elif args.dry_run: print("[Dry Run] Would list installed packages")
    
#     else: print("Listing installed packages...")

# else:
#     parser.print_help()


########################################
# Command Logic
########################################

if args.command == "hook":
    package_name = args.package_name
    with open(INSTALLED_JSON, "r") as f:
        installed_data = json.load(f)
    
    if is_installed(package_name): print(f"{package_name} is already installed!")
    else:
        new_entry = {
            package_name: {
                "version": "1.0",
                "installed_at": "2025-11-04T12:00:00Z",
                "source_type": "local_path",
                "source_value": f"/data/packages/{package_name}",
                "install_path": f"data/packages/{package_name}"
            }
        }

        if args.dry_run:
            print(f"[Dry Run] Would hook {package_name}")
        else:
            installed_data.update(new_entry)
            write_db(installed_data, INSTALLED_JSON)
            if not args.quiet: print(f"Successfully hooked '{package_name}'!")

elif args.command == "run":
    package_name = args.package_name

    if not is_installed(package_name): print(f"{package_name} is not installed!")
    
    elif args.dry_run: print(f"[Dry Run] Would run {package_name}")

    else: print(f"Running {package_name}")

elif args.command == "list":
    installed_data = read_db(INSTALLED_JSON)

    if not installed_data: print("No packages installed.") # If no packages are installed
    
    elif args.dry_run: print("[Dry Run] Would list packages and version")

    else: 
        for pkg, info in installed_data.items():
            print(f"{pkg} - version {info['version']}")

elif args.command == "remove":
    package_name = args.package_name
    installed_data = read_db(INSTALLED_JSON)

    if not installed_data: print("No packages installed")

    elif args.dry_run and not args.quiet: print(f"[Dry Run] Would remove {package_name}")

    elif not package_name in installed_data: print(f"Package '{package_name}' is not found")

    else:
        deleted = installed_data.pop(package_name)
        write_db(installed_data, INSTALLED_JSON)
        if not args.quiet: print(f"Successfully removed {package_name} !")

else:
    parser.print_help()
    










#########################################################
#                                                       #
#                  Welcome to Sandbox.                  #
#   Sandbox is a free roam code area for testing code   #
#               before implementing it.                 #
#                                                       #
#########################################################
#                                                       #
#  To run Sandbox code, you may use the --sandbox flag. #
#                                                       #
#########################################################

class Sandbox:
    def __init__(self, name, should_auto_instance=False):
        self.name = name
        print(f"============ Sandbox: {self.name} ============")
        print(f"Welcome to Sandbox™!\n\nThe following are instances of Sandbox™ code written inside the Sandbox™ class\nfor Sandbox '{self.name}'")
        self.instance_count = 0
        if should_auto_instance: self.new_instance("Initial Instance")
    
    def new_instance(self, name):
        self.instance_count += 1
        print(f"\n------------ Sandbox Instance {self.instance_count} ------------")
        print(f"Case: {name}\n")
        print(f"Output: ")

    def run(self):
        print("Hello world! learning concept tests here.")


        self.new_instance("Reading data")
        data = read_db(INSTALLED_JSON)
        print(data)


        self.new_instance("Writing data (Updating)")
        new_data = {"hello": {"version": "1.0"}}
        if not is_installed("hello"): data.update(new_data)
        write_db(data, INSTALLED_JSON)
        print(read_db(INSTALLED_JSON))


        self.new_instance("Accessing arguments for hook")
        try: 
            package_name = args.package_name
            print(package_name)
        except: print("[Failure] No arguments provided")


        self.new_instance("Reading package from repo.json")
        pkg_info = get_package_info("hello") # Defaults to repo.json
        if pkg_info:
            print(f"Found: {pkg_info}")
        else:
            print("Package not found in repos")


if args.sandbox:
    sandbox = Sandbox("tinyhook")
    sandbox.run()
import json
import argparse

VERSION = "v0.1"
INSTALLED_JSON = 'data/installed.json'

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

args = parser.parse_args()

if args.version:
    print(f"TinyHook {VERSION} - Dev Build")

elif args.command == "hook":
    if args.quiet: pass
    elif args.dry_run: print(f"[Dry Run] Would hook {args.package_name}")

    else: print(f"Hooking {args.package_name}...")

elif args.command == "run":
    if args.quiet: pass
    elif args.dry_run: print(f"[Dry Run] Would run {args.package_name}")

    else: print(f"Running {args.package_name}...")


elif args.command == "list":
    if args.quiet: pass
    elif args.dry_run: print("[Dry Run] Would list installed packages")
    
    else: print("Listing installed packages...")

elif not args.sandbox:
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

    def read_db(self, file_location):
        try:
            with open(file_location, "r") as f:
                return json.load(f)
        except: print(f"File '{file_location}' not found.")
    
    def write_db(self, data, file_location):
        try:
            with open(file_location, "w") as f:
                json.dump(data, f, indent=2)
        except: 
            if data is None: print(f"Data empty")
            if file_location is None: print(f"File '{file}' not found")

    def is_installed(self, name):
        try:
            with open(INSTALLED_JSON, "r") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        return name in data
    
    def new_instance(self, name):
        self.instance_count += 1
        print(f"\n------------ Sandbox Instance {self.instance_count} ------------")
        print(f"Case: {name}\n")
        print(f"Output: ")

    def run(self):
        print("Hello world! learning concept tests here.")

        self.new_instance("Reading data")
        data = self.read_db(INSTALLED_JSON)
        print(data)

        self.new_instance("Writing data (Updating)")
        new_data = {"hello": {"version": "1.0"}}
        if not self.is_installed("hello"): data.update(new_data)
        self.write_db(data, INSTALLED_JSON)
        print(self.read_db(INSTALLED_JSON))

        self.new_instance("Accessing arguments for hook")
        try: 
            package_name = args.package_name
            print(package_name)
        except: print("[Failure] No arguments provided")

sandbox = Sandbox("tinyhook", True)
if args.sandbox: sandbox.run()
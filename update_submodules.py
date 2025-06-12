import os
import subprocess
import yaml
import shutil

CONFIG_FILE = 'submodules.yaml'

def run(cmd, cwd=None):
    print(f"> {cmd}")
    subprocess.run(cmd, shell=True, check=True, cwd=cwd)

def load_config():
    with open(CONFIG_FILE) as f:
        return yaml.safe_load(f)["submodules"]

def current_submodules():
    if not os.path.exists(".gitmodules"):
        return []
    with open(".gitmodules") as f:
        return [line.split('=')[1].strip() for line in f if line.strip().startswith("path")]

def remove_submodule(path):
    print(f"Removing submodule: {path}")
    run(f"git submodule deinit -f {path}")
    shutil.rmtree(f".git/modules/{path}", ignore_errors=True)
    run(f"git rm -f {path}")

def add_or_update_submodule(url, path, ref):
    if not os.path.exists(path):
        run(f"git submodule add {url} {path}")
    run("git fetch", cwd=path)
    run(f"git checkout {ref}", cwd=path)
    run(f"git add {path}")

def main():
    config = load_config()
    desired_paths = {sub["path"] for sub in config}
    existing_paths = set(current_submodules())

    # Remove submodules not in config
    for path in existing_paths - desired_paths:
        remove_submodule(path)

    # Add or update submodules
    for sub in config:
        add_or_update_submodule(sub["url"], sub["path"], sub["ref"])

    run('git commit -m "Update submodules from config"')

if __name__ == "__main__":
    main()

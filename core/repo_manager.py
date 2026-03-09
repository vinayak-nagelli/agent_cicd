import subprocess
import os
import shutil

CLONE_DIR = "cloned_repo"


def clone_repository(repo_url):
    """
    Clone the GitHub repository.
    """

    if os.path.exists(CLONE_DIR):
        shutil.rmtree(CLONE_DIR)

    print("Cloning repository...")

    result = subprocess.run(
        ["git", "clone", repo_url, CLONE_DIR],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print("Clone failed")
        print(result.stderr)
        return False

    print("Repository cloned successfully")
    return True


def install_dependencies():
    """
    Install requirements.txt if present.
    """

    req_file = os.path.join(CLONE_DIR, "requirements.txt")

    if os.path.exists(req_file):

        print("Installing dependencies...")

        subprocess.run(
            ["pip", "install", "-r", "requirements.txt"],
            cwd=CLONE_DIR
        )

    else:
        print("No requirements.txt found")
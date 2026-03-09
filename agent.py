from core.repo_manager import clone_repository, install_dependencies
from core.test_runner import run_tests


REPO_URL = "https://github.com/vinayak-nagelli/my-first-project.git"


if __name__ == "__main__":

    if not clone_repository(REPO_URL):
        exit()

    install_dependencies()

    run_tests()
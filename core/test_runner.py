import subprocess
from debugging.failure_parser import parse_test_failures

CLONE_DIR = "cloned_repo"


def run_tests():

    print("Running pytest...")

    result = subprocess.run(
        ["python", "-m", "pytest", "-v"],
        cwd=CLONE_DIR,
        capture_output=True,
        text=True
    )

    output = result.stdout

    print(output)

    if result.returncode == 0:
        print("All tests passed")
        return True

    print("Tests failed")

    parse_test_failures(output)

    return False
import subprocess
import sys


def str_starts_with(string: str, prefixes: list[str]):
    """
    Determines if a given string starts with any one of the given list of prefixes.

    :param string: the string to check for prefixes in
    :param prefixes: the list of prefixes
    :return: whether the string begins with any one of the prefixes
    """
    for prefix in prefixes:
        if string.startswith(prefix):
            return True
    return False


prefixes: list[str] = ["DEPRECATION", "ERROR", "WARNING", "Package", "-------"]

failed: list[str] = []
success: list[str] = []

for line in sys.stdin:

    # Don't try to install debug/error output
    if str_starts_with(line, prefixes):
        print(f"Skipping line: \"{line[:len(line)-1]}\"")  # slice removes new-line character
        continue
    
    # Installation is attempted simply by trying to install whatever comes before the first space
    # in the line, if there are any spaces
    line_parts: list[str] = line.split(" ")
    try:
        subprocess.check_call(["pip", "install", "-U", line_parts[0]])
        success.append(line_parts[0])
    except Exception as e:
        print(f"ERROR: Failed to update package: {line_parts[0]} ({e})")
        failed.append(line_parts[0])

if len(success) > 0:
    print(
        "The following packages were updated (list does not include auto-installed dependencies): "
        + ', '.join(success)
    )

if len(failed) > 0:
    print(f"Updates failed for the following packages: {', '.join(failed)}")
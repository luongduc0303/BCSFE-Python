"""Update the editor"""

import subprocess

import requests

from . import config_manager, helper


def update(latest_version: str, command: str = "py") -> None:
    """Update pypi package testing for py and python"""

    helper.colored_text("Updating...", base=helper.GREEN)
    try:
        full_cmd = f"{command} -m pip install --upgrade battle-cats-save-editor=={latest_version}"
        subprocess.run(
            full_cmd,
            shell=True,
            capture_output=True,
            check=True,
        )
        helper.colored_text("Update successful", base=helper.GREEN)
    except subprocess.CalledProcessError as err:
        helper.colored_text("Update failed", base=helper.RED)
        if command == "py":
            helper.colored_text("Trying with python instead", base=helper.RED)
            update(latest_version, "python")
        else:
            helper.colored_text(
                f"Error: {err.stderr.decode('utf-8')}\nYou may need to manually update with py -m pip install -U battle-cats-save-editor",
                base=helper.RED,
            )


def get_local_version() -> str:
    """Returns the local version of the editor"""

    return helper.read_file_string(helper.get_file("version.txt"))


def get_pypi_version():
    """Get latest pypi version of the program"""
    package_name = "battle-cats-save-editor"
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
        response.raise_for_status()
        return response.json()["info"]["version"]
    except requests.exceptions.RequestException as err:
        raise Exception("Error getting pypi version") from err


def get_latest_prerelease_version() -> str:
    """Get latest prerelease version of the program"""
    package_name = "battle-cats-save-editor"
    try:
        response = requests.get(f"https://pypi.org/pypi/{package_name}/json")
        response.raise_for_status()
        releases = list(response.json()["releases"])
        releases.reverse()
        for release in releases:
            if "b" in release:
                return release
        return ""
    except requests.exceptions.RequestException as err:
        raise Exception("Error getting pypi version") from err


def pypi_is_newer(local_version: str, pypi_version: str, remove_b: bool = True) -> bool:
    """Checks if the local version is newer than the pypi version"""
    if remove_b:
        if "b" in pypi_version:
            pypi_version = pypi_version.split("b")[0]
        if "b" in local_version:
            local_version = local_version.split("b")[0]

    return pypi_version > local_version


def check_update() -> tuple[bool, str]:
    """Checks if the editor is updated"""

    local_version = get_local_version()
    pypi_version = get_pypi_version()
    latest_prerelease_version = get_latest_prerelease_version()

    check_pre = "b" in local_version or config_manager.get_config_value_category(
        "START_UP", "UPDATE_TO_BETAS"
    )
    if check_pre and pypi_is_newer(
        local_version, latest_prerelease_version, remove_b=False
    ):
        helper.colored_text("Prerelease update available\n", base=helper.GREEN)
        return True, latest_prerelease_version

    if pypi_is_newer(local_version, pypi_version):
        helper.colored_text("Stable update available\n", base=helper.GREEN)
        return True, pypi_version

    helper.colored_text("No update available\n", base=helper.GREEN)
    return False, local_version

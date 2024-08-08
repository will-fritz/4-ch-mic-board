"""
Description:
Module responsible for various utility functions needed by the system
"""

import fnmatch
import os


def find_file(pattern: str, path: str) -> str:
    """
    find_file(pat, path) is the first file found matching pattern pat.
    """
    for root, _, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                return os.path.join(root, name)


def get_kicad_project_name(path: str) -> str:
    """
    get_kicad_project_name(path) is the name of the KiCad project in the given path.

    Returns None if a KiCad project is not found at the given path.
    """
    try:
        project_file = find_file("*.kicad_pro", path)
        project_name = project_file.split(".kicad_pro")[0]
        project_name = project_name.split(os.sep)[-1]
        return project_name
    except:
        return None


def inches_to_mils(inches):
    """
    inches_to_mils(i) is inches i converted to mils
    """
    return inches * 1000


def inches_to_mm(inches):
    """
    inches_to_mm(i) is inches i converted to millimeters
    """
    return inches * 25.4

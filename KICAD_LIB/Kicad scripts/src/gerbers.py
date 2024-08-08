"""
Description:
Module responsible for generating gerbers and drill files needed for PCB fabrication

Inputs:
- KiCad_Project structure with information about the PCB to document

Outputs:
- Writes files to the file system
"""

import glob
import os
import shutil
import subprocess
import zipfile
from kicad_project import KiCad_Project
from enum import Enum


class GerberFormat(Enum):
    """
    Enumerated Gerber formats
    """

    X2 = 0
    RS274X = 1


class DrillUnits(Enum):
    """
    Enumerated Drill units
    """

    INCHES = 0
    MILLIMETERS = 1


class DrillOrigin(Enum):
    """
    Enumerated Drill Origin choices
    """

    ABSOLUTE = 0
    DRILL_FILE_ORIGIN = 1


class DrillMap(Enum):
    """
    Enumerated Drill Map types
    """

    NO_MAP = 0  # not all fab houses want a drill map file
    GERBER_X2 = 1
    POSTSCRIPT = 2


def plot_and_zip_gerbers(
    kproj: KiCad_Project,
    output_dir: str,
    format: GerberFormat,
    drill_units: DrillUnits,
    drill_origin: DrillOrigin,
    drill_map: DrillMap,
    use_drill_origin_for_gerbers: bool,
    disable_aperture_macros: bool,
) -> None:
    """
    generate and compress gerbers and drill files needed for manufacturing the PCB

    Arguments:
        kproj (KiCad_Project): the structure containing information about the KiCad project

        output_dir (str): path to the output directory for the zipped gerbers

        format (GerberFormat): format to plot, X2 is more typical but some fabs want RS274X

        drill_units (DrillUnits): units for drill file, mm or inches

        drill_origin (DrillOrigin): the origin for the drill file, absolute or use drill file origin

        drill_map (DrillMap): drill map format, or NO_MAP for fabs that don't want a map file

        use_drill_origin_for_gerbers (bool): if true use the drill file origin while plotting gerbers

        disable_aperture_macros (bool): disable aperture macros if true, desired by some fabs

    Side Effects:
        writes files to the file system
    """

    # dump the gerbers in a temporary folder, we'll delete this at the end
    temp_dir = os.path.join(output_dir, "temp")
    os.makedirs(temp_dir, exist_ok=True)

    # plot gerbers
    gerber_args = [
        "kicad-cli",
        "pcb",
        "export",
        "gerbers",
    ]

    if use_drill_origin_for_gerbers:
        gerber_args += ["--use-drill-file-origin"]

    if disable_aperture_macros:
        gerber_args += ["--disable-aperture-macros"]

    if format == GerberFormat.RS274X:
        gerber_args += ["--no-x2"]

    gerber_args += [
        "--subtract-soldermask",
        "--output",
        temp_dir,
        kproj.PCB_FILE,
    ]

    subprocess.call(gerber_args)

    # plot drill files
    drill_args = [
        "kicad-cli",
        "pcb",
        "export",
        "drill",
    ]

    if drill_units == DrillUnits.INCHES:
        drill_args += ["--excellon-units", "in"]
    else:
        drill_args += ["--excellon-units", "mm"]

    if drill_map == DrillMap.GERBER_X2:
        drill_args += [
            "--generate-map",
            "--map-format",
            "gerberx2",
        ]
    elif drill_map == DrillMap.POSTSCRIPT:
        drill_args += [
            "--generate-map",
            "--map-format",
            "ps",
        ]

    if drill_origin == DrillOrigin.ABSOLUTE:
        drill_args += ["--drill-origin", "absolute"]
    elif drill_origin == DrillOrigin.DRILL_FILE_ORIGIN:
        drill_args += ["--drill-origin", "plot"]

    drill_args += [
        "--output",
        # there is a bug where the drill file needs a trailing slash,
        #  see https://gitlab.com/kicad/code/kicad/-/issues/14438
        # remove the extra slash if/when the bug is resolved
        f"{temp_dir}/",
        kproj.PCB_FILE,
    ]

    subprocess.call(drill_args)

    # we don't need all the gerbers that KiCad generated, fab houses only want specific ones
    patterns_to_keep = [
        "*.gtl",  # top copper, F.Cu
        "*.gto",  # top silkscreen, F.SilkS
        "*.gts",  # top solder mask, F.Mask
        "*.gtp",  # top solder paste, F.Paste
        "*.gbl",  # bottom copper, B.Cu
        "*.gbo",  # bottom silkscreen, B.SilkS
        "*.gbs",  # bottom solder mask, B.Mask
        "*.gbp",  # bottom solder paste, B.Paste
        "*.gm1",  # edge cuts, Edge.Cuts
        "*.g2",  # inner copper 1, In1.Cu
        "*.g3",  # inner copper 2, In2.Cu
        "*.g4",  # inner copper 3, In3.Cu
        "*.g5",  # inner copper 4, In4.Cu
        "*.drl",  # drill
        "*-drl_map.gbr",  # drill map
    ]

    gerbers_to_keep = []

    for pattern in patterns_to_keep:
        gerbers_to_keep.extend(glob.glob(os.path.join(temp_dir, pattern)))

    # compress just the files we want to keep
    with zipfile.ZipFile(
        os.path.join(output_dir, f"{kproj.PROJECT_NAME}-gerbers.zip"),
        "w",
    ) as zip_file:
        for full_path_to_gerber in gerbers_to_keep:
            # writing the name only avoids a bunch of junk directory structure being compressed,
            # we want the gerbers at the top level of the compressed file, not buried in subdirs
            name_only = full_path_to_gerber.split(os.sep)[-1]
            zip_file.write(full_path_to_gerber, name_only)

    # get rid of the temporary gerbers
    shutil.rmtree(temp_dir)

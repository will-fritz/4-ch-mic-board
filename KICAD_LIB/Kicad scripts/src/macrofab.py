"""
Description:
Module responsible for generating PCB fabrication files in the format specified
by MacroFab

Inputs:
- KiCad_Project structure with information about the PCB to document

Outputs:
- Writes files to the file system
"""

import common_part_sizes
import os
from kicad_project import KiCad_Project
from gerbers import (
    plot_and_zip_gerbers,
    GerberFormat,
    DrillUnits,
    DrillMap,
    DrillOrigin,
)
from utils import inches_to_mils


def generate_macrofab_outputs(kproj: KiCad_Project) -> None:
    """
    generate the fabrication files needed by Macrofab in their preferred format

    MacroFab wants an XYRS and BOM file

    Parameters:
        kproj (KiCad_Project): the structure containing information about the KiCad project

    Side Effects:
        Writes files to the file system
    """

    # put the macrofab outputs in their own subdirectory of /docs/
    output_dir = os.path.join(kproj.DOCS_DIR, "macrofab")
    os.makedirs(output_dir, exist_ok=True)

    plot_and_zip_gerbers(
        kproj,
        output_dir,
        format=GerberFormat.RS274X,
        drill_units=DrillUnits.INCHES,
        drill_origin=DrillOrigin.ABSOLUTE,
        drill_map=DrillMap.NO_MAP,
        use_drill_origin_for_gerbers=False,
        disable_aperture_macros=True,
    )

    _write_XYRS(kproj, output_dir)
    _write_BOM(kproj, output_dir)


def _write_XYRS(kproj: KiCad_Project, output_dir: str) -> None:
    # rename some columns according to macrofab preferences
    macrofab_xyrs_df = kproj.unique_refs_df.rename(
        columns={
            "Ref": "Designator",
            "Val": "Value",
            "Package": "Footprint",
            "DNP": "Populate",
            "PosX": "X-Loc",
            "PosY": "Y-Loc",
            "Rot": "Rotation",
        }
    )

    # map the DNP field to integers 0 and 1, with 1 meaning "yes do populate this part"
    macrofab_xyrs_df["Populate"] = macrofab_xyrs_df["Populate"].apply(
        _dnp_to_populate_int
    )

    # convert the X and Y locations from inches to mils
    macrofab_xyrs_df["X-Loc"] = macrofab_xyrs_df["X-Loc"].apply(inches_to_mils)
    macrofab_xyrs_df["Y-Loc"] = macrofab_xyrs_df["Y-Loc"].apply(inches_to_mils)

    # create the X and Y size columns, units are mils
    macrofab_xyrs_df["X-Size"] = macrofab_xyrs_df["Footprint"].apply(
        lambda fp: common_part_sizes.footprint_to_XY_mils(fp)[0]
    )
    macrofab_xyrs_df["Y-Size"] = macrofab_xyrs_df["Footprint"].apply(
        lambda fp: common_part_sizes.footprint_to_XY_mils(fp)[1]
    )

    # reorder and keep only needed columns
    macrofab_xyrs_df = macrofab_xyrs_df[
        [
            "Designator",
            "X-Loc",
            "Y-Loc",
            "Rotation",
            "Side",
            "Type",
            "X-Size",
            "Y-Size",
            "Value",
            "Footprint",
            "Populate",
            "MPN",
        ]
    ]

    # this is the file macrofab wants
    file_name = kproj.PROJECT_NAME + ".XYRS"
    macrofab_xyrs_df.to_csv(os.path.join(output_dir, file_name), sep="\t", index=False)
    # create an excel version so we can easily open and verify the contents using excel
    file_name = kproj.PROJECT_NAME + "-XYRS.xlsx"
    macrofab_xyrs_df.to_excel(os.path.join(output_dir, file_name), index=False)


def _write_BOM(kproj, output_dir: str):
    # rename some columns according to macrofab preferences
    macrofab_bom_df = kproj.grouped_by_val_df.rename(
        columns={
            "Ref": "Designator",
            "Val": "Value",
            "DNP": "Populate",
            "Package": "Footprint",
        }
    )
    # map the DNP field to integers 0 and 1, with 1 meaning "do populate this part"
    macrofab_bom_df["Populate"] = macrofab_bom_df["Populate"].apply(
        _dnp_to_populate_int
    )

    # reorder the BOM columns according to macrofab example
    macrofab_bom_df = macrofab_bom_df[
        [
            "Designator",
            "Quantity",
            "Type",
            "Value",
            "Footprint",
            "Populate",
            "Manufacturer",
            "MPN",
        ]
    ]

    file_name = kproj.PROJECT_NAME + "_BOM.xlsx"
    macrofab_bom_df.to_excel(os.path.join(output_dir, file_name), index=False)


def _dnp_to_populate_int(dnp):
    """
    dnp_to_populate_int(dnp) is the integer representing if a component should be populated

    Arguments:
        dnp (str): String representation of Do Not Populate status

    Returns:
        int 0 if the component should not be populated, else 1
    """
    return 0 if dnp.upper() in ["DNF", "DNI", "DNP"] else 1

"""
Description:
Module responsible for generating PCB fabrication files in the format specified
by Advanced Circuits

Inputs:
- KiCad_Project structure with information about the PCB to document

Outputs:
- Writes files to the file system
"""

import os
from kicad_project import KiCad_Project
from gerbers import (
    plot_and_zip_gerbers,
    GerberFormat,
    DrillUnits,
    DrillMap,
    DrillOrigin,
)


def generate_advanced_circuits_outputs(kproj: KiCad_Project) -> None:
    """
    generate the fabrication files needed by Advanced Circuits in their preferred format

    Advanced Circuits wants a pick-and-place (CPL) file and BOM

    Parameters:
        kproj (KiCad_Project): the structure containing information about the KiCad project

    Side Effects:
        Writes files to the file system
    """

    # put the AC outputs in their own subdirectory of /docs/
    output_dir = os.path.join(kproj.DOCS_DIR, "advanced_circuits")
    os.makedirs(output_dir, exist_ok=True)

    plot_and_zip_gerbers(
        kproj,
        output_dir,
        format=GerberFormat.RS274X,
        drill_units=DrillUnits.INCHES,
        drill_origin=DrillOrigin.DRILL_FILE_ORIGIN,
        drill_map=DrillMap.GERBER_X2,
        use_drill_origin_for_gerbers=True,
        disable_aperture_macros=False,
    )

    _write_CPL(kproj, output_dir)
    _write_BOM(kproj, output_dir)


def _write_CPL(kproj: KiCad_Project, output_dir: str) -> None:
    # rename some columns according to AC preferences
    ac_cpl_df = kproj.unique_refs_df.rename(
        columns={
            "Ref": "Ref Designator",
            "PosX": "Mid X",
            "PosY": "Mid Y",
            "Side": "Layer",
            "Rot": "Rotation",
        }
    )

    # reorder and keep only needed columns
    ac_cpl_df = ac_cpl_df[
        [
            "Ref Designator",
            "Mid X",
            "Mid Y",
            "Layer",
            "Rotation",
        ]
    ]

    file_name = kproj.PROJECT_NAME + "_CPL.xlsx"
    ac_cpl_df.to_excel(os.path.join(output_dir, file_name), index=False)


def _write_BOM(kproj: KiCad_Project, output_dir: str) -> None:
    # rename some columns according to AC preferences
    ac_bom_df = kproj.grouped_by_val_df.rename(
        columns={
            "Ref": "Ref Des",
            "Description": "Component Description",
            "Quantity": "QTY",
            "MPN": "Mfg P/N#",
        }
    )

    # reorder and keep only needed columns
    ac_bom_df = ac_bom_df[
        [
            "Component Description",
            "QTY",
            "Ref Des",
            "Mfg P/N#",
            "Manufacturer",
        ]
    ]

    # add distributor part number, to be filled in manually if needed
    ac_bom_df["Distributor P/N"] = "~"

    file_name = kproj.PROJECT_NAME + "_BOM.xlsx"
    ac_bom_df.to_excel(os.path.join(output_dir, file_name), index=False)

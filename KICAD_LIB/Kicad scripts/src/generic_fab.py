"""
Description:
Module responsible for generating PCB fabrication files for a generic/unspecified
fab house. This module generates gerbers and a basic human readable BOM.
There is no position file generated, since each fab house tends to want a 
different format.

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


def generate_generic_outputs(kproj: KiCad_Project) -> None:
    """
    generate the fabrication files

    Parameters:
        kproj (KiCad_Project): the structure containing information about the KiCad project

    Side Effects:
        Writes files to the file system
    """

    # put the outputs in their own subdirectory of /docs/
    output_dir = os.path.join(kproj.DOCS_DIR, "generic_fab")
    os.makedirs(output_dir, exist_ok=True)

    plot_and_zip_gerbers(
        kproj,
        output_dir,
        format=GerberFormat.X2,
        drill_map=DrillMap.GERBER_X2,
        drill_units=DrillUnits.INCHES,
        drill_origin=DrillOrigin.ABSOLUTE,
        use_drill_origin_for_gerbers=False,
        disable_aperture_macros=True,
    )

    _write_BOM(kproj, output_dir)


def _write_BOM(kproj, output_dir: str):
    generic_bom_df = kproj.grouped_by_val_df.copy()

    # reorder the BOM columns
    generic_bom_df = generic_bom_df[
        [
            "Ref",
            "Quantity",
            "Val",
            "Description",
            "Manufacturer",
            "MPN",
            "Package",
            "Type",
            "DNP",
        ]
    ]

    # sort alphabetically on the ref so it's nice for humans to read
    generic_bom_df = generic_bom_df.sort_values(by=["Ref"])

    file_name = kproj.PROJECT_NAME + "_BOM.xlsx"
    generic_bom_df.to_excel(os.path.join(output_dir, file_name), index=False)

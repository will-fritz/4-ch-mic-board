"""
Description:
Module responsible for generating PCB fabrication files in the format specified
by PCBCart

Inputs:
- KiCad_Project structure with information about the PCB to document

Outputs:
- Writes files to the file system
"""


import os
from gerbers import (
    plot_and_zip_gerbers,
    GerberFormat,
    DrillUnits,
    DrillMap,
    DrillOrigin,
)
from kicad_project import KiCad_Project
from utils import inches_to_mm


def generate_pcbcart_outputs(kproj: KiCad_Project) -> None:
    """
    generate the fabrication files needed by PCBCart in their preferred format

    PCBCart wants a pick-and-place (CPL) file and BOM

    Parameters:
        kproj (KiCad_Project): the structure containing information about the KiCad project

    Side Effects:
        Writes files to the file system
    """
    output_dir = os.path.join(kproj.DOCS_DIR, "pcbcart")
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

    _write_POS(kproj, output_dir)
    _write_BOM(kproj, output_dir)


def _write_POS(kproj: KiCad_Project, output_dir: str) -> None:
    # keep only wanted columns according to fab house preferences, in the correct order
    pos_df = kproj.unique_refs_df[
        [
            "Ref",
            "Val",
            "Package",
            "PosX",
            "PosY",
            "Rot",
            "Side",
            "DNP",
        ]
    ].copy()  # since we don't rename any columns (rename func makes a copy) we need to make a copy of the dataframe

    pos_df["PosX"] = pos_df["PosX"].apply(inches_to_mm)
    pos_df["PosY"] = pos_df["PosY"].apply(inches_to_mm)

    file_name = kproj.PROJECT_NAME + "_component_placement.xlsx"
    pos_df.to_excel(os.path.join(output_dir, file_name), index=False)


def _write_BOM(kproj: KiCad_Project, output_dir: str) -> None:
    # rename some columns according to fab house preferences
    pcbcart_bom_df = kproj.grouped_by_val_df.rename(
        columns={
            "MPN": "Manufacturer Part Number",
            "Ref": "Designator",
            "Quantity": "QTY",
            "Package": "Case",
            "Type": "SMD, BGA, LCC, OR TH",
            "Side": "Top/Bottom",
            "Num pins": "points (number of contacts the IC has in each board)",
            "DNP": "Comment",
        }
    )

    pcbcart_bom_df["Total points (number of contacts per BOM line has)"] = (
        pcbcart_bom_df["points (number of contacts the IC has in each board)"]
        * pcbcart_bom_df["QTY"]
    )

    # reorder and keep only needed columns
    pcbcart_bom_df = pcbcart_bom_df[
        [
            "Manufacturer",
            "Manufacturer Part Number",
            "Designator",
            "QTY",
            "Description",
            "Case",
            "SMD, BGA, LCC, OR TH",
            "Top/Bottom",
            "points (number of contacts the IC has in each board)",
            "Total points (number of contacts per BOM line has)",
            "Comment",
        ]
    ]

    file_name = kproj.PROJECT_NAME + "_BOM.xlsx"
    pcbcart_bom_df.to_excel(os.path.join(output_dir, file_name), index=False)

"""
Description:
Module responsible for plotting schematic PDFs for a KiCad project

Inputs:
- KiCad_Project structure with information about the PCB to document

Outputs:
- Writes files to the file system
"""

import os
import subprocess
from kicad_project import KiCad_Project


def plot_schematic(kproj: KiCad_Project) -> None:
    """
    plot the schematic as a PDF using the KiCad CLI
    """
    subprocess.call(
        [
            "kicad-cli",
            "sch",
            "export",
            "pdf",
            "--output",
            os.path.join(kproj.DOCS_DIR, kproj.PROJECT_NAME + "-schematic.pdf"),
            kproj.SCH_FILE,
        ]
    )

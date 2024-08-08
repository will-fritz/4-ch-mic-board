"""
Description:
Main application entry point for KiCad documentation scripts

Inputs:
- Command line argument representing a path to a KiCad project and the fab houses to use

Outputs:
- Writes files to the file system
"""

import argparse
import sys
from kicad_project import KiCad_Project
from schematic import plot_schematic
from advanced_circuits import generate_advanced_circuits_outputs
from generic_fab import generate_generic_outputs
from macrofab import generate_macrofab_outputs
from pcbcart import generate_pcbcart_outputs


"""
Dict of fab-house-name -> fabrication generating function

Each function takes a KiCad_Project structure and generates gerbers, BOM, etc
in the format preferred by the given fab house.
"""
FAB_HOUSES = {
    "advanced-circuits": generate_advanced_circuits_outputs,
    "macrofab": generate_macrofab_outputs,
    "pcbcart": generate_pcbcart_outputs,
    "generic": generate_generic_outputs,
}

# we need a path to the KiCad project that we want to document
parser = argparse.ArgumentParser()
parser.add_argument(
    "project_dir",
    type=str,
    help="path to directory encompassing a KiCad project",
)

# optional list of fab houses from the predefined list of choices, if empty then
# generate documentation for all the fab houses
parser.add_argument(
    "--fabs",
    nargs="+",
    choices=FAB_HOUSES.keys(),
    help="Choose one or more of: %(choices)s)",
)

args = parser.parse_args()

# KiCad project structure holds information about the project
try:
    kicad_project = KiCad_Project(args.project_dir)
except:
    print(f"KiCad project not found in {args.project_dir}, aborting.")
    print()
    parser.print_help(sys.stderr)
    sys.exit(1)

# # generate the outputs
plot_schematic(kicad_project)

if args.fabs is None:
    # if they didn't specify, do all the fab houses
    fabs_to_generate = FAB_HOUSES.keys()
else:
    # otherwise do only the ones they specified in the args
    fabs_to_generate = [fab for fab in args.fabs]

for fab in fabs_to_generate:
    print(f"Generating documentation for {fab}")
    FAB_HOUSES[fab](kicad_project)

# cleanup
kicad_project.cleanup_temp_files()

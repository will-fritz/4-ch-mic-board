# KiCad Documentation Generator Scripts

## Intended Audience
- Yang center engineering team

## Brief
- Python scripts to generate gerbers, BOMs, pick-and-place, etc for fabricating PCBs
- Works with KiCad 7+ projects

## Motivation
- Manually generating fabrication outputs is tedious and error prone
- For large orders we need several quotes, increasing the time and errors spent generating fabrication outputs
- This script is intended to automatically spit out fabrication outputs for the common fab houses we use at the Yang Center

## Dependencies
- [Python 3+](https://www.python.org/)
- [pandas](https://pandas.pydata.org/)
- [openpyxl](https://openpyxl.readthedocs.io/en/stable/)
- [KiCad 7+](https://www.kicad.org/download/)
- Some familiarity with EDA software, KiCad, and PCB fabrication output formats is assumed

## Installation/Setup

### All OS
- Clone or download this repo to your local machine, install it somewhere easy to find

### Windows
- Right click on `/src/kicad_doc_gen.py`, select `Opens with`, then select `Python`
- Add the `/src/` directory to your `PATH` variable
- You may need to add `C:\Program Files\KiCad\7.0\bin` to your `PATH` as well in order for `kicad-cli` to work

### Linux
- Make the python script executable, however you prefer, any of the following
    - Create a symlink to `/src/kicad_doc_gen.py` in `/usr/local/bin` or somewhere on your path
    - Add the `/src/` directory to your path
    - Add an alias to `~/.bashrc` (or equivalent), example: `alias kicad_doc_gen="python ~/clo/scripts/kicad_doc_gen/src/kicad_doc_gen.py"`

### Mac OS
- TODO: If anyone from the Yang Center is using KiCad on Mac OS, please fill this in

## Usage

```
usage: kicad_doc_gen.py [-h] [--fabs {advanced-circuits,macrofab,pcbcart,generic} [{advanced-circuits,macrofab,pcbcart,generic} ...]] project_dir

positional arguments:
  project_dir           path to directory encompassing a KiCad project

options:
  -h, --help            show this help message and exit
  --fabs {advanced-circuits,macrofab,pcbcart,generic} [{advanced-circuits,macrofab,pcbcart,generic} ...]
                        Choose one or more of: advanced-circuits, macrofab, pcbcart, generic)
```

- The intended project directory structure is shown below (before running this script)

```
─── project_root
  ├── kicad_project
  │   ├── project_name.kicad_pcb
  │   ├── project_name.kicad_pro
  │   ├── project_name.kicad_sch
  │   └── ... other KiCad project files
  └── ... Other non-KiCad project files
```
## Demo
- In a terminal navigate to `example_board`
- Run `kicad_doc_gen . --fabs advanced-circuits macrofab`
- Browse the newly generated `docs` directory
    - Each fab house has their own folder of documents
    - Try different combos of fab houses
    - the output will be similar to below (after running this script)

```
─── example_board
  ├── docs
  │ ├── advanced_circuits
  │ │ ├── example_board_BOM.xlsx
  │ │ ├── example_board_CPL.xlsx
  │ │ └── example_board-gerbers.zip
  │ ├── macrofab
  │ │ ├── example_board_BOM.xlsx
  │ │ ├── example_board-XYRS.xlsx
  │ │ └── example_board-gerbers.zip
  │ ├── ... other fab house output directories
  │ └── example_board-schematic.pdf
  ├── kicad_project
  │   ├── example_board.kicad_pcb
  │   ├── example_board.kicad_pro
  │   ├── example_board.kicad_sch
  │   └── ... other KiCad project files
  └── ... Other non-KiCad project files
```

## Mandatory Symbol Structure
- This script requires **all** symbols to a have a few mandatory fields. If these are not included, the script will fail
    - `Manufacturer`: the manufacturer of the part
    - `MPN`: the manufacturer part number. ideally copy-pasted from Digikey or similar vendor website
    - `Type`: the type of the component, in {"SMD", "BGA", "PTH"}
- The [CCB KiCad Symbol Library](https://bitbucket.org/CLO-BRP/ccb_kicad_symbol_lib/src/main/) tracked in Bitbucket conforms to this standard
    - The easiest thing to do is use only symbols from the CCB library
    - Add new symbols which satisfy the standard when you come across a symbol that is not in the CCB library yet

## Understanding kicad-cli
- These scripts heavily leverage KiCad's new Command Line Interface `kicad-cli`, introduced in KiCad 7
- This allows us to easily generate fabrication outputs programatically
- Refer to the [official documentation](https://docs.kicad.org/7.0/en/cli/cli.html)
- Browse the use of the cli in this repo by searching for "kicad-cli"
- Use the built in `--help -h` menu to explore the various subcommands, example shown below
```
➜ kicad-cli -h   
Usage: kicad-cli [-h] {fp,pcb,sch,sym,version}

Optional arguments:
  -v, --version prints version information and exits 
  -h, --help    shows help message and exits 

Subcommands:
  fp            
  pcb           
  sch           
  sym           
  version  
```

## Adding more fab houses
- Each fab house tends to have their own requirements for BOM and pick-and-place formats
- Adding new fab houses should be relatively easy
- All information needed is captured in the KiCad_Project structure
- Pandas dataframes offer an easy way to restructure the data as needed
- See the existing specific fab house python files for guidance

## Code formatting
- The python `black` formatter is used to format all python files
- [black documentation](https://github.com/psf/black)
- [Instructions for setting up black in VSCode](https://marketplace.visualstudio.com/items?itemName=ms-python.black-formatter)
- Any new python code checked in **must** be formatted using `black` first

## Status
- Working well for the fab houses included so far

## Future improvements
- Add more fab houses
- Improve user feedback and/or logging
- Add ability to specify output directory 

## Contact for questions and comments
- Jordan Aceto ja532@cornell.edu

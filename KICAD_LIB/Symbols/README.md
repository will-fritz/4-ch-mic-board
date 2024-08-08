# CCB KiCad Symbol Libraries

## Intended Audience

- Yang Center engineering team

## Brief

- KiCad symbol library

## Standards

- As much as possible, follow the [KiCad Library Conventions](https://klc.kicad.org/)
- Deviations are permitted when it makes sense for our workflow
- Prepend new `.kicad_sym` files with `ccb_[library name]`
- Add new symbols as you need them for projects
    - When adding a new symbol, also add a matching footprint to the CCB footprint lib if one does not already exist

### Mandatory symbol fields

- Symbols should be as atomic as possible. This means that all information needed to buy and assemble the part is captured in the symbol.
- Each symbol must have the following standard fields filled out with correct information
    - `Footprint`: link to a footprint in the CCB KiCad footprint lib
    - `Description`: a good description of the part, ideally copy-pasted from Digikey or similar vendor website
- Each symbol must have the following fields added
    - `Manufacturer`: the manufacturer of the part
    - `MPN`: the manufacturer part number. ideally copy-pasted from Digikey or similar vendor website
    - `Type`: the type of the component, in {"SMD", "BGA", "PTH"}


### Context dependent symbol fields
- `Datasheet`: link to a valid datasheet for the part
    - Active components must have a valid link to a datasheet
    - Passive jellybean components do not need a datasheet, but it is acceptible to include one
    - Use your judgement here, the intention of the datasheet field is that you can hit hotkey `d` while hovering over a symbol and the datasheet pops up. If you think you'll want to look at the datasheet, add the link

Other fields may be optionally added to symbols, but the above are mandatory

## Installation/setup

- Clone or download this repo to your local computer
- Add the library to KiCad either globally, or project specific depending on your preference
    - Adding globally probably makes more sense if you will be doing much KiCad work
    - Ideally, all symbols in your projects will come from this library 
- If you are not familiar with KiCad library management, consult the [KiCad documentation](https://docs.kicad.org/7.0/en/eeschema/eeschema.html#symbols-and-symbol-libraries) 

## Contact for questions and comments

- Jordan Aceto ja532@cornell.edu

"""
Description:
Module responsible for translating common electronics component footprints to 
XY tuples of their bounding box size, in units of mils

Inputs:
- Strings representing the footprint

Outputs:
- Tuples representing the size of the footprint
"""

# dict of part name to (x, y) dimension of rectangular bounding box, in mils
# update this with new packages as they are used (add packages in alphabetical order)
common_sizes = {
    "5035000991": (1078, 1078),
    "BAT-HLD-012-SMT-TR": (694, 346),
    "BMP280": (98, 79),
    "C_0402_1005Metric": (40, 20),
    "C_0603_1608Metric": (60, 30),
    "C_0805_2012Metric": (80, 50),
    "C_1206_3216Metric": (120, 60),
    "C_1210_3225Metric": (120, 100),
    "CR1220-2": (645, 638),
    "Crystal_SMD_3225-4Pin_3.2x2.5mm": (126, 98),
    "Crystal_SMD_MicroCrystal_MS3V-T1R": (55, 264),
    "D_SOD-123": (170, 74),
    "D_SOD-323": (70, 55),
    "D_SMA": (190, 90),
    "Diodes_PowerDI3333-8": (130, 130),
    "DM1AA-SF_NH": (1177, 1102),
    "EMIF06MSD02N16": (118, 28),
    "KSC421_V30_ACT2.95_LFS": (346, 196),
    "L_0805_2012Metric": (80, 50),
    "L_1210_3225Metric": (120, 100),
    "L_Coilcraft_XxL4030": (160, 160),
    "LED_0603_1608Metric": (60, 30),
    "LMZ21700": (138, 138),
    "LQFP-80_12x12mm_P0.5mm": (473, 473),
    "micro_USB_Molex_47589-0001": (296, 192),
    "MURATA-FILTER_CSTCR": (177, 79),
    "PTS815_SJM_250_SMTR_LFS": (176, 136),
    "R_0603_1608Metric": (60, 30),
    "R_0805_1608Metric": (80, 50),
    "Relay_DPDT_Kemet_EE2_NU_DoubleCoil": (295, 591),
    "SIT1534AIH4DCC00032G": (79, 47),
    "SOIC-16W_7.5x10.3mm_P1.27mm": (295, 406),
    "SOT-23": (51, 115),
    "SOT-23W": (63, 114),
    "SOT-23-5": (114, 114),
    "SOT-23-6": (114, 114),
    "SOT-563": (67, 51),
    "Texas_DQK": (78, 78),
    "Texas_DPY0002A_0.6x1mm_P0.65mm": (51, 33),
    "Texas_S-PWSON-N10_ThermalVias": (124, 126),
    "UFBGA-144_10x10mm_Layout12x12_P0.8mm": (394, 394),
    "VQFN-24-1EP_4x4mm_P0.5mm_EP2.45x2.45mm": (158, 158),
    "VQFN-FCRLF14_RXB_TEX": (137, 137),
    "VQFN-HR_9_2mmx2mm": (79, 79),
    "VSSOP-10_3x3mm_P0.5mm": (118, 118),
}

# default size when the package is not in the dict of common sizes
DEFAULT_SIZE = (0, 0)


def footprint_to_XY_mils(fp: str) -> (int, int):
    """
    footprint_to_XY_mils(fp) is a tuple of (x, y) sizes in mils representing the
    bounding box for footprint fp.

    If fp is not recognized then a default size is returned.
    """
    return common_sizes.get(fp, DEFAULT_SIZE)

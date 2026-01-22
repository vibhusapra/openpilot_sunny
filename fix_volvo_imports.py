#!/usr/bin/env python3
"""
Fix script to convert Paper's modern openpilot Volvo implementation to sunnypilot structure.
This script updates all imports and references to work with sunnypilot's older architecture.
"""

import os
import re
from pathlib import Path

# Base directory for Volvo implementation
VOLVO_DIR = Path(__file__).parent / "selfdrive/car/volvo"

# Files to fix
FILES_TO_FIX = [
    "interface.py",
    "carstate.py",
    "carcontroller.py",
    "values.py",
    "fingerprints.py",
]

def fix_interface_py():
    """Fix interface.py imports and structure"""
    filepath = VOLVO_DIR / "interface.py"
    content = filepath.read_text()

    # Fix imports
    content = re.sub(
        r'from selfdrive\.car import structs, get_safety_config',
        'from cereal import car\nfrom openpilot.selfdrive.car import get_safety_config',
        content
    )
    content = re.sub(
        r'from selfdrive\.car\.interfaces import CarInterfaceBase',
        'from openpilot.selfdrive.car.interfaces import CarInterfaceBase',
        content
    )
    content = re.sub(
        r'from selfdrive\.car\.volvo\.',
        'from openpilot.selfdrive.car.volvo.',
        content
    )

    # Fix struct references
    content = re.sub(r'structs\.CarParams', 'car.CarParams', content)
    content = re.sub(r'structs\.CarState', 'car.CarState', content)

    # Fix TransmissionType reference
    content = re.sub(
        r'TransmissionType = structs\.CarParams\.TransmissionType',
        'TransmissionType = car.CarParams.TransmissionType',
        content
    )

    # Fix _get_params method signature
    content = re.sub(
        r'def _get_params\(ret: structs\.CarParams,',
        'def _get_params(ret,',
        content
    )

    # Fix safety model reference
    content = re.sub(
        r'structs\.CarParams\.SafetyModel',
        'car.CarParams.SafetyModel',
        content
    )

    # Fix SteerControlType
    content = re.sub(
        r'structs\.CarParams\.SteerControlType',
        'car.CarParams.SteerControlType',
        content
    )

    filepath.write_text(content)
    print(f"Fixed {filepath}")


def fix_carstate_py():
    """Fix carstate.py imports and structure"""
    filepath = VOLVO_DIR / "carstate.py"
    content = filepath.read_text()

    # Fix imports
    content = re.sub(
        r'from selfdrive\.car import structs, Bus',
        'from cereal import car\nfrom openpilot.selfdrive.car import Bus',
        content
    )
    content = re.sub(
        r'from opendbc\.can\.parser import CANParser',
        'from openpilot.selfdrive.can.parser import CANParser',
        content
    )
    content = re.sub(
        r'from selfdrive\.car\.common\.conversions import Conversions as CV',
        'from openpilot.common.conversions import Conversions as CV',
        content
    )
    content = re.sub(
        r'from selfdrive\.car\.volvo\.',
        'from openpilot.selfdrive.car.volvo.',
        content
    )
    content = re.sub(
        r'from selfdrive\.car\.interfaces import CarStateBase',
        'from openpilot.selfdrive.car.interfaces import CarStateBase',
        content
    )

    # Fix GearShifter and TransmissionType references
    content = re.sub(
        r'GearShifter = structs\.CarState\.GearShifter',
        'GearShifter = car.CarState.GearShifter',
        content
    )
    content = re.sub(
        r'TransmissionType = structs\.CarParams\.TransmissionType',
        'TransmissionType = car.CarParams.TransmissionType',
        content
    )

    # Fix update method signature and return type
    content = re.sub(
        r'def update\(self, can_parsers\) -> structs\.CarState:',
        'def update(self, can_parsers):',
        content
    )

    # Fix CarState instantiation
    content = re.sub(
        r'ret = structs\.CarState\(\)',
        'ret = car.CarState.new_message()',
        content
    )

    filepath.write_text(content)
    print(f"Fixed {filepath}")


def fix_carcontroller_py():
    """Fix carcontroller.py imports and constructor"""
    filepath = VOLVO_DIR / "carcontroller.py"
    content = filepath.read_text()

    # Fix imports
    content = re.sub(
        r'from opendbc\.can\.packer import CANPacker',
        'from openpilot.selfdrive.can.packer import CANPacker',
        content
    )
    content = re.sub(
        r'from selfdrive\.car import Bus',
        'from openpilot.selfdrive.car import Bus',
        content
    )
    content = re.sub(
        r'from selfdrive\.car\.interfaces import CarControllerBase',
        'from openpilot.selfdrive.car.interfaces import CarControllerBase',
        content
    )
    content = re.sub(
        r'from selfdrive\.car\.volvo\.',
        'from openpilot.selfdrive.car.volvo.',
        content
    )

    # Fix constructor signature - add VM parameter
    content = re.sub(
        r'def __init__\(self, dbc_names, CP\):',
        'def __init__(self, dbc_name, CP, VM):',
        content
    )

    # Fix super().__init__ call
    content = re.sub(
        r'super\(\).__init__\(dbc_names, CP\)',
        'super().__init__(dbc_name, CP, VM)',
        content
    )

    # Fix packer initialization - use dbc_name instead of dbc_names[Bus.party]
    content = re.sub(
        r'self\.packer = CANPacker\(dbc_names\[Bus\.party\]\)',
        'self.packer = CANPacker(dbc_name)',
        content
    )

    filepath.write_text(content)
    print(f"Fixed {filepath}")


def fix_values_py():
    """Fix values.py imports"""
    filepath = VOLVO_DIR / "values.py"
    content = filepath.read_text()

    # Fix imports
    content = re.sub(
        r'from selfdrive\.car\.structs import CarParams',
        'from cereal import car',
        content
    )
    content = re.sub(
        r'from selfdrive\.car import ',
        'from openpilot.selfdrive.car import ',
        content
    )
    content = re.sub(
        r'from selfdrive\.car\.lateral import AngleSteeringLimits',
        'from openpilot.selfdrive.car.lateral_angle import AngleSteeringLimits',
        content
    )
    content = re.sub(
        r'from selfdrive\.car\.docs_definitions import',
        'from openpilot.selfdrive.car.docs_definitions import',
        content
    )
    content = re.sub(
        r'from selfdrive\.car\.fw_query_definitions import',
        'from openpilot.selfdrive.car.fw_query_definitions import',
        content
    )

    # Fix Ecu reference
    content = re.sub(
        r'Ecu = CarParams\.Ecu',
        'Ecu = car.CarParams.Ecu',
        content
    )

    filepath.write_text(content)
    print(f"Fixed {filepath}")


def fix_fingerprints_py():
    """Fix fingerprints.py imports"""
    filepath = VOLVO_DIR / "fingerprints.py"
    content = filepath.read_text()

    # Fix imports
    content = re.sub(
        r'from selfdrive\.car\.structs import CarParams',
        'from cereal import car',
        content
    )
    content = re.sub(
        r'from selfdrive\.car\.volvo\.',
        'from openpilot.selfdrive.car.volvo.',
        content
    )

    # Fix Ecu reference
    content = re.sub(
        r'Ecu = CarParams\.Ecu',
        'Ecu = car.CarParams.Ecu',
        content
    )

    filepath.write_text(content)
    print(f"Fixed {filepath}")


def fix_helper_files():
    """Fix any helper files that exist"""
    helper_files = ["helpers.py", "volvocan.py", "live_testing.py", "lca_encoder.py"]

    for filename in helper_files:
        filepath = VOLVO_DIR / filename
        if not filepath.exists():
            continue

        content = filepath.read_text()

        # Fix common imports
        content = re.sub(
            r'from selfdrive\.car\.',
            'from openpilot.selfdrive.car.',
            content
        )
        content = re.sub(
            r'from selfdrive\.car import',
            'from openpilot.selfdrive.car import',
            content
        )
        content = re.sub(
            r'from opendbc\.can\.',
            'from openpilot.selfdrive.can.',
            content
        )

        filepath.write_text(content)
        print(f"Fixed {filepath}")


def main():
    """Main function to run all fixes"""
    print("Starting Volvo import fixes for sunnypilot...")
    print(f"Working in: {VOLVO_DIR}")

    if not VOLVO_DIR.exists():
        print(f"Error: Volvo directory not found at {VOLVO_DIR}")
        return 1

    # Fix each file
    fix_interface_py()
    fix_carstate_py()
    fix_carcontroller_py()
    fix_values_py()
    fix_fingerprints_py()
    fix_helper_files()

    print("\n✅ All imports fixed for sunnypilot compatibility!")
    print("\nNext steps:")
    print("1. Run: python3 fix_volvo_imports.py")
    print("2. Test locally with: python3 -m py_compile selfdrive/car/volvo/*.py")
    print("3. Push to GitHub and test on device")

    return 0


if __name__ == "__main__":
    exit(main())
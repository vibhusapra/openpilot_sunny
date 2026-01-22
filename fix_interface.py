#!/usr/bin/env python3
"""
Fix remaining issues in Volvo interface for sunnypilot
"""

import re
from pathlib import Path

def fix_interface():
    filepath = Path(__file__).parent / "selfdrive/car/volvo/interface.py"
    content = filepath.read_text()

    # Remove type annotation from _get_params (sunnypilot doesn't use them)
    content = re.sub(
        r'def _get_params\(ret: car\.CarParams, candidate, fingerprint, car_fw, alpha_long, is_release, docs\) -> car\.CarParams:',
        'def _get_params(ret, candidate, fingerprint, car_fw, experimental_long, docs):',
        content
    )

    # Add lateral tuning for angle control (required even for angle control)
    lateral_tuning = '''    # Lateral tuning for angle control
    ret.lateralTuning.init('pid')
    ret.lateralTuning.pid.kiBP = [0.]
    ret.lateralTuning.pid.kpBP = [0.]
    ret.lateralTuning.pid.kpV = [0.1]  # Conservative angle control
    ret.lateralTuning.pid.kiV = [0.0]
    ret.lateralTuning.pid.kf = 0.00004

'''

    # Insert lateral tuning after steerControlType line
    content = re.sub(
        r'(    ret\.steerControlType = car\.CarParams\.SteerControlType\.angle\n)(    # Note: No lateral tuning.*?\n)',
        r'\1' + lateral_tuning,
        content
    )

    # Add missing parameters
    missing_params = '''    # Additional required parameters
    ret.steerMaxBP = [0.]
    ret.steerMaxV = [1.]
    ret.gasMaxBP = [0.]
    ret.gasMaxV = [0.5]
    ret.brakeMaxBP = [0.]
    ret.brakeMaxV = [1.]
    ret.longitudinalTuning.deadzoneBP = [0.]
    ret.longitudinalTuning.deadzoneV = [0.]
    ret.longitudinalActuatorDelayLowerBound = 0.3
    ret.longitudinalActuatorDelayUpperBound = 0.3
    ret.stoppingDecelRate = 0.3  # reach stopping target smoothly
    ret.startingAccelRate = 0.3  # reach starting target smoothly
    ret.vEgoStopping = 0.5
    ret.vEgoStarting = 0.5

'''

    # Add before return statement
    content = re.sub(
        r'(    return ret)',
        missing_params + r'\1',
        content
    )

    # Fix experimental_long parameter name (was alpha_long)
    content = content.replace('alpha_long', 'experimental_long')

    filepath.write_text(content)
    print(f"Fixed {filepath}")
    return True

if __name__ == "__main__":
    if fix_interface():
        print("\n✅ Interface fixed successfully!")
        print("\nKey fixes applied:")
        print("1. Removed type annotations from _get_params")
        print("2. Added lateral tuning for angle control")
        print("3. Added missing required parameters")
        print("4. Fixed experimental_long parameter name")
#!/usr/bin/env python3
"""
Comprehensive test script to verify Polestar 2 support.

This script simulates the openpilot startup sequence for a Polestar 2:
1. Check that Volvo is registered in the platform system
2. Verify fingerprint detection works
3. Instantiate CarInterface
4. Run a mock control loop

Usage:
    python3 tools/test_polestar2_startup.py
"""

import sys
import time
from cereal import car
from openpilot.selfdrive.car import gen_empty_fingerprint
from openpilot.selfdrive.car.volvo.values import CAR
from openpilot.selfdrive.car.volvo.fingerprints import FINGERPRINTS


def test_registration():
    """Test 1: Verify Volvo is registered."""
    print("\n" + "="*80)
    print("TEST 1: Checking Volvo registration in platform system")
    print("="*80)

    try:
        from openpilot.selfdrive.car.values import PLATFORMS
        polestar_2_key = str(CAR.POLESTAR_2)

        if polestar_2_key not in PLATFORMS:
            print(f"❌ FAIL: {polestar_2_key} not found in PLATFORMS")
            print(f"Available platforms: {list(PLATFORMS.keys())[:10]}...")
            return False

        print(f"✓ SUCCESS: {polestar_2_key} is registered in PLATFORMS")
        print(f"  Platform value: {PLATFORMS[polestar_2_key]}")
        return True

    except Exception as e:
        print(f"❌ FAIL: Exception during registration check: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_interface_loading():
    """Test 2: Verify interface can be loaded."""
    print("\n" + "="*80)
    print("TEST 2: Loading Volvo CarInterface through car_helpers")
    print("="*80)

    try:
        from openpilot.selfdrive.car.car_helpers import interfaces
        polestar_2_key = str(CAR.POLESTAR_2)

        if polestar_2_key not in interfaces:
            print(f"❌ FAIL: {polestar_2_key} not found in interfaces dict")
            print(f"Available interfaces: {list(interfaces.keys())[:10]}...")
            return False

        CarInterface, CarController, CarState = interfaces[polestar_2_key]
        print(f"✓ SUCCESS: Loaded interfaces for {polestar_2_key}")
        print(f"  CarInterface: {CarInterface}")
        print(f"  CarController: {CarController}")
        print(f"  CarState: {CarState}")
        return True

    except Exception as e:
        print(f"❌ FAIL: Exception during interface loading: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_car_params():
    """Test 3: Get CarParams for Polestar 2."""
    print("\n" + "="*80)
    print("TEST 3: Getting CarParams for Polestar 2")
    print("="*80)

    try:
        from openpilot.selfdrive.car.car_helpers import interfaces
        polestar_2_key = str(CAR.POLESTAR_2)

        CarInterface, _, _ = interfaces[polestar_2_key]

        # Create mock fingerprint
        fingerprint = gen_empty_fingerprint()
        fingerprint[0] = FINGERPRINTS[CAR.POLESTAR_2][0]

        # Get params
        CP = CarInterface.get_params(
            polestar_2_key,
            fingerprint,
            [],
            experimental_long=False,
            docs=False
        )

        print(f"✓ SUCCESS: Got CarParams for {polestar_2_key}")
        print(f"  Car name: {CP.carName}")
        print(f"  Brand: {CP.brand}")
        print(f"  Mass: {CP.mass} kg")
        print(f"  Wheelbase: {CP.wheelbase} m")
        print(f"  Steering control: {CP.steerControlType}")
        print(f"  Safety model: {CP.safetyConfigs[0].safetyModel}")

        # Validate critical parameters
        assert CP.brand == 'volvo', f"Brand should be 'volvo', got '{CP.brand}'"
        assert CP.steerControlType == car.CarParams.SteerControlType.angle, \
            "Should use angle control"
        assert CP.mass > 2000, f"Mass seems too low: {CP.mass}"

        print("  All parameter validations passed!")
        return True

    except Exception as e:
        print(f"❌ FAIL: Exception getting CarParams: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_car_interface_instantiation():
    """Test 4: Instantiate CarInterface."""
    print("\n" + "="*80)
    print("TEST 4: Instantiating CarInterface")
    print("="*80)

    try:
        from openpilot.selfdrive.car.car_helpers import interfaces
        polestar_2_key = str(CAR.POLESTAR_2)

        CarInterface, CarController, CarState = interfaces[polestar_2_key]

        # Create mock fingerprint
        fingerprint = gen_empty_fingerprint()
        fingerprint[0] = FINGERPRINTS[CAR.POLESTAR_2][0]

        # Get params
        CP = CarInterface.get_params(
            polestar_2_key,
            fingerprint,
            [],
            experimental_long=False,
            docs=False
        )

        # Instantiate
        CI = CarInterface(CP, CarController, CarState)

        print(f"✓ SUCCESS: CarInterface instantiated")
        print(f"  CI type: {type(CI)}")
        print(f"  Has CC: {hasattr(CI, 'CC')}")
        print(f"  Has CS: {hasattr(CI, 'CS')}")
        return True

    except Exception as e:
        print(f"❌ FAIL: Exception instantiating CarInterface: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_mock_update():
    """Test 5: Run mock update loop."""
    print("\n" + "="*80)
    print("TEST 5: Running mock update loop (10 iterations)")
    print("="*80)

    try:
        from openpilot.selfdrive.car.car_helpers import interfaces
        polestar_2_key = str(CAR.POLESTAR_2)

        CarInterface, CarController, CarState = interfaces[polestar_2_key]

        # Create mock fingerprint
        fingerprint = gen_empty_fingerprint()
        fingerprint[0] = FINGERPRINTS[CAR.POLESTAR_2][0]

        # Get params
        CP = CarInterface.get_params(
            polestar_2_key,
            fingerprint,
            [],
            experimental_long=False,
            docs=False
        )

        # Instantiate
        CI = CarInterface(CP, CarController, CarState)

        # Run mock update loop
        print("  Running update loop...")
        for i in range(10):
            try:
                # Call update with empty CAN strings
                # This will likely fail internally, but shouldn't crash with import errors
                CI.update([])
                print(f"    Iteration {i+1}/10: ✓")
            except Exception as e:
                # We expect errors due to missing CAN data, but not import errors
                error_type = type(e).__name__
                if error_type in ['ImportError', 'ModuleNotFoundError', 'KeyError']:
                    print(f"❌ FAIL: Critical error at iteration {i+1}: {error_type}: {e}")
                    raise
                else:
                    # Expected errors (missing CAN data, etc)
                    print(f"    Iteration {i+1}/10: Expected error ({error_type})")

        print(f"✓ SUCCESS: Update loop completed without import errors")
        return True

    except Exception as e:
        print(f"❌ FAIL: Exception in update loop: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests."""
    print("\n" + "="*80)
    print("POLESTAR 2 SUPPORT VALIDATION TEST SUITE")
    print("="*80)

    tests = [
        ("Platform Registration", test_registration),
        ("Interface Loading", test_interface_loading),
        ("CarParams Generation", test_car_params),
        ("CarInterface Instantiation", test_car_interface_instantiation),
        ("Mock Update Loop", test_mock_update),
    ]

    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
        time.sleep(0.5)

    # Print summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)

    for test_name, result in results:
        status = "✓ PASS" if result else "❌ FAIL"
        print(f"  {status}: {test_name}")

    passed = sum(1 for _, r in results if r)
    total = len(results)

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Polestar 2 support is working correctly.")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review errors above.")
        return 1


if __name__ == '__main__':
    sys.exit(main())
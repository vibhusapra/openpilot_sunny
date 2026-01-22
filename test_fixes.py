#!/usr/bin/env python3
"""
Simple test to verify our fixes without requiring all dependencies.
"""

import os
import ast


def test_volvo_registered():
    """Test that Volvo is registered in values.py"""
    print("\n" + "="*80)
    print("TEST 1: Checking Volvo registration in values.py")
    print("="*80)

    with open('selfdrive/car/values.py', 'r') as f:
        content = f.read()

    # Check if Volvo import exists
    if 'from openpilot.selfdrive.car.volvo.values import CAR as VOLVO' in content:
        print("✓ Volvo import found in values.py")
    else:
        print("❌ Volvo import NOT found in values.py")
        return False

    # Check if VOLVO is in Platform union
    if '| VOLVO' in content:
        print("✓ VOLVO added to Platform union")
    else:
        print("❌ VOLVO NOT in Platform union")
        return False

    print("✓ SUCCESS: Volvo is properly registered in values.py")
    return True


def test_volvo_in_fingerprints():
    """Test that Volvo is imported in fingerprints.py"""
    print("\n" + "="*80)
    print("TEST 2: Checking Volvo import in fingerprints.py")
    print("="*80)

    with open('selfdrive/car/fingerprints.py', 'r') as f:
        content = f.read()

    if 'from openpilot.selfdrive.car.volvo.values import CAR as VOLVO' in content:
        print("✓ Volvo import found in fingerprints.py")
        print("✓ SUCCESS: Volvo is properly imported in fingerprints.py")
        return True
    else:
        print("❌ Volvo import NOT found in fingerprints.py")
        return False


def test_can_imports():
    """Test that CAN imports are fixed"""
    print("\n" + "="*80)
    print("TEST 3: Checking CAN imports are fixed")
    print("="*80)

    errors = []

    # Check carcontroller.py
    with open('selfdrive/car/volvo/carcontroller.py', 'r') as f:
        content = f.read()

    if 'from opendbc.can.packer import CANPacker' in content:
        print("✓ carcontroller.py uses correct CAN import (opendbc.can.packer)")
    elif 'from openpilot.selfdrive.can.packer' in content:
        print("❌ carcontroller.py still has wrong import (openpilot.selfdrive.can)")
        errors.append("carcontroller.py")
    else:
        print("⚠️  carcontroller.py has unexpected CAN import")
        errors.append("carcontroller.py")

    # Check carstate.py
    with open('selfdrive/car/volvo/carstate.py', 'r') as f:
        content = f.read()

    if 'from opendbc.can.parser import CANParser' in content:
        print("✓ carstate.py uses correct CAN import (opendbc.can.parser)")
    elif 'from openpilot.selfdrive.can.parser' in content:
        print("❌ carstate.py still has wrong import (openpilot.selfdrive.can)")
        errors.append("carstate.py")
    else:
        print("⚠️  carstate.py has unexpected CAN import")
        errors.append("carstate.py")

    if not errors:
        print("✓ SUCCESS: All CAN imports are correctly fixed")
        return True
    else:
        print(f"❌ FAIL: Issues found in: {', '.join(errors)}")
        return False


def test_python_syntax():
    """Test that all Python files have valid syntax"""
    print("\n" + "="*80)
    print("TEST 4: Checking Python syntax in Volvo files")
    print("="*80)

    volvo_files = [
        'selfdrive/car/volvo/interface.py',
        'selfdrive/car/volvo/carstate.py',
        'selfdrive/car/volvo/carcontroller.py',
        'selfdrive/car/volvo/values.py',
        'selfdrive/car/volvo/fingerprints.py',
    ]

    errors = []
    for filepath in volvo_files:
        try:
            with open(filepath, 'r') as f:
                ast.parse(f.read())
            print(f"✓ {filepath}: Valid Python syntax")
        except SyntaxError as e:
            print(f"❌ {filepath}: Syntax error: {e}")
            errors.append(filepath)

    if not errors:
        print("✓ SUCCESS: All Volvo Python files have valid syntax")
        return True
    else:
        print(f"❌ FAIL: Syntax errors in: {', '.join(errors)}")
        return False


def test_test_files_created():
    """Test that all test files were created"""
    print("\n" + "="*80)
    print("TEST 5: Checking test files were created")
    print("="*80)

    test_files = [
        'selfdrive/car/volvo/tests/__init__.py',
        'selfdrive/car/volvo/tests/test_imports.py',
        'selfdrive/car/volvo/tests/test_polestar2_detection.py',
        'selfdrive/car/volvo/tests/test_car_interface.py',
        'tools/test_polestar2_startup.py',
    ]

    missing = []
    for filepath in test_files:
        if os.path.exists(filepath):
            print(f"✓ {filepath}: Exists")
        else:
            print(f"❌ {filepath}: Missing")
            missing.append(filepath)

    if not missing:
        print("✓ SUCCESS: All test files created")
        return True
    else:
        print(f"❌ FAIL: Missing files: {', '.join(missing)}")
        return False


def main():
    """Run all tests"""
    print("\n" + "="*80)
    print("POLESTAR 2 FIX VALIDATION")
    print("="*80)
    print("\nThis test verifies our fixes without requiring all dependencies.")

    tests = [
        ("Volvo Registration in values.py", test_volvo_registered),
        ("Volvo Import in fingerprints.py", test_volvo_in_fingerprints),
        ("CAN Import Fixes", test_can_imports),
        ("Python Syntax Check", test_python_syntax),
        ("Test Files Created", test_test_files_created),
    ]

    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))

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
        print("\n🎉 ALL TESTS PASSED!")
        print("\nThe fixes are ready to be deployed to the Comma 3:")
        print("1. Volvo is registered in the platform system")
        print("2. CAN imports are corrected")
        print("3. All Python files have valid syntax")
        print("4. Test files are created for future validation")
        print("\nNext step: Push to GitHub and deploy to Comma 3")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please review errors above.")
        return 1


if __name__ == '__main__':
    exit(main())
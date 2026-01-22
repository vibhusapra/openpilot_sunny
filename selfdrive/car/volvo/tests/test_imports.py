"""Test that all Volvo imports work correctly."""
import unittest


class TestVolvoImports(unittest.TestCase):
    def test_can_imports(self):
        """Test that CAN imports work."""
        from opendbc.can.packer import CANPacker
        from opendbc.can.parser import CANParser
        self.assertIsNotNone(CANPacker)
        self.assertIsNotNone(CANParser)

    def test_volvo_module_imports(self):
        """Test that all Volvo modules can be imported."""
        from openpilot.selfdrive.car.volvo import interface
        from openpilot.selfdrive.car.volvo import carstate
        from openpilot.selfdrive.car.volvo import carcontroller
        from openpilot.selfdrive.car.volvo import values
        from openpilot.selfdrive.car.volvo import fingerprints

        self.assertIsNotNone(interface)
        self.assertIsNotNone(carstate)
        self.assertIsNotNone(carcontroller)
        self.assertIsNotNone(values)
        self.assertIsNotNone(fingerprints)

    def test_volvo_registered_in_platforms(self):
        """Test that Volvo is registered in the platform system."""
        from openpilot.selfdrive.car.values import PLATFORMS
        from openpilot.selfdrive.car.volvo.values import CAR

        # Check that POLESTAR_2 is in PLATFORMS
        polestar_2_key = str(CAR.POLESTAR_2)
        self.assertIn(polestar_2_key, PLATFORMS)
        self.assertEqual(PLATFORMS[polestar_2_key], CAR.POLESTAR_2)

    def test_volvo_interface_loadable(self):
        """Test that Volvo interface can be loaded through car_helpers."""
        from openpilot.selfdrive.car.car_helpers import interfaces
        from openpilot.selfdrive.car.volvo.values import CAR

        polestar_2_key = str(CAR.POLESTAR_2)
        self.assertIn(polestar_2_key, interfaces)

        CarInterface, CarController, CarState = interfaces[polestar_2_key]
        self.assertIsNotNone(CarInterface)
        self.assertIsNotNone(CarController)
        self.assertIsNotNone(CarState)


if __name__ == '__main__':
    unittest.main()
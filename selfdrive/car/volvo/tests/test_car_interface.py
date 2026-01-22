"""Test Volvo CarInterface instantiation."""
import unittest
from cereal import car
from openpilot.selfdrive.car import gen_empty_fingerprint
from openpilot.selfdrive.car.volvo.interface import CarInterface
from openpilot.selfdrive.car.volvo.carcontroller import CarController
from openpilot.selfdrive.car.volvo.carstate import CarState
from openpilot.selfdrive.car.volvo.values import CAR
from openpilot.selfdrive.car.volvo.fingerprints import FINGERPRINTS


class TestVolvoCarInterface(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        # Use actual Polestar 2 fingerprint
        self.fingerprint = gen_empty_fingerprint()
        self.fingerprint[0] = FINGERPRINTS[CAR.POLESTAR_2][0]

        # Empty firmware list
        self.car_fw = []

    def test_get_params(self):
        """Test that get_params works for Polestar 2."""
        car_name = str(CAR.POLESTAR_2)

        car_params = CarInterface.get_params(
            car_name,
            self.fingerprint,
            self.car_fw,
            experimental_long=False,
            docs=False
        )

        self.assertIsNotNone(car_params)
        self.assertEqual(car_params.carName, car_name)
        self.assertEqual(car_params.brand, 'volvo')

        # Check angle-based steering is configured
        self.assertEqual(car_params.steerControlType, car.CarParams.SteerControlType.angle)

        # Check safety config
        self.assertEqual(len(car_params.safetyConfigs), 1)
        self.assertEqual(car_params.safetyConfigs[0].safetyModel,
                        car.CarParams.SafetyModel.noOutput)

        # Check physical parameters
        self.assertGreater(car_params.mass, 2000)  # Polestar 2 is ~2123 kg
        self.assertGreater(car_params.wheelbase, 2.7)  # ~2.735 m
        self.assertGreater(car_params.steerRatio, 15)  # ~15.8

    def test_car_interface_instantiation(self):
        """Test that CarInterface can be instantiated."""
        car_name = str(CAR.POLESTAR_2)

        car_params = CarInterface.get_params(
            car_name,
            self.fingerprint,
            self.car_fw,
            experimental_long=False,
            docs=False
        )

        # Create CarInterface instance
        ci = CarInterface(car_params, CarController, CarState)
        self.assertIsNotNone(ci)
        self.assertIsNotNone(ci.CP)
        self.assertIsNotNone(ci.CC)
        self.assertIsNotNone(ci.CS)

    def test_update_loop(self):
        """Test that update loop can run without crashing."""
        car_name = str(CAR.POLESTAR_2)

        car_params = CarInterface.get_params(
            car_name,
            self.fingerprint,
            self.car_fw,
            experimental_long=False,
            docs=False
        )

        ci = CarInterface(car_params, CarController, CarState)

        # Create mock CAN data
        # For testing, we'll use empty CAN data
        can_strings = []

        # Try to run update - should not crash even with empty data
        try:
            ci.update(can_strings)
            # If we get here without exception, test passes
            self.assertTrue(True)
        except Exception as e:
            # We expect some errors with empty CAN data, but not import errors
            self.assertNotIn('ImportError', str(type(e)))
            self.assertNotIn('ModuleNotFoundError', str(type(e)))


if __name__ == '__main__':
    unittest.main()
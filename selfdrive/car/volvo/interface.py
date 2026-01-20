from cereal import car
from openpilot.selfdrive.car import get_safety_config
from openpilot.selfdrive.car.interfaces import CarInterfaceBase
from openpilot.selfdrive.car.volvo.carcontroller import CarController
from openpilot.selfdrive.car.volvo.carstate import CarState

TransmissionType = car.CarParams.TransmissionType


class CarInterface(CarInterfaceBase):
  CarState = CarState
  CarController = CarController

  @staticmethod
  def _get_params(ret: car.CarParams, candidate, fingerprint, car_fw, alpha_long, is_release, docs) -> car.CarParams:
    ret.brand = 'volvo'

    ret.safetyConfigs = [get_safety_config(car.CarParams.SafetyModel.volvo)]
    #ret.safetyConfigs = [get_safety_config(car.CarParams.SafetyModel.noOutput)]

    ret.dashcamOnly = False

    ret.steerActuatorDelay = 0.3
    ret.steerLimitTimer = 0.1
    ret.steerAtStandstill = True

    # Use angle-based steering control for Volvo CMA platform
    ret.steerControlType = car.CarParams.SteerControlType.angle
    # Note: No lateral tuning configuration needed for basic angle control
    ret.radarUnavailable = True

    ret.alphaLongitudinalAvailable = False

    ret.pcmCruise = True

    return ret
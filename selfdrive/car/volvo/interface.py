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
  def _get_params(ret, candidate, fingerprint, car_fw, experimental_long, docs):
    ret.brand = 'volvo'

    #ret.safetyConfigs = [get_safety_config(car.CarParams.SafetyModel.volvo)]
    ret.safetyConfigs = [get_safety_config(car.CarParams.SafetyModel.noOutput)]

    ret.dashcamOnly = False

    ret.steerActuatorDelay = 0.3
    ret.steerLimitTimer = 0.1
    ret.steerAtStandstill = True

    # Use angle-based steering control for Volvo CMA platform
    ret.steerControlType = car.CarParams.SteerControlType.angle
    # Lateral tuning for angle control
    ret.lateralTuning.init('pid')
    ret.lateralTuning.pid.kiBP = [0.]
    ret.lateralTuning.pid.kpBP = [0.]
    ret.lateralTuning.pid.kpV = [0.1]  # Conservative angle control
    ret.lateralTuning.pid.kiV = [0.0]
    ret.lateralTuning.pid.kf = 0.00004

    ret.radarUnavailable = True

    ret.alphaLongitudinalAvailable = False

    ret.pcmCruise = True

    # Additional required parameters
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

    return ret
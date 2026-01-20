from dataclasses import dataclass, field

from cereal import car
from openpilot.selfdrive.car import CarSpecs, PlatformConfig, Platforms, dbc_dict
from openpilot.selfdrive.car.docs_definitions import CarDocs, CarHarness, CarParts
from openpilot.selfdrive.car.fw_query_definitions import FwQueryConfig, Request, StdQueries

Ecu = car.CarParams.Ecu


class CarControllerParams:
  STEER_STEP = 1  # 100 Hz LCA command frequency (controlsd runs at 100 Hz)
  # Note: Angle rate limiting is handled by panda safety model, not in Python


@dataclass
class VolvoCarDocs(CarDocs):
  package: str = "Pilot Assist & Adaptive Cruise Control"
  car_parts: CarParts = field(default_factory=CarParts.common([CarHarness.custom]))


@dataclass
class VolvoCMAPlatformConfig(PlatformConfig):
  def init(self):
    pass

@dataclass
class VolvoSPAPlatformConfig(PlatformConfig):
  def init(self):
    pass


class CAR(Platforms):
  VOLVO_XC40_RECHARGE = VolvoCMAPlatformConfig(
    [VolvoCarDocs("Volvo XC40 Recharge 2021-2023")],
    CarSpecs(
      mass=2170,
      wheelbase=2.702,
      steerRatio=15.8,
      centerToFrontRatio=0.52,
    ),
    dbc_dict('volvo_front_1_cma', None, chassis_dbc='volvo_mid_1'),
  )
  POLESTAR_2 = VolvoCMAPlatformConfig(
    [VolvoCarDocs("Polestar 2 2020-2024")],
    CarSpecs(
      mass=2123,  # Long Range Dual Motor variant
      wheelbase=2.735,
      steerRatio=15.8,  # Same as XC40 (CMA platform)
      centerToFrontRatio=0.52,
    ),
    dbc_dict('volvo_front_1_cma', None, chassis_dbc='volvo_mid_1'),
  )
  #TODO update car specs
  VOLVO_S60_RECHARGE = VolvoSPAPlatformConfig(
    [VolvoCarDocs("Volvo S60 Recharge 2024")],
    CarSpecs(
      mass=2170,
      wheelbase=2.702,
      steerRatio=15.8,
      centerToFrontRatio=0.52,
    ),
    dbc_dict('volvo_front_1_spa', None, chassis_dbc='volvo_mid_1'),
  )


# FW Query configuration for Volvo CMA platform
# FW_QUERY_CONFIG = FwQueryConfig(
#   requests=[
#     Request(
#       [StdQueries.TESTER_PRESENT_REQUEST, StdQueries.UDS_VERSION_REQUEST],
#       [StdQueries.TESTER_PRESENT_RESPONSE, StdQueries.UDS_VERSION_RESPONSE],
#       bus=0,
#     ),
#   ],
# )
FW_QUERY_CONFIG = FwQueryConfig(
  requests=[]
)

DBC = CAR.create_dbc_map()

import math
from WonderPy.core.wwConstants import WWRobotConstants
from .wwSensorBase import WWSensorBase
from WonderPy.util import wwMath

_rcv = WWRobotConstants.RobotComponentValues
_expected_json_fields = (
    _rcv.WW_SENSOR_VALUE_ATTITUDE_ROLL,
    _rcv.WW_SENSOR_VALUE_ATTITUDE_PITCH,
)


class WWSensorAttitude(WWSensorBase):
    """
    Measures the robot's current estimated attitude (roll and pitch). Units are
    in degrees.
    """

    def __init__(self, robot):
        super(WWSensorAttitude, self).__init__(robot)
        self._roll = 0
        self._pitch = 0

    def _important_field_names(self):
        return 'roll', 'pitch'

    @property
    def roll(self):
        return self._roll

    @property
    def pitch(self):
        return self._pitch

    def parse(self, single_component_dictionary):
        if not self.check_fields_exist(single_component_dictionary, _expected_json_fields):
            return

        roll = single_component_dictionary[_rcv.WW_SENSOR_VALUE_ATTITUDE_ROLL]
        pitch = single_component_dictionary[_rcv.WW_SENSOR_VALUE_ATTITUDE_PITCH]

        self._roll = roll
        self._pitch = pitch

        self._valid = True


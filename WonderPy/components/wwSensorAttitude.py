import math
from WonderPy.core.wwConstants import WWRobotConstants
from .wwSensorBase import WWSensorBase
from WonderPy.util import wwMath

_rcv = WWRobotConstants.RobotComponentValues
_expected_json_fields = (
    _rcv.WW_SENSOR_VALUE_ATTITUDE_ROLL,
    _rcv.WW_SENSOR_VALUE_ATTITUDE_PITCH,
    _rcv.WW_SENSOR_VALUE_ATTITUDE_SLOPE,
    _rcv.WW_SENSOR_VALUE_ATTITUDE_ROLL_TYPE,
    _rcv.WW_SENSOR_VALUE_ATTITUDE_PITCH_TYPE,
    _rcv.WW_SENSOR_VALUE_ATTITUDE_SLOPE_TYPE,
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
        self._slope = 0
    
        self._roll_type = 0
        self._pitch_type = 0
        self._slope_type = 0

    def _important_field_names(self):
        return 'roll', 'pitch', 'slope', 'roll_type', 'pitch_type', 'slope_type'

    @property
    def roll(self):
        return self._roll

    @property
    def pitch(self):
        return self._pitch

    @property
    def slope(self):
        return self._slope

    @property
    def roll_type(self):
        return self._roll_type

    @property
    def pitch_type(self):
        return self._pitch_type

    @property
    def slope_type(self):
        return self._slope_type

    def parse(self, single_component_dictionary):
        if not self.check_fields_exist(single_component_dictionary, _expected_json_fields):
            return

        roll = single_component_dictionary[_rcv.WW_SENSOR_VALUE_ATTITUDE_ROLL]
        self._roll = roll

        pitch = single_component_dictionary[_rcv.WW_SENSOR_VALUE_ATTITUDE_PITCH]
        self._pitch = pitch

        slope = single_component_dictionary[_rcv.WW_SENSOR_VALUE_ATTITUDE_SLOPE]
        self._slope = slope

        roll_type = single_component_dictionary[_rcv.WW_SENSOR_VALUE_ATTITUDE_ROLL_TYPE]
        self._roll_type = roll_type

        pitch_type = single_component_dictionary[_rcv.WW_SENSOR_VALUE_ATTITUDE_PITCH_TYPE]
        self._pitch_type = pitch_type

        slope_type = single_component_dictionary[_rcv.WW_SENSOR_VALUE_ATTITUDE_SLOPE_TYPE]
        self._slope_type = slope_type

        self._valid = True


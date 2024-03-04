import logging
from dataclasses import dataclass
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder, Endian
from custom_components.solax_modbus.const import *

_LOGGER = logging.getLogger(__name__)

ALLDEFAULT = 0

@dataclass
class SolintegModbusButtonEntityDescription(BaseModbusButtonEntityDescription):
    allowedtypes: int = ALLDEFAULT # maybe 0x0000 (nothing) is a better default choice

@dataclass
class SolintegModbusNumberEntityDescription(BaseModbusNumberEntityDescription):
    allowedtypes: int = ALLDEFAULT # maybe 0x0000 (nothing) is a better default choice

@dataclass
class SolintegModbusSelectEntityDescription(BaseModbusSelectEntityDescription):
    allowedtypes: int = ALLDEFAULT # maybe 0x0000 (nothing) is a better default choice
    unit = REGISTER_U16

@dataclass
class SolintegModbusSensorEntityDescription(BaseModbusSensorEntityDescription):
    """A class that describes Solinteg Modbus sensor entities."""
    allowedtypes: int = ALLDEFAULT # maybe 0x0000 (nothing) is a better default choice
    order16: int = Endian.BIG
    order32: int = Endian.BIG
    unit: int = REGISTER_U16
    register_type: int= REG_HOLDING

BUTTON_TYPES = []

MAX_CURRENTS = []

SELECT_TYPES = []

NUMBER_TYPES = []

SENSOR_TYPES: list[SolintegModbusSensorEntityDescription] = [
    SolintegModbusSensorEntityDescription(
        name="Serial Number",
        key="serial_number",
        ignore_readerror = True,
        register_type=REG_INPUT,
        register=10000,
        unit=REGISTER_STR,
        wordcount = 8,
        entity_category = EntityCategory.DIAGNOSTIC,
        icon = "mdi:information",
    ),
    # Firmware version master (10011)
    SolintegModbusSensorEntityDescription(
        name="Firmware Version (master)",
        key="firmware_version_master",
        ignore_readerror = True,
        register_type=REG_INPUT,
        register=10011,
        unit=REGISTER_U32,
        entity_category = EntityCategory.DIAGNOSTIC,
        icon = "mdi:information",
    ),
    # Firmware version slave (10013)
    SolintegModbusSensorEntityDescription(
        name="Firmware Version (slave)",
        key="firmware_version_slave",
        ignore_readerror = True,
        register_type=REG_INPUT,
        register=10013,
        unit=REGISTER_U32,
        entity_category = EntityCategory.DIAGNOSTIC,
        icon = "mdi:information",
    ),
    # Skip RTC for now
    # Skip safety code for now
    # Inverter working status (10105)
    SolintegModbusSelectEntityDescription(
        name="Inverter Status",
        key="inverter_status",
        register=10105,        
        option_dict = {
            0: "Wait For Grid Connection",
            1: "Self-checking",
            2: "On-grid Generating",
            3: "Device fault",
            4: "Firmware Upgrade",
            5: "Off-grid Generating",
        },
        icon = "mdi:dip-switch",
    ),
    # Fault flag1 (10112) U32
    # TODO parse bits of error flags
    SolintegModbusSensorEntityDescription(
        name="Fault Flag 1",
        key="fault_flag1",
        register=10112,
        unit=REGISTER_U32,
        entity_category = EntityCategory.DIAGNOSTIC,
        icon = "mdi:alert",
    ),
    # Fault flag2 (10114) U32
    # TODO parse bits of error flags
    SolintegModbusSensorEntityDescription(
        name="Fault Flag 2",
        key="fault_flag2",
        register=10114,
        unit=REGISTER_U32,
        entity_category = EntityCategory.DIAGNOSTIC,
        icon = "mdi:alert",
    ),
    # Fault flag3 (10116) U32
    # TODO parse bits of error flags
    SolintegModbusSensorEntityDescription(
        name="Fault Flag 3",
        key="fault_flag3",
        register=10116,
        unit=REGISTER_U32,
        entity_category = EntityCategory.DIAGNOSTIC,
        icon = "mdi:alert",
    ),
    # PV1 voltage (11038)
    SolintegModbusNumberEntityDescription(
        name="PV1 Voltage",
        key="pv1_voltage",
        native_unit_of_measurement = UnitOfElectricPotential.VOLT,
        device_class = SensorDeviceClass.VOLTAGE,
        register=11038,
        unit = REGISTER_U16,
        scale = 0.1,
    ),
    # PV1 current (11039)
    SolintegModbusNumberEntityDescription(
        name="PV1 Current",
        key="pv1_current",
        native_unit_of_measurement = UnitOfElectricCurrent.AMPERE,
        device_class = SensorDeviceClass.CURRENT,
        register=11039,
        unit = REGISTER_U16,
        scale = 0.1,
        icon = "mdi:current-dc",
    ),
    # PV2 voltage (11040)
    SolintegModbusNumberEntityDescription(
        name="PV2 Voltage",
        key="pv2_voltage",
        native_unit_of_measurement = UnitOfElectricPotential.VOLT,
        device_class = SensorDeviceClass.VOLTAGE,
        register=11040,
        unit = REGISTER_U16,
        scale = 0.1,
    ),
    # PV2 current (11041)
    SolintegModbusNumberEntityDescription(
        name="PV2 Current",
        key="pv2_current",
        native_unit_of_measurement = UnitOfElectricCurrent.AMPERE,
        device_class = SensorDeviceClass.CURRENT,
        register=11041,
        unit = REGISTER_U16,
        scale = 0.1,
        icon = "mdi:current-dc",
    ),
]

@dataclass
class solinteg_plugin(plugin_base):
    async def async_determineInverterType(self, hub, configdict):
        invertertype = ALLDEFAULT
        return invertertype

plugin_instance = solinteg_plugin(
    plugin_name = 'Solinteg',
    plugin_manufacturer = 'Solinteg',
    SENSOR_TYPES = SENSOR_TYPES,
    NUMBER_TYPES = NUMBER_TYPES,
    BUTTON_TYPES = BUTTON_TYPES,
    SELECT_TYPES = SELECT_TYPES,
    block_size = 100,
    order16 = Endian.BIG,
    order32 = Endian.LITTLE,
    auto_block_ignore_readerror = True,
)
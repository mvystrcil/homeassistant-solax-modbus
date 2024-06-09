import logging
from dataclasses import dataclass
from homeassistant.components.number import NumberEntityDescription
from homeassistant.components.select import SelectEntityDescription
from homeassistant.components.button import ButtonEntityDescription
from pymodbus.payload import BinaryPayloadBuilder, BinaryPayloadDecoder, Endian
from custom_components.solax_modbus.const import *

_LOGGER = logging.getLogger(__name__)

ALLDEFAULT = 0

# Inverter type
HYBRID  = 0x1000

# Constants - number of phases
X1      = 0x0100
X3      = 0x0200

# Constant for model type parsing
HYBRID_3F_DUAL_MPPT = 0x3000

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

def value_function_remotecontrol_recompute(initval, descr, datadict):
    _LOGGER.info("Recompute called")
    pass

BUTTON_TYPES = [
    # Start trigger command
    SolintegModbusButtonEntityDescription(
        name = "EMC controll",
        key = "ems_controll_trigger",
        register = 0x7C,
        #command = 0,
        allowedtypes = HYBRID,
        write_method = WRITE_MULTI_MODBUS,
        icon = "mdi:battery-clock",
        value_function = value_function_remotecontrol_recompute,
        autorepeat = "remotecontrol_autorepeat_duration"
    ),
]

MAX_CURRENTS = []

SELECT_TYPES = [
    # Enable grid injenction
    SolintegModbusSelectEntityDescription(
        name = "Grid Injenction Power Limit",
        key = "grid_injenction_power_limit",
        register = 25100,
        unit = REGISTER_U16,
        option_dict =  {
                0: "Disabled",
                1: "Enabled",
            },
        allowedtypes = HYBRID,
        entity_category = EntityCategory.CONFIG,
        icon = "mdi:transmission-tower-import",
    ),
     # Battery off-grid SOC battery protection
    SolintegModbusSelectEntityDescription(
        name = "Inverter working mode",
        key = "inverter_working_mode",
        register = 50000,
        option_dict = {
            0x0101: "General Mode",
            0x0102: "Economic Mode",
            0x0103: "UPS Mode",
            0x0200: "Off Grid Mode",
            0x0301: "EMS AC Ctrl Mode",
            0x0302: "EMS General Mode",
            0x0303: "EMS Battery Mode",
            0x0304: "EMS Off Grid Mode",
            },
        unit = REGISTER_U16,
        allowedtypes = HYBRID,
        entity_category = EntityCategory.CONFIG,
        icon = "mdi:home-lightning-bolt",
    ),
    # UPS function switch
    SolintegModbusSelectEntityDescription(
        name = "UPS Function Switch",
        key = "ups_function_switch",
        register = 50001,
        option_dict = {
            0: "Disabled",
            1: "Enabled",
            },
        unit = REGISTER_U16,
        allowedtypes = HYBRID,
        entity_category = EntityCategory.CONFIG,
        icon = "mdi:power-plug-battery",
    ),
    # Battery on-grid SOC battery protection
    SolintegModbusSelectEntityDescription(
        name = "Battery SOC on-grid protection",
        key = "battery_soc_on_grid_protection",
        register = 52502,
        option_dict = {
            0: "Off",
            1: "On",
            },
        unit = REGISTER_U16,
        allowedtypes = HYBRID,
        icon = "mdi:battery-plus-variant",
    ),
    # Battery off-grid SOC battery protection
    SolintegModbusSelectEntityDescription(
        name = "Battery SOC off-grid protection",
        key = "battery_soc_off_grid_protection",
        register = 52504,
        option_dict = {
            0: "Off",
            1: "On",
            },
        unit = REGISTER_U16,
        allowedtypes = HYBRID,
        icon = "mdi:battery-plus-variant",
    ),

]

NUMBER_TYPES = [
    # Local number data
    SolintegModbusNumberEntityDescription(
        name = "Remotecontrol Autorepeat Duration",
        key = "remotecontrol_autorepeat_duration",
        unit = REGISTER_U16,
        allowedtypes =  HYBRID,
        icon = "mdi:home-clock",
        initvalue = 0, # seconds -
        native_min_value = 0,
        native_max_value = 28800,
        native_step = 600,
        fmt = "i",
        native_unit_of_measurement = UnitOfTime.SECONDS,
        write_method = WRITE_DATA_LOCAL,
    ),
    # Device number data

    # Set grid injection percentage
    SolintegModbusNumberEntityDescription(
        name = "Grid Injection Power Limit Settings",
        key = "grid_injenction_power_limit_settings",
        register = 25101,
        unit = REGISTER_U32,
        fmt = "i",
        native_min_value = 0,
        native_max_value = 100000,
        native_step = 1,
        native_unit_of_measurement = UnitOfPower.WATT,
        allowedtypes = HYBRID,
        icon = "mdi:transmission-tower-import",
    ),

    # Settings of grid injenction power
    SolintegModbusNumberEntityDescription(
        name = "Grid Injection Power Limit Settings %",
        key = "grid_injenction_power_limit_settings_percent",
        register = 25103,
        unit = REGISTER_U16,
        fmt = "i",
        native_min_value = 0,
        native_max_value = 100000,
        native_step = 1,
        native_unit_of_measurement = PERCENTAGE,
        scale = 0.1,
        allowedtypes = HYBRID,
        icon = "mdi:transmission-tower-export",
    ),

    # Set on-grid SOC battery end
    SolintegModbusNumberEntityDescription(
        name = "Battery SOC on-grid end",
        key = "battery_soc_on_grid_end",
        register = 52503,
        unit = REGISTER_U16,
        fmt = "i",
        native_min_value = 10,
        native_max_value = 10000,
        native_step = 1,
        #native_unit_of_measurement = PERCENTAGE,
        #scale = 0.001,
        allowedtypes = HYBRID,
        icon = "mdi:battery-30",
    ),
    # Set off-grid SOC battery end
    SolintegModbusNumberEntityDescription(
        name = "Battery SOC off-grid end",
        key = "battery_soc_off_grid_end",
        register = 52505,
        unit = REGISTER_U16,
        fmt = "i",
        native_min_value = 10,
        native_max_value = 100,
        native_step = 1,
        native_unit_of_measurement = PERCENTAGE,
        scale = 0.001,
        allowedtypes = HYBRID,
        icon = "mdi:battery-10",
    ),
]

SENSOR_TYPES: list[SolintegModbusSensorEntityDescription] = [
#    # Serial number
#    SolintegModbusSensorEntityDescription(
#        name = "Serial Number",
#        key = "serial_number",
#        register = 10000,
#        unit = REGISTER_STR,
#        wordcount=8,
#        #entity_registry_enabled_default = False,
#        allowedtypes = HYBRID,
#        entity_category = EntityCategory.DIAGNOSTIC,
#        icon = "mdi:information",
#    ),

    # Inverter model
    SolintegModbusSensorEntityDescription(
        name="Inverter model",
        key="inverter_model",
        entity_category = EntityCategory.DIAGNOSTIC,
        register=10008,
        unit = REGISTER_U16,
        allowedtypes=HYBRID,
        icon = "mdi:information",
    ),
    # Inverter working status
    SolintegModbusSensorEntityDescription(
        name = "Inverter working status",
        key = "inverter_working_status",
        entity_category = EntityCategory.DIAGNOSTIC,
        register = 10105,
        scale = {
            0: "Waiting for grid connection",
            1: "Self-checking",
            2: "On-grid generating",
            3: "Device fault",
            4: "Firmware upgrade",
            5: "Off-grid generating",
            },
        allowedtypes = HYBRID,
        icon = "mdi:dip-switch",
    ),
    # Power consumption on phase 1
    SolintegModbusSensorEntityDescription(
        name="Grid phase 1 power",
        key="grid_phase_1_power",
        native_unit_of_measurement = UnitOfPower.WATT,
        device_class = SensorDeviceClass.POWER,
        state_class = SensorStateClass.MEASUREMENT,
        register=10994,
        #scale = 0.001,
        unit = REGISTER_S32,
        allowedtypes=HYBRID,
    ),
    # Power consumption on phase 2
    SolintegModbusSensorEntityDescription(
        name="Grid phase 2 power",
        key="grid_phase_2_power",
        native_unit_of_measurement = UnitOfPower.WATT,
        device_class = SensorDeviceClass.POWER,
        state_class = SensorStateClass.MEASUREMENT,
        register=10996,
        #scale = 0.001,
        unit = REGISTER_S32,
        allowedtypes=HYBRID,
    ),
    # Power consumption on phase 3
    SolintegModbusSensorEntityDescription(
        name="Grid phase 3 power",
        key="grid_phase_3_power",
        native_unit_of_measurement = UnitOfPower.WATT,
        device_class = SensorDeviceClass.POWER,
        state_class = SensorStateClass.MEASUREMENT,
        register=10998,
        #scale = 0.001,
        unit = REGISTER_S32,
        allowedtypes=HYBRID,
    ),
    # Total power consumption
    SolintegModbusSensorEntityDescription(
        name="Total grid power",
        key="total_grid_power",
        native_unit_of_measurement = UnitOfPower.WATT,
        device_class = SensorDeviceClass.POWER,
        state_class = SensorStateClass.MEASUREMENT,
        register=11000,
        #scale = 0.001,
        unit = REGISTER_S32,
        allowedtypes=HYBRID,
    ),
    # Total grid injenction
    SolintegModbusSensorEntityDescription(
        name="Total grid injenction",
        key="total_grid_injenction",
        native_unit_of_measurement = UnitOfPower.WATT,
        device_class = SensorDeviceClass.POWER,
        state_class = SensorStateClass.MEASUREMENT,
        register=11002,
        #scale = 0.001,
        unit = REGISTER_U32,
        allowedtypes=HYBRID,
    ),
    # Total purchasing energy
    SolintegModbusSensorEntityDescription(
        name="Total purchasing energy",
        key="total_purchasing_energy",
        native_unit_of_measurement = UnitOfPower.WATT,
        device_class = SensorDeviceClass.POWER,
        state_class = SensorStateClass.MEASUREMENT,
        register=11004,
        #scale = 0.001,
        unit = REGISTER_U32,
        allowedtypes=HYBRID,
    ),
    # Energy today
    SolintegModbusSensorEntityDescription(
        name="Energy today",
        key="energy_today",
        native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR,
        device_class = SensorDeviceClass.ENERGY,
        register=11018,
        unit = REGISTER_U32,
        scale = 0.1,
        rounding = 1,
        allowedtypes=HYBRID,
    ),
    # Energy total
    SolintegModbusSensorEntityDescription(
        name="Energy total",
        key="energy_total",
        native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR,
        device_class = SensorDeviceClass.ENERGY,
        register=11020,
        unit = REGISTER_U32,
        scale = 0.1,
        rounding = 1,
        allowedtypes=HYBRID,
    ),
    # Total PV Input power
    SolintegModbusSensorEntityDescription(
        name="PV total",
        key="pv_total",
        native_unit_of_measurement = UnitOfPower.WATT,
        device_class = SensorDeviceClass.POWER,
        state_class = SensorStateClass.MEASUREMENT,
        register=11028,
        unit = REGISTER_U32,
        #scale = 0.001,
        rounding = 0,
        allowedtypes=HYBRID,
    ),
    # PV1 voltage (11038)
    SolintegModbusSensorEntityDescription(
        name="PV1 Voltage",
        key="pv1_voltage",
        native_unit_of_measurement = UnitOfElectricPotential.VOLT,
        device_class = SensorDeviceClass.VOLTAGE,
        register=11038,
        unit = REGISTER_U16,
        scale = 0.1,
        allowedtypes=HYBRID,
    ),
    # PV1 current (11039)
    SolintegModbusSensorEntityDescription(
        name="PV1 Current",
        key="pv1_current",
        native_unit_of_measurement = UnitOfElectricCurrent.AMPERE,
        device_class = SensorDeviceClass.CURRENT,
        register=11039,
        unit = REGISTER_U16,
        scale = 0.1,
        icon = "mdi:current-dc",
        allowedtypes=HYBRID,
    ),
    # PV2 voltage (11040)
    SolintegModbusSensorEntityDescription(
        name="PV2 Voltage",
        key="pv2_voltage",
        native_unit_of_measurement = UnitOfElectricPotential.VOLT,
        device_class = SensorDeviceClass.VOLTAGE,
        register_type=REG_HOLDING,
        register=11040,
        unit = REGISTER_U16,
        scale = 0.1,
        allowedtypes=HYBRID,
    ),
    # PV2 current (11041)
    SolintegModbusSensorEntityDescription(
        name="PV2 Current",
        key="pv2_current",
        native_unit_of_measurement = UnitOfElectricCurrent.AMPERE,
        device_class = SensorDeviceClass.CURRENT,
        register_type=REG_HOLDING,
        register=11041,
        unit = REGISTER_U16,
        scale = 0.1,
        allowedtypes=HYBRID,
        icon = "mdi:current-dc",
    ),
    # PV1 Input power
    SolintegModbusSensorEntityDescription(
        name="PV1 power",
        key="pv1_input_power",
        native_unit_of_measurement = UnitOfPower.WATT,
        device_class = SensorDeviceClass.POWER,
        state_class = SensorStateClass.MEASUREMENT,
        register=11062,
        unit = REGISTER_U32,
        #scale = 0.001,
        allowedtypes=HYBRID,
    ),
    # PV2 Input power
    SolintegModbusSensorEntityDescription(
        name="PV2 power",
        key="pv2_input_power",
        native_unit_of_measurement = UnitOfPower.WATT,
        device_class = SensorDeviceClass.POWER,
        state_class = SensorStateClass.MEASUREMENT,
        register=11064,
        unit = REGISTER_U32,
        #scale = 0.001,
        allowedtypes=HYBRID,
    ),
    # Grid injenction power limit
    SolintegModbusSensorEntityDescription(
        name = "Grid Injenction Power Limit",
        key = "grid_injenction_power_limit",
        register = 25100,
        unit = REGISTER_U16,
        scale =  {
                0: "Disabled",
                1: "Enabled",
            },
        allowedtypes = HYBRID,
        entity_category = EntityCategory.DIAGNOSTIC,
        icon = "mdi:transmission-tower-import",
    ),
    # Settings of grid injenction power
    SolintegModbusSensorEntityDescription(
        name = "Grid Injection Power Limit Settings",
        key = "grid_injenction_power_limit_settings",
        register = 25101,
        unit = REGISTER_U32,
        native_unit_of_measurement = UnitOfPower.WATT,
        device_class = SensorDeviceClass.POWER,
        state_class = SensorStateClass.MEASUREMENT,
        allowedtypes = HYBRID,
        icon = "mdi:transmission-tower-export",
    ),
    # Settings of grid injenction power
    SolintegModbusSensorEntityDescription(
        name = "Grid Injection Power Limit Settings %",
        key = "grid_injenction_power_limit_settings_percent",
        register = 25103,
        unit = REGISTER_U16,
        native_unit_of_measurement = PERCENTAGE,
        scale = 0.1,
        allowedtypes = HYBRID,
        icon = "mdi:transmission-tower-export",
    ),
    # Backup phase 1 voltage
    SolintegModbusSensorEntityDescription(
        name="Backup phase 1 Voltage",
        key="bck_phase_1_voltage",
        native_unit_of_measurement = UnitOfElectricPotential.VOLT,
        device_class = SensorDeviceClass.VOLTAGE,
        register_type=REG_HOLDING,
        register=30200,
        unit = REGISTER_U16,
        scale = 0.1,
        allowedtypes=HYBRID,
    ),
    # Backup phase 1 current
    SolintegModbusSensorEntityDescription(
        name="Backup phase 1 Current",
        key="bck_phase_1_current",
        native_unit_of_measurement = UnitOfElectricCurrent.AMPERE,
        device_class = SensorDeviceClass.CURRENT,
        register_type=REG_HOLDING,
        register=30201,
        unit = REGISTER_U16,
        scale = 0.1,
        allowedtypes=HYBRID,
        icon = "mdi:current-dc",
    ),
    # Backup phase 1 frequency
    SolintegModbusSensorEntityDescription(
        name="Backup phase 1 Frequency",
        key="bck_phase_1_frequency",
        native_unit_of_measurement = UnitOfFrequency.HERTZ,
        state_class = SensorStateClass.MEASUREMENT,
        register_type=REG_HOLDING,
        register=30202,
        unit = REGISTER_U16,
        scale = 0.01,
        rounding = 1,
        allowedtypes=HYBRID,
    ),
    # Backup phase 1 power
    SolintegModbusSensorEntityDescription(
        name="Backup phase 1 Power",
        key="bck_phase_1_power",
        native_unit_of_measurement = UnitOfPower.WATT,
        device_class = SensorDeviceClass.POWER,
        state_class = SensorStateClass.MEASUREMENT,
        register_type=REG_HOLDING,
        register=30204,
        unit = REGISTER_S32,
        #scale = 0.001,
        allowedtypes=HYBRID,
    ),
    # Backup phase 2 voltage
    SolintegModbusSensorEntityDescription(
        name="Backup phase 2 Voltage",
        key="bck_phase_2_voltage",
        native_unit_of_measurement = UnitOfElectricPotential.VOLT,
        device_class = SensorDeviceClass.VOLTAGE,
        register_type=REG_HOLDING,
        register=30210,
        unit = REGISTER_U16,
        scale = 0.1,
        allowedtypes=HYBRID,
    ),
    # Backup phase 2 current
    SolintegModbusSensorEntityDescription(
        name="Backup phase 2 Current",
        key="bck_phase_2_current",
        native_unit_of_measurement = UnitOfElectricCurrent.AMPERE,
        device_class = SensorDeviceClass.CURRENT,
        register_type=REG_HOLDING,
        register=30211,
        unit = REGISTER_U16,
        scale = 0.1,
        allowedtypes=HYBRID,
        icon = "mdi:current-dc",
    ),
    # Backup phase 2 frequency
    SolintegModbusSensorEntityDescription(
        name="Backup phase 2 Frequency",
        key="bck_phase_2_frequency",
        native_unit_of_measurement = UnitOfFrequency.HERTZ,
        state_class = SensorStateClass.MEASUREMENT,
        register_type=REG_HOLDING,
        register=30212,
        unit = REGISTER_U16,
        scale = 0.01,
        rounding = 1,
        allowedtypes=HYBRID,
    ),
    # Backup phase 2 power
    SolintegModbusSensorEntityDescription(
        name="Backup phase 2 Power",
        key="bck_phase_2_power",
        native_unit_of_measurement = UnitOfPower.WATT,
        device_class = SensorDeviceClass.POWER,
        state_class = SensorStateClass.MEASUREMENT,
        register_type=REG_HOLDING,
        register=30214,
        unit = REGISTER_S32,
        #scale = 0.001,
        allowedtypes=HYBRID,
    ),
    # Backup phase 3 voltage
    SolintegModbusSensorEntityDescription(
        name="Backup phase 3 Voltage",
        key="bck_phase_3_voltage",
        native_unit_of_measurement = UnitOfElectricPotential.VOLT,
        device_class = SensorDeviceClass.VOLTAGE,
        register_type=REG_HOLDING,
        register=30220,
        unit = REGISTER_U16,
        scale = 0.1,
        allowedtypes=HYBRID,
    ),
    # Backup phase 3 current
    SolintegModbusSensorEntityDescription(
        name="Backup phase 3 Current",
        key="bck_phase_3_current",
        native_unit_of_measurement = UnitOfElectricCurrent.AMPERE,
        device_class = SensorDeviceClass.CURRENT,
        register_type=REG_HOLDING,
        register=30221,
        unit = REGISTER_U16,
        scale = 0.1,
        allowedtypes=HYBRID,
        icon = "mdi:current-dc",
    ),
    # Backup phase 3 frequency
    SolintegModbusSensorEntityDescription(
        name="Backup phase 3 Frequency",
        key="bck_phase_3_frequency",
        native_unit_of_measurement = UnitOfFrequency.HERTZ,
        state_class = SensorStateClass.MEASUREMENT,
        register_type=REG_HOLDING,
        register=30222,
        unit = REGISTER_U16,
        scale = 0.01,
        rounding = 1,
        allowedtypes=HYBRID,
    ),
    # Backup phase 3 power
    SolintegModbusSensorEntityDescription(
        name="Backup phase 3 Power",
        key="bck_phase_3_power",
        native_unit_of_measurement = UnitOfPower.WATT,
        device_class = SensorDeviceClass.POWER,
        state_class = SensorStateClass.MEASUREMENT,
        register_type=REG_HOLDING,
        register=30224,
        unit = REGISTER_S32,
        #scale = 0.001,
        allowedtypes=HYBRID,
    ),
    # Total Backup power
    SolintegModbusSensorEntityDescription(
        name="Total Backup Power",
        key="total_backup_power",
        native_unit_of_measurement = UnitOfPower.WATT,
        device_class = SensorDeviceClass.POWER,
        state_class = SensorStateClass.MEASUREMENT,
        register_type=REG_HOLDING,
        register=30230,
        unit = REGISTER_S32,
        #scale = 0.001,
        allowedtypes=HYBRID,
    ),
    # Battery voltage
    SolintegModbusSensorEntityDescription(
        name="Battery voltage",
        key="battery_voltage",
        native_unit_of_measurement = UnitOfElectricPotential.VOLT,
        device_class = SensorDeviceClass.VOLTAGE,
        register_type=REG_HOLDING,
        register=30254,
        unit = REGISTER_U16,
        scale = 0.1,
        allowedtypes=HYBRID,
    ),
    # Battery current
    SolintegModbusSensorEntityDescription(
        name="Battery current",
        key="battery_current",
        native_unit_of_measurement = UnitOfElectricCurrent.AMPERE,
        device_class = SensorDeviceClass.CURRENT,
        register_type=REG_HOLDING,
        register=30255,
        unit = REGISTER_S16,
        scale = 0.1,
        allowedtypes=HYBRID,
        icon = "mdi:current-dc",
    ),
    # Battery mode
    SolintegModbusSensorEntityDescription(
        name="Battery mode",
        key="battery_mode",
        entity_category = EntityCategory.DIAGNOSTIC,
        register = 30256,
        scale = {
            0: "Discharge",
            1: "Charge",
            },
        allowedtypes = HYBRID,
        icon = "mdi:dip-switch",
    ),
    # Battery power
    SolintegModbusSensorEntityDescription(
        name="Battery power",
        key="battery_power",
        native_unit_of_measurement = UnitOfPower.WATT,
        device_class = SensorDeviceClass.POWER,
        state_class = SensorStateClass.MEASUREMENT,
        register_type=REG_HOLDING,
        register=30258,
        unit = REGISTER_S32,
        #scale = 0.001,
        allowedtypes=HYBRID,
    ),
    # Daily Energy Injected to Grid
    SolintegModbusSensorEntityDescription(
        name="Daily Energy Injected to Grid",
        key="daily_energy_injected_to_grid",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        register_type=REG_HOLDING,
        register=31000,
        unit=REGISTER_U16,
        scale=0.1,
        rounding = 1,
        allowedtypes=HYBRID,
    ),
    # Daily Purchased Energy
    SolintegModbusSensorEntityDescription(
        name="Daily Purchased Energy",
        key="daily_purchased_energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        register_type=REG_HOLDING,
        register=31001,
        unit=REGISTER_U16,
        scale=0.1,
        rounding = 1,
        allowedtypes=HYBRID,
    ),
    # Daily Energy Output on Backup Port
    SolintegModbusSensorEntityDescription(
        name="Daily Energy Output on Backup Port",
        key="daily_energy_output_on_backup_port",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        register_type=REG_HOLDING,
        register=31002,
        unit=REGISTER_U16,
        scale=0.1,
        rounding = 1,
        allowedtypes=HYBRID,
    ),
    # Daily Battery Charging Energy
    SolintegModbusSensorEntityDescription(
        name="Daily Battery Charging Energy",
        key="daily_battery_charging_energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        register_type=REG_HOLDING,
        register=31003,
        unit=REGISTER_U16,
        scale=0.1,
        rounding = 1,
        allowedtypes=HYBRID,
    ),
    # Daily Battery Discharging Energy
    SolintegModbusSensorEntityDescription(
        name="Daily Battery Discharging Energy",
        key="daily_battery_discharging_energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        register_type=REG_HOLDING,
        register=31004,
        unit=REGISTER_U16,
        scale=0.1,
        rounding = 1,
        allowedtypes=HYBRID,
    ),
    # Daily PV Generation
    SolintegModbusSensorEntityDescription(
        name="Daily PV Generation",
        key="daily_pv_generation",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        register_type=REG_HOLDING,
        register=31005,
        unit=REGISTER_U16,
        scale=0.1,
        rounding = 1,
        allowedtypes=HYBRID,
    ),
    # Daily Load Consumption
    SolintegModbusSensorEntityDescription(
        name="Daily Load Consumption",
        key="daily_load_consumption",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        register_type=REG_HOLDING,
        register=31006,
        unit=REGISTER_U16,
        scale=0.1,
        rounding = 1,
        allowedtypes=HYBRID,
    ),
    # Daily Energy Purchased from Grid at Inverter Side
    SolintegModbusSensorEntityDescription(
        name="Daily Energy Purchased from Grid at Inverter Side",
        key="daily_energy_purchased_from_grid_at_inverter_side",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        register_type=REG_HOLDING,
        register=31008,
        unit=REGISTER_U16,
        scale=0.1,
        rounding = 1,
        allowedtypes=HYBRID,
    ),
    # Total energy injected to grid
    SolintegModbusSensorEntityDescription(
        name="Total energy injected to grid",
        key="total_energy_injected_to_grid",
        native_unit_of_measurement = UnitOfEnergy.KILO_WATT_HOUR,
        device_class = SensorDeviceClass.ENERGY,
        state_class = SensorStateClass.TOTAL_INCREASING,
        register_type=REG_HOLDING,
        register=31102,
        unit = REGISTER_U32,
        scale = 0.1,
        rounding = 1,
        allowedtypes=HYBRID,
    ),
    # Total purchased energy from grid
    SolintegModbusSensorEntityDescription(
        name="Total purchased energy from grid",
        key="total_purchased_energy_from_grid",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class = SensorStateClass.TOTAL_INCREASING,
        register_type=REG_HOLDING,
        register=31104,
        unit=REGISTER_U32,
        scale=0.1,
        rounding = 1,
        allowedtypes=HYBRID,
    ),
    # Total output energy on backup port
    SolintegModbusSensorEntityDescription(
        name="Total output energy on backup port",
        key="total_output_energy_on_backup_port",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class = SensorStateClass.TOTAL_INCREASING,
        register_type=REG_HOLDING,
        register=31106,
        unit=REGISTER_U32,
        scale=0.1,
        rounding = 1,
        allowedtypes=HYBRID,
    ),
    # Total battery charging energy
    SolintegModbusSensorEntityDescription(
        name="Total battery charging energy",
        key="total_battery_charging_energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class = SensorStateClass.TOTAL_INCREASING,
        register_type=REG_HOLDING,
        register=31108,
        unit=REGISTER_U32,
        scale=0.1,
        rounding = 1,
        allowedtypes=HYBRID,
    ),
    # Total battery discharging energy
    SolintegModbusSensorEntityDescription(
        name="Total battery discharging energy",
        key="total_battery_discharging_energy",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class = SensorStateClass.TOTAL_INCREASING,
        register_type=REG_HOLDING,
        register=31110,
        unit=REGISTER_U32,
        scale=0.1,
        rounding = 1,
        allowedtypes=HYBRID,
    ),
    # Total PV generation
    SolintegModbusSensorEntityDescription(
        name="Total PV generation",
        key="total_pv_generation",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class = SensorStateClass.TOTAL_INCREASING,
        register_type=REG_HOLDING,
        register=31112,
        unit=REGISTER_U32,
        scale=0.1,
        rounding = 0,
        allowedtypes=HYBRID,
    ),
    # Total load consumption
    SolintegModbusSensorEntityDescription(
        name="Total load consumption",
        key="total_load_consumption",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class = SensorStateClass.TOTAL_INCREASING,
        register_type=REG_HOLDING,
        register=31114,
        unit=REGISTER_U32,
        scale=0.1,
        rounding = 1,
        allowedtypes=HYBRID,
    ),
    # Total energy purchased from grid at inverter side
    SolintegModbusSensorEntityDescription(
        name="Total energy purchased from grid at inverter side",
        key="total_energy_purchased_from_grid_at_inverter_side",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class = SensorStateClass.TOTAL_INCREASING,
        register_type=REG_HOLDING,
        register=31118,
        unit=REGISTER_U32,
        scale=0.1,
        rounding = 1,
        allowedtypes=HYBRID,
    ),
    # Battery SOC
    SolintegModbusSensorEntityDescription(
        name="Battery SOC",
        key="battery_soc",
        native_unit_of_measurement = PERCENTAGE,
        register_type=REG_HOLDING,
        register=33000,
        unit=REGISTER_U16,
        scale=0.01,
        allowedtypes=HYBRID,
        icon = "mdi:battery-sync",
    ),
    # Battery SOH
    SolintegModbusSensorEntityDescription(
        name="Battery SOH",
        key="battery_soh",
        native_unit_of_measurement = PERCENTAGE,
        entity_category = EntityCategory.DIAGNOSTIC,
        register_type=REG_HOLDING,
        register=33001,
        unit=REGISTER_U16,
        scale=0.01,
        allowedtypes=HYBRID,
        icon = "mdi:battery-heart-variant",
    ),
    # BMS tempearature
    SolintegModbusSensorEntityDescription(
        name="BMS pack temperature",
        key="bms_pack_temperature",
        native_unit_of_measurement = UnitOfTemperature.CELSIUS,
        device_class = SensorDeviceClass.TEMPERATURE,
        state_class = SensorStateClass.MEASUREMENT,
        entity_category = EntityCategory.DIAGNOSTIC,
        register_type=REG_HOLDING,
        register=33003,
        unit=REGISTER_U16,
        scale=0.1,
        allowedtypes=HYBRID,
        icon = "mdi:battery-sync",
    ),
    # Battery off-grid SOC battery protection
    SolintegModbusSensorEntityDescription(
        name = "Inverter working mode",
        key = "inverter_working_mode",
        entity_category = EntityCategory.DIAGNOSTIC,
        register = 50000,
        scale = {
            0x0101: "General Mode",
            0x0102: "Economic Mode",
            0x0103: "UPS Mode",
            0x0200: "Off Grid Mode",
            0x0301: "EMS AC Ctrl Mode",
            0x0302: "EMS General Mode",
            0x0303: "EMS Battery Mode",
            0x0304: "EMS Off Grid Mode",
            },
        unit = REGISTER_U16,
        allowedtypes = HYBRID,
        icon = "mdi:home-lightning-bolt",
    ),
    # UPS function switch
    SolintegModbusSensorEntityDescription(
        name = "UPS Function Switch",
        key = "ups_function_switch",
        entity_category = EntityCategory.DIAGNOSTIC,
        register = 50001,
        scale = {
            0: "Disabled",
            1: "Enabled",
            },
        unit = REGISTER_U16,
        allowedtypes = HYBRID,
        icon = "mdi:power-plug-battery",
    ),
    # Battery on-grid SOC battery protection
    SolintegModbusSensorEntityDescription(
        name = "Battery SOC on-grid protection",
        key = "battery_soc_on_grid_protection",
        entity_category = EntityCategory.DIAGNOSTIC,
        register = 52502,
        scale = {
            0: "Off",
            1: "On",
            },
        unit = REGISTER_U16,
        allowedtypes = HYBRID,
        icon = "mdi:battery-plus-variant",
    ),
    # Battery on-grid SOC battery end
    SolintegModbusSensorEntityDescription(
        name = "Battery SOC on-grid end",
        key = "battery_soc_on_grid_end",
        register = 52503,
        unit = REGISTER_U16,
        native_unit_of_measurement = PERCENTAGE,
        #scale=0.01,
        allowedtypes = HYBRID,
        icon = "mdi:battery-30",
    ),
    # Battery off-grid SOC battery protection
    SolintegModbusSensorEntityDescription(
        name = "Battery SOC off-grid protection",
        key = "battery_soc_off_grid_protection",
        entity_category = EntityCategory.DIAGNOSTIC,
        register = 52504,
        scale = {
            0: "Off",
            1: "On",
            },
        unit = REGISTER_U16,
        allowedtypes = HYBRID,
        icon = "mdi:battery-plus-variant",
    ),
    # Battery off-grid SOC battery end
    SolintegModbusSensorEntityDescription(
        name = "Battery SOC off-grid end",
        key = "battery_soc_off_grid_end",
        register = 52505,
        unit = REGISTER_U16,
        native_unit_of_measurement = PERCENTAGE,
        scale=0.001,
        allowedtypes = HYBRID,
        icon = "mdi:battery-10",
    ),
]

async def async_read_serialnr(hub, address):
    inverter_data = None
    try:
        inverter_data = await hub.async_read_holding_registers(unit=hub._modbus_addr, address=address, count=8)
        if not inverter_data.isError():
            decoder = BinaryPayloadDecoder.fromRegisters(inverter_data.registers, byteorder=Endian.BIG)
            res = decoder.decode_string(14).decode("ascii")
            hub.seriesnumber = res
    except Exception as ex: _LOGGER.warning(f"{hub.name}: attempt to read serialnumber failed at 0x{address:x} data: {inverter_data}", exc_info=True)
    if not res: _LOGGER.warning(f"{hub.name}: reading serial number from address 0x{address:x} failed; other address may succeed")
    _LOGGER.info(f"Read {hub.name} 0x{address:x} serial number before potential swap: {res}")
    return res

async def async_read_model(hub, address):
    inverter_data = None
    try:
        inverter_data = await hub.async_read_holding_registers(unit=hub._modbus_addr, address=address, count=8)
        if not inverter_data.isError():
            decoder = BinaryPayloadDecoder.fromRegisters(inverter_data.registers, byteorder=Endian.BIG)
            return decoder.decode_16bit_uint()
    except Exception as ex:
        _LOGGER.warning(f"{hub.name}: attempt to read inverter mode failed at 0x{address:x} data: {inverter_data}", exc_info=True)
        return None

@dataclass
class solinteg_plugin(plugin_base):
    async def async_determineInverterType(self, hub, configdict):
        _LOGGER.info(f"{hub.name}: trying to determine inverter type.")
        invertertype = ALLDEFAULT
        model = await async_read_model(hub, 10008)
        serial = await async_read_serialnr(hub, 10008)
        if not model:
            _LOGGER.info(f"{hub.name}: failed to read inverter type")
            # TODO: set inverter type to UNKNOWN
        if not serial:
            _LOGGER.info(f"{hub.name}: failed to read inverter serial")
            # TODO: read inverter serial
        _LOGGER.info(f"{hub.name}: inverter model {model}")
        if model & HYBRID_3F_DUAL_MPPT:
            invertertype = HYBRID
        return invertertype
    
    def matchInverterWithMask (self, inverterspec, entitymask, serialnumber = 'not relevant', blacklist = None):
        return True

    def localDataCallback(self, hub):
        pass

plugin_instance = solinteg_plugin(
    plugin_name = 'Solinteg',
    plugin_manufacturer = 'Solinteg',
    SENSOR_TYPES = SENSOR_TYPES,
    NUMBER_TYPES = NUMBER_TYPES,
    BUTTON_TYPES = BUTTON_TYPES,
    SELECT_TYPES = SELECT_TYPES,
    block_size = 100,
    order16 = Endian.BIG,
    order32 = Endian.BIG,
    auto_block_ignore_readerror = True,
)

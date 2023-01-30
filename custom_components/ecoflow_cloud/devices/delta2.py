from . import const, BaseDevice
from .. import EcoflowMQTTClient
from ..entities import BaseSensorEntity, BaseNumberEntity, BaseSwitchEntity, BaseSelectEntity
from ..number import LevelEntity, ChargingPowerEntity
from ..select import DictSelectEntity
from ..sensor import LevelSensorEntity, WattsSensorEntity, RemainSensorEntity, TempSensorEntity, CyclesSensorEntity, \
    FanSensorEntity
from ..switch import BeeperEntity, EnabledEntity


class Delta2(BaseDevice):
    def sensors(self, client: EcoflowMQTTClient) -> list[BaseSensorEntity]:
        return [
            LevelSensorEntity(client, "pd.soc", const.MAIN_BATTERY_LEVEL),
            WattsSensorEntity(client, "pd.wattsInSum", const.TOTAL_IN_POWER),
            WattsSensorEntity(client, "pd.wattsOutSum", const.TOTAL_OUT_POWER),
            RemainSensorEntity(client, "bms_emsStatus.chgRemainTime", const.CHARGE_REMAINING_TIME),
            RemainSensorEntity(client, "bms_emsStatus.dsgRemainTime", const.DISCHARGE_REMAINING_TIME),

            TempSensorEntity(client, "inv.outTemp", "Inv Out Temperature"),
            TempSensorEntity(client, "bms_bmsStatus.temp", const.BATTERY_TEMP),
            CyclesSensorEntity(client, "bms_bmsStatus.cycles", const.CYCLES),

            FanSensorEntity(client, "bms_emsStatus.fanLevel", "Fan Level"),

            # Optional Slave Battery
            LevelSensorEntity(client, "bms_slave.soc", const.SLAVE_BATTERY_LEVEL, False, True),
            TempSensorEntity(client, "bms_slave.temp", const.SLAVE_BATTERY_TEMP, False, True),
            CyclesSensorEntity(client, "bms_slave.cycles", const.SLAVE_CYCLES, False, True)

        ]

    def numbers(self, client: EcoflowMQTTClient) -> list[BaseNumberEntity]:
        return [
            LevelEntity(client, "bms_emsStatus.maxChargeSoc", const.MAX_CHARGE_LEVEL, 50, 100,
                        lambda value: {"moduleType": 2, "operateType": "upsConfig",
                                       "params": {"maxChgSoc": int(value)}}),

            LevelEntity(client, "bms_emsStatus.minDsgSoc", const.MIN_DISCHARGE_LEVEL, 0, 30,
                        lambda value: {"moduleType": 2, "operateType": "upsConfig",
                                       "params": {"minDsgSoc": int(value)}}),

            LevelEntity(client, "bms_emsStatus.minOpenOilEb", const.GEN_AUTO_START_LEVEL, 0, 30,
                        lambda value: {"moduleType": 2, "operateType": "closeOilSoc",
                                        "params": {"closeOilSoc": value}}),

            LevelEntity(client, "bms_emsStatus.maxCloseOilEb", const.GEN_AUTO_STOP_LEVEL, 50, 100,
                        lambda value: {"moduleType": 2, "operateType": "openOilSoc",
                                        "params": {"openOilSoc": value}}),

            ChargingPowerEntity(client, "mppt.cfgChgWatts", const.AC_CHARGING_POWER, 200, 1200,
                                lambda value: {"moduleType": 5, "operateType": "acChgCfg",
                                               "params": {"chgWatts": int(value), "chgPauseFlag": 255}})

        ]

    def switches(self, client: EcoflowMQTTClient) -> list[BaseSwitchEntity]:
        return [
            BeeperEntity(client, "mppt.beepState", const.BEEPER,
                         lambda value: {"moduleType": 5, "operateType": "quietMode", "params": {"enabled": value}}),

            EnabledEntity(client, "pd.dcOutState", const.USB_ENABLED,
                          lambda value: {"moduleType": 1, "operateType": "dcOutCfg", "params": {"enabled": value}}),

            EnabledEntity(client, "pd.acAutoOnCfg", const.AC_ALWAYS_ENABLED,
                          lambda value: {"moduleType": 1, "operateType": "acAutoOn", "params": {"cfg": value}}),

            EnabledEntity(client, "mppt.cfgAcEnabled", const.AC_ENABLED,
                          lambda value: {"moduleType": 5, "operateType": "acOutCfg",
                                         "params": {"enabled": value, "out_voltage": -1, "out_freq": 255,
                                                    "xboost": 255}}),

            EnabledEntity(client, "pd.carState", const.DC_ENABLED,
                          lambda value: {"moduleType": 5, "operateType": "mpptCar", "params": {"enabled": value}}),

        ]

    def selects(self, client: EcoflowMQTTClient) -> list[BaseSelectEntity]:
        return [
            DictSelectEntity(client, "mppt.dcChgCurrent", const.DC_CHARGE_CURRENT, const.DC_CHARGE_CURRENT_OPTIONS,
                             lambda value: {"moduleType": 5, "operateType": "dcChgCfg",
                                            "params": {"dcChgCfg": value}}),

            DictSelectEntity(client, "pd.lcdOffSec", const.SCREEN_TIMEOUT, const.SCREEN_TIMEOUT_OPTIONS,
                             lambda value: {"moduleType": 1, "operateType": "lcdCfg",
                                            "params": {"brighLevel": 255, "delayOff": value}}),

            DictSelectEntity(client, "pd.standbyMin", const.UNIT_TIMEOUT, const.UNIT_TIMEOUT_OPTIONS,
                             lambda value: {"moduleType": 1, "operateType": "standbyTime",
                                            "params": {"standbyMins": value}}),

            DictSelectEntity(client, "mppt.acStandbyMins", const.AC_TIMEOUT, const.AC_TIMEOUT_OPTIONS,
                             lambda value: {"moduleType": 5, "operateType": "standbyTime",
                                            "params": {"standbyMins": value}}),

            DictSelectEntity(client, "mppt.carStandbyMin", const.DC_TIMEOUT, const.DC_TIMEOUT_OPTIONS,
                             lambda value: {"moduleType": 5, "operateType": "carStandby",
                                            "params": {"standbyMins": value}})

        ]
from custom_components.ecoflow_cloud.api import EcoflowApiClient
from custom_components.ecoflow_cloud.devices import const, BaseDevice
from custom_components.ecoflow_cloud.entities import BaseSensorEntity, BaseNumberEntity, BaseSwitchEntity, \
    BaseSelectEntity
from custom_components.ecoflow_cloud.sensor import LevelSensorEntity, WattsSensorEntity, RemainSensorEntity, \
    TempSensorEntity, \
    InWattsSensorEntity, OutWattsSensorEntity, \
    CapacitySensorEntity, QuotaStatusSensorEntity
from custom_components.ecoflow_cloud.switch import BeeperEntity, EnabledEntity


class DeltaPro3(BaseDevice):
    def sensors(self, client: EcoflowApiClient) -> list[BaseSensorEntity]:
        return [
            LevelSensorEntity(client, self, "bmsBattSoc", const.MAIN_BATTERY_LEVEL)
            .attr("bmsDesignCap", const.ATTR_DESIGN_CAPACITY, 0),
            LevelSensorEntity(client, self, "bmsMaster.f32ShowSoc", const.MAIN_BATTERY_LEVEL_F32, False)
            .attr("bmsDesignCap", const.ATTR_DESIGN_CAPACITY, 0),
            CapacitySensorEntity(client, self, "bmsDesignCap", const.MAIN_DESIGN_CAPACITY, False),
            LevelSensorEntity(client, self, "bmsBattSoh", const.SOH),

            LevelSensorEntity(client, self, "ems.lcdShowSoc", const.COMBINED_BATTERY_LEVEL),
            LevelSensorEntity(client, self, "ems.f32LcdShowSoc", const.COMBINED_BATTERY_LEVEL_F32, False),
            WattsSensorEntity(client, self, "powInSumW", const.TOTAL_IN_POWER),
            WattsSensorEntity(client, self, "powOutSumW", const.TOTAL_OUT_POWER),

            InWattsSensorEntity(client, self, "powGetAcIn", const.AC_IN_POWER),
            OutWattsSensorEntity(client, self, "powOutSumW", const.AC_OUT_POWER),

            OutWattsSensorEntity(client, self, "powGetTypec1", const.TYPEC_1_OUT_POWER),
            OutWattsSensorEntity(client, self, "powGetTypec2", const.TYPEC_2_OUT_POWER),

            OutWattsSensorEntity(client, self, "powGetQcusb1", const.USB_QC_1_OUT_POWER),
            OutWattsSensorEntity(client, self, "powGetQcusb2", const.USB_QC_2_OUT_POWER),

            RemainSensorEntity(client, self, "bmsChgRemTime", const.CHARGE_REMAINING_TIME),
            RemainSensorEntity(client, self, "cmsDsgRemTime", const.DISCHARGE_REMAINING_TIME),

            TempSensorEntity(client, self, "bmsMaxCellTemp", const.BATTERY_TEMP)
            .attr("bmsMinCellTemp", const.ATTR_MIN_CELL_TEMP, 0)
            .attr("bmsMaxCellTemp", const.ATTR_MAX_CELL_TEMP, 0),
            TempSensorEntity(client, self, "bmsMinCellTemp", const.MIN_CELL_TEMP, False),
            TempSensorEntity(client, self, "bmsMaxCellTemp", const.MAX_CELL_TEMP, False),

            QuotaStatusSensorEntity(client, self)
        ]


    def numbers(self, client: EcoflowApiClient) -> list[BaseNumberEntity]:
        return []
    def switches(self, client: EcoflowApiClient) -> list[BaseSwitchEntity]:
        return []
    def selects(self, client: EcoflowApiClient) -> list[BaseSelectEntity]:
        return []

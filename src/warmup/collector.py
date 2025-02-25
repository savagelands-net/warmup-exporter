from __future__ import annotations

import datetime
import typing
import logging

from prometheus_client import CollectorRegistry, Gauge

from .warmup4ie import Warmup4IE, Warmup4IEDevice


class Collector:

    def __init__(
        self,
        thermostat_id: str = "",
        username: str = "",
        password: str = "",
    ) -> None:

        self.thermostat_id = thermostat_id
        self.username = username
        self.password = password

        self.registry = CollectorRegistry()

        self.logger = logging.getLogger(__name__)

        labels = ["device_id", "room_id", "room_name", "location_id", "location_name", "serial_number"]

        self.warmup_current_temp = Gauge(
            "warmup_current_temperature",
            "Current Temperature",
            labels,
            registry=self.registry,
        )

        self.warmup_floor_temp = Gauge(
            "warmup_floor_temperature",
            "Floor Temperature",
            labels,
            registry=self.registry,
        )

        self.warmup_air_temp = Gauge(
            "warmup_air_temperature",
            "Air Temperature",
            labels,
            registry=self.registry,
        )

        self.warmup_target_temp = Gauge(
            "warmup_target_temperature",
            "Thermostat Target Temperature",
            labels,
            registry=self.registry,
        )

        self.warmup_min_temp = Gauge(
            "warmup_minimum_temperature",
            "Thermostat Minimum Temperature",
            labels,
            registry=self.registry,
        )

        self.warmup_max_temp = Gauge(
            "warmup_maximum_temperature",
            "Thermostat Maximum Temperature",
            labels,
            registry=self.registry,
        )

        self.warmup_away_temp = Gauge(
            "warmup_away_temperature",
            "Thermostat Away Temperature",
            labels,
            registry=self.registry,
        )

        self.warmup_comfort_temp = Gauge(
            "warmup_comfort_temperature",
            "Thermostat Comfort Temperature",
            labels,
            registry=self.registry,
        )

        self.warmup_fixed_temp = Gauge(
            "warmup_fixed_temperature",
            "Thermostat Fixed Temperature",
            labels,
            registry=self.registry,
        )

        self.warmup_override_temp = Gauge(
            "warmup_override_temperature",
            "Thermostat Override Temperature",
            labels,
            registry=self.registry,
        )

        self.warmup_override_duration_mins = Gauge(
            "warmup_override_duration_mins",
            "Thermostat Override Duration in minutes",
            labels,
            registry=self.registry,
        )

        self.warmup_sleep_temp = Gauge(
            "warmup_sleep_temperature",
            "Thermostat Sleep Temperature",
            labels,
            registry=self.registry,
        )

        self.warmup_cost = Gauge(
            "warmup_cost",
            "Heating Cost (£/day)",
            labels,
            registry=self.registry,
        )

        self.warmup_energy= Gauge(
            "warmup_energy",
            "Heating Energy (kWh/d)",
            labels,
            registry=self.registry,
        )

    async def update_metrics(self) -> None:

        devices = Warmup4IE(self.username, self.password)
        try:
            thermostat: Warmup4IEDevice = [v for k, v in devices.get_all_devices().items() if k.thermostat_id == int(self.thermostat_id)][0]
        except IndexError:
            self.logger.error(f"Thermostat {self.thermostat_id} not found.")
            return
        else:
            labels = {
                "device_id": thermostat.get_device_id(),
                "room_id": thermostat.get_room_id(),
                "room_name": thermostat.get_room_name(),
                "location_id": thermostat.get_location_id(),
                "location_name": thermostat.get_location_name(),
                "serial_number": thermostat.get_serial_number(),
            }

            self.warmup_current_temp.labels(**labels).set(thermostat.get_current_temperature())
            self.warmup_floor_temp.labels(**labels).set(thermostat.get_floor_temperature())
            self.warmup_air_temp.labels(**labels).set(thermostat.get_air_temperature())
            self.warmup_target_temp.labels(**labels).set(thermostat.get_target_temperature())
            self.warmup_min_temp.labels(**labels).set(thermostat.get_target_temperature_low())
            self.warmup_max_temp.labels(**labels).set(thermostat.get_target_temperature_high())
            self.warmup_away_temp.labels(**labels).set(thermostat.get_away_temperature())
            self.warmup_comfort_temp.labels(**labels).set(thermostat.get_comfort_temperature())
            self.warmup_fixed_temp.labels(**labels).set(thermostat.get_fixed_temperature())
            self.warmup_override_temp.labels(**labels).set(thermostat.get_override_temperature())
            self.warmup_override_duration_mins.labels(**labels).set(thermostat.get_override_duration_mins())
            self.warmup_sleep_temp.labels(**labels).set(thermostat.get_sleep_temperature())
            self.warmup_cost.labels(**labels).set(thermostat.get_cost())
            self.warmup_energy.labels(**labels).set(thermostat.get_energy())

    def get_registry(self) -> CollectorRegistry:
        return self.registry

    @staticmethod
    def uptime(on_since: typing.Optional[datetime.datetime]) -> float:
        if not on_since:
            return float(0)

        now = datetime.datetime.now(on_since.tzinfo)
        uptime = now - on_since
        return uptime.total_seconds()

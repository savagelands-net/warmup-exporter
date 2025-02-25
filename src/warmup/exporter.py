from aiohttp import web
from prometheus_client import generate_latest

from .collector import Collector


class Exporter:

    def __init__(self) -> None:

        self.collectors: dict[str, Collector] = {}

    async def get_collector(
        self, thermostat_id: str, username: str, password: str
    ) -> Collector:
        if thermostat_id not in self.collectors:
            self.collectors[thermostat_id] = Collector(
                thermostat_id, username, password
            )
        return self.collectors[thermostat_id]

    async def collect(self, request: web.Request) -> web.Response:
        thermostat_id = request.query.get("thermostat_id")
        username = request.query.get("username")
        password = request.query.get("password")
        if not thermostat_id or not username or not password:
            return web.Response(
                body="'thermostat_id', 'username' and 'password' parameters must be specified",
                status=400,
            )

        device = await self.get_collector(thermostat_id, username, password)
        await device.update_metrics()

        return web.Response(body=generate_latest(device.get_registry()),
                            headers={"Content-Type": "text/plain"})

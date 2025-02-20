import os
import logging
from loki_logger import LokiHandler
import asyncio
import random

username = os.getenv("LOKI_USERNAME", "")
password = os.getenv("LOKI_PASSWORD", "")
tenant = os.getenv("LOKI_TENANT_ID", "fake")
url = os.getenv("LOKI_URL", "http://localhost:8080/loki/api/v1/push")
ca_bundle_path = os.getenv("CA_BUNDLE_PATH", "")
app_name = os.getenv("APP_NAME", "logs-spawner")

log_loki = logging.getLogger('loki')
log_loki.setLevel('DEBUG')
log_loki.addHandler(LokiHandler(
    url=url,
    app_name=app_name,
    username=username,
    password=password,
))

async def heartbeat():
    while True:
        log_loki.info(f"Heartbeat / tenant {username if username else tenant}")
        await asyncio.sleep(15)

async def error():
    while True:
        await asyncio.sleep(random.randint(60, 360))
        log_loki.error(f"Unexpected error")

async def info():
    while True:
        await asyncio.sleep(random.randint(5, 60))
        log_loki.info(f"Just an info, in case you care...")

async def debug():
    while True:
        await asyncio.sleep(random.randint(5, 120))
        log_loki.debug(f"Low level info")

async def main():
    print(f"Starting the App {app_name}...")
    await asyncio.gather(heartbeat(), error(), info(), debug())

if __name__ == "__main__":
    asyncio.run(main())

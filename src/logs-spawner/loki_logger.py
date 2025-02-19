import logging
import logging.handlers
import json
import base64
import requests
import time

class LokiHandler(logging.Handler):
    def __init__(self, url, app_name, username=None, password=None, ca_bundle_path=None, tenant=None, level = 0,):
        super().__init__(level)
        self.username = username
        self.password = password
        self.tenant = tenant
        self.url = url
        self.ca_bundle_path = ca_bundle_path
        self.app_name = app_name

    def convert(self, record: logging.LogRecord) -> str:
        ts = str(int(time.time() * 1e9))
        stream = {
            "stream": {
                "app": self.app_name,
                "level": record.levelname,
            },
            "values": [
                [
                    ts, 
                    f"{self.app_name} : [{record.levelname}] {record.getMessage()}"
                ]
            ]
        }
        data = {"streams": [stream]}
        return json.dumps(data)


    def emit(self, record: logging.LogRecord):
        headers = {"Content-Type": "application/json",}
        if self.username and self.password:
            auth_token = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
            headers["Authorization"] = f"Basic {auth_token}"
        else:
            headers["X-Scope-OrgID"] = self.tenant if self.tenant else 'fake'

        if self.ca_bundle_path:
            response = requests.post(url=self.url, data=self.convert(record), headers=headers, verify=self.ca_bundle_path)
        else:
            response = requests.post(url=self.url, data=self.convert(record), headers=headers)

        if response.status_code != 204:
            print(f"Failed to send log: {response.status_code}, {response.text}")

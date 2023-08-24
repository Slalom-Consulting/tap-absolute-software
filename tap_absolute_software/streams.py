"""Stream type classes for tap-absolute-software."""

from __future__ import annotations

from pathlib import Path

from tap_absolute_software.client import AbsoluteSoftwareStream

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")


class DeviceStream(AbsoluteSoftwareStream):
    """Define custom stream."""

    name = "devices-advanced"
    path = "/devices-advanced"
    primary_keys = ["deviceUid"]
    replication_key = None
    records_jsonpath = "$.data[*]"
    schema_filepath = SCHEMAS_DIR.joinpath("devices-advanced.json")

class ApplicationStream(AbsoluteSoftwareStream):
    """Define custom stream."""

    name = "applications"
    path = "/applications"
    primary_keys = ["deviceAppId"]
    replication_key = None
    records_jsonpath = "$.data[*]"
    schema_filepath = SCHEMAS_DIR.joinpath("applications.json")
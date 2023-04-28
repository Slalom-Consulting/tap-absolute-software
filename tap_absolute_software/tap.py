"""AbsoluteSoftware tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers
from tap_absolute_software import streams


class TapAbsoluteSoftware(Tap):
    """AbsoluteSoftware tap class."""

    name = "tap-absolute-software"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "token_id",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "token_secret",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The token secret to authenticate against the API service",
        ),
        th.Property(
            "auth_url",
            th.StringType,
            default="https://api.absolute.com/jws/validate",
            description="The url for the API service",
        ),
        th.Property(
            "endpoint",
            th.StringType,
            default="/v3/reporting",
            description="The reporting endpoint for the set of streams",
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.AbsoluteSoftwareStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.DeviceStream(self),
            streams.ApplicationStream(self),
        ]


if __name__ == "__main__":
    TapAbsoluteSoftware.cli()

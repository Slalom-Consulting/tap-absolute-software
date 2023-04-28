"""Tests standard tap features using the built-in SDK tests library."""

import datetime

from singer_sdk.testing import get_tap_test_class

from tap_absolute_software.tap import TapAbsoluteSoftware


SAMPLE_CONFIG = {
    "start_date": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d")
}


# Run standard built-in tap tests from the SDK:
TestTapAbsoluteSoftware = get_tap_test_class(
    tap_class=TapAbsoluteSoftware,
    config=SAMPLE_CONFIG
)

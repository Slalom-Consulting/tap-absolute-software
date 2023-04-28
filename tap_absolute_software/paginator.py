"""Pagination handling for AbsoluteSoftwareStream."""

from __future__ import annotations

from singer_sdk.pagination import JSONPathPaginator
from requests import Response
from singer_sdk.helpers.jsonpath import extract_jsonpath

import typing as t

if t.TYPE_CHECKING:
    from requests import Response

T = t.TypeVar("T")
TPageToken = t.TypeVar("TPageToken")


class AbsoluteSoftwarePaginator(JSONPathPaginator):
    def advance(self, response: Response) -> None:
        """Get a new page value and advance the current one.

        Args:
            response: API response object.

        Raises:
            RuntimeError: If a loop in pagination is detected. That is, when two
                consecutive pagination tokens are identical.
        """
        self._page_count += 1

        if not self.has_more(response):
            self._finished = True
            return

        new_value = self.get_next(response)

        if new_value and new_value == self._value:
            raise RuntimeError(
                f"Loop detected in pagination. "
                f"Pagination token {new_value} is identical to prior token.",
            )

        # Stop if new value None, empty string, 0, etc.
        if not new_value:
            self._finished = True
        else:
            self._value = new_value

    def get_next(self, response: Response) -> str | None:
        """Get the next page token.

        Args:
            response: API response object.

        Returns:
            The next page token.
        """
        all_matches = extract_jsonpath(self._jsonpath, response.json())
        return next(all_matches, None)
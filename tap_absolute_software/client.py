"""REST client handling, including AbsoluteSoftwareStream base class."""

from __future__ import annotations

import time
import json
import requests
import logging
from pathlib import Path
from authlib.jose import JsonWebSignature
from singer_sdk.streams import RESTStream
from tap_absolute_software.paginator import AbsoluteSoftwarePaginator

SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
class AbsoluteSoftwareStream(RESTStream):
    """AbsoluteSoftware stream class."""

    records_jsonpath = "$.data[*]"
    next_page_token_jsonpath = '$.metadata.pagination.nextPage'

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        return self.config.get('auth_url')
    
    def get_url(self, context: dict | None) -> str:
        """Get stream entity URL.

        Args:
            context: Stream partition or context dictionary.

        Returns:
            A URL, optionally targeted to a specific partition or context.
        """
        url = self.url_base
        return url

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """
        headers = {
            "alg": "HS256",
            "kid": self.config.get("token_id"),
            "method": "GET",
            "content-type": "application/json",
            "uri": self.config.get('endpoint') + self.path, # dynamically gets uri from stream
            "issuedAt": str(round(time.time() * 1000))
        }

        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")

        return headers
    
    def _request(
        self,
        prepared_request: requests.PreparedRequest,
        context: dict | None,
    ) -> requests.Response:

        # Creates prepared headers dictionary to dynamically pass the headers with the pagination token in it

        prepared_headers = json.loads(json.dumps(dict(prepared_request.headers)))

        # Signs the request with a Json Web Signature and posts the request
        jws = JsonWebSignature()
        signed = jws.serialize_compact(prepared_headers, json.dumps({}), self.config.get("token_secret"))
        response = requests.post(self.url_base, signed,{"content-type": "text/plain"})

        self._write_request_duration_log(
            endpoint=self.path,
            response=response,
            context=context,
            extra_tags={"url": prepared_request.path_url}
            if self._LOG_REQUEST_METRIC_URLS
            else None,
        )
        self.validate_response(response)
        logging.debug("Response received successfully.")
        return response

    def prepare_request(
        self,
        context: dict | None,
        next_page_token: _TToken | None,
    ) -> requests.PreparedRequest:
        """Prepare a request object for this stream.

        Args:
            context: Stream partition or context dictionary.
            next_page_token: Token, page number or any request argument to request the
                next page of data.

        Returns:
            Build a request with the stream's URL, path, query parameters,
            HTTP headers and authenticator.
        """
        http_method = self.rest_method
        url: str = self.get_url(context)
        params: dict | str = self.get_url_params(context, next_page_token)
        request_data = self.prepare_request_payload(context, next_page_token)
        headers = self.http_headers

        # Adds next page token to the headers in the prepared request
        if next_page_token:
            headers["query-string"] = 'nextPage=' + next_page_token

        return self.build_prepared_request(
            method=http_method,
            url=url,
            params=params,
            headers=headers,
            json=request_data,
        )
    
    def get_new_paginator(self) -> AbsoluteSoftwarePaginator:
        return AbsoluteSoftwarePaginator(self.next_page_token_jsonpath)

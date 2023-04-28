# tap-absolute-software

`tap-absolute-software` is a Singer tap for the [Absolute Software API](https://api.absolute.com/api-doc/doc.html).

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps and the [Absolute Software API Reference](https://api.absolute.com/api-doc/doc.html)

## Installation

Install from PyPi:

```bash
pipx install tap-absolute-software
```

Install from GitHub:

```bash
pipx install git+https://github.com/SlalomConsulting/tap-absolute-software.git@main
```

## Configuration

### Accepted Config Options

<!--
Developer TODO: Provide a list of config options accepted by the tap.

This section can be created by copy-pasting the CLI output from:

```
tap-absolute-software --about --format=markdown
```
-->

| Setting             | Required | Default | Description |
|:--------------------|:--------:|:-------:|:------------|
| token_id              | True     | None    | The token ID created in your Absolute API app.  |
| token_secret           | True     | None    | The token secret created in your Absolute API app. |
| auth_url       | True     | https://api.absolute.com/jws/validate    | The url for the authorization. This is changeable depending on country where your Absolute admin portal is accessed from. Please see  the Accessing the API section on the [Absolute Software API Reference](https://api.absolute.com/api-doc/doc.html) |
| endpoint       | True    | /v3/reporting    | Configurable depending on streams to be accessed. The v3/reporting endpoint is the uri accessed by default for the two stream. configured in this tap. There are other streams at different endpoints as well. Adding the other endpoints will require updating of this tap. |

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-absolute-software --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Custom Query String Configuration

This API also intakes different types of options to be appended to the query string alongside the pagination token that is located in the headers. 

For information on sorting, simple filtering, advanced filtering, selecting, and additional parameters in the query string for pagination, please see this [documentation link](https://api.absolute.com/api-doc/doc.html#section/Introduction/Sorting) from the Absolute Software API documentation. 

<!--
Developer TODO: If your tap requires special access on the source system, or any special authentication requirements, provide those here.
-->

## Usage

You can easily run `tap-absolute-software` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-absolute-software --version
tap-absolute-software --help
tap-absolute-software --config CONFIG --discover > ./catalog.json
```

## Developer Resources

Follow these instructions to contribute to this project.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-absolute-software` CLI interface directly using `poetry run`:

```bash
poetry run tap-absolute-software --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-absolute-software
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-absolute-software --version
# OR run a test `elt` pipeline:
meltano elt tap-absolute-software target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
# Canvas Extractor

This script retrieves and writes out to CSV all students, active sections, assignments,
and submissions.

## Requirements

Requires Python 3.8 and [Poetry](https://python-poetry.org/). To get started,
run the following command in the package directory:

```bash
poetry install
```

## Configuration

Application configuration is provided through environment variables or command
line interface (CLI) arguments. CLI arguments take precedence over environment
variables. Environment variables can be set the normal way, or by using a
dedicated [`.env` file](https://pypi.org/project/python-dotenv/). For `.env`
support, we provided a [.env.example](.env.example) which you can copy, rename
to `.env`, and adjust to your desired parameters. Supported parameters:

| Description | Required | Command Line Argument | Environment Variable |
| ----------- | -------- | --------------------- | -------------------- |
| Base Canvas URL | yes | -b or --base-url | CANVAS_BASE_URL |
| Canvas API access token | yes |  -a or --access-token | CANVAS_ACCESS_TOKEN |
| Output Directory | no (default: [working directory]/data) | -o or --output-directory | OUTPUT_DIRECTORY |
| Log level | no (default: INFO) | -l or --log-level | LOG_LEVEL |
| Start date | yes | -s or --start_date | START_DATE |
| End date | yes | -e or --end_date | END_DATE |


Valid log levels:
* DEBUG
* INFO(default)
* WARNING
* ERROR
* CRITICAL

## Execution

Execute the extractor with CLI args:

```bash
poetry run python.exe canvas_extractor -b your-canvas-url -a your-api-token -s start-date-range -e end-date-range
```

Alternately, run with environment variables or `.env` file:

```bash
poetry run python.exe canvas_extractor
```

For detailed help, execute `poetry run python canvas_extractor -h`.

### Output

CSV files in the data(or the specified output) directory with the LMS UDM format.

### Logging and Exit Codes

Log statements are written to the standard output. If you wish to capture log
details, then be sure to redirect the output to a file. For example:

```bash
poetry run python.exe schoology_extractor > 2020-12-07-15-43.log
```

If any errors occurred during the script run, then there will be a final print
message to the standard error handler as an additional mechanism for calling
attention to the error: `"A fatal error occurred, please review the log output
for more information."`

The application will exit with status code `1` if there were any log messages at
the ERROR or CRITICAL level, otherwise it will exit with status code `0`.

## Developer Utilities

Unit test execution:

```bash
poetry run pytest
```

Code coverage:

```bash
poetry run coverage run -m pytest
poetry run coverage report
```

Linting:

```bash
poetry run flake8
```

Static type checks:

```bash
poetry run mypy schoology_extractor
```

## Legal Information

Copyright (c) 2020 Ed-Fi Alliance, LLC and contributors.

Licensed under the [Apache License, Version 2.0](LICENSE) (the "License").

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

See [NOTICES](NOTICES.md) for additional copyright and license notifications.
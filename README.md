# Opafin

A simple tool to gererate charts of credit card expenses based on historical data in CSV format.

## Requirements

- Python 3.12+
- pip
- venv

## Setup (Linux / Ubuntu)

First, install `pip` and `venv` if not already installed:

```bash
sudo apt install python3-pip
sudo apt install python3.12-venv
```
Then, create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
```
Install the required Python packages:
`pip install -r requirements.txt`

## Run
`python3 main.py --csv "/path/to/your/file.csv"`

### Notes
- The CSV file should be similar to template.csv with the same columns.
- Dates should be parsable by pandas.to_datetime.

## Test
Run `pytest`

The warning `setDaemon() is deprecated, set the daemon attribute instead` is related to kaleido, one of the dependencies, it can be ignored.


## License

Distributed under the terms of the [LICENSE.txt](./LICENSE.txt) file.

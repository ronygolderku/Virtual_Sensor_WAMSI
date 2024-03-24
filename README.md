# Automated Python Script

This repository contains a Python script that automates the process of downloading and processing data from the Copernicus Marine dataset. The script retrieves chlorophyll-a (CHL) data for a specific geographical area and time range, converts it to a CSV file, and schedules the execution using GitHub Actions.

## Script Overview

The Python script performs the following tasks:

1. Opens the Copernicus Marine dataset remotely.
2. Extracts the first and last dates available in the dataset.
3. 
<iframe src="https://rpubs.com/ronygolderku/1165490" width="100%" height="500px"></iframe>

3. Opens the dataset for the last available date.
4. Converts the dataset to a Pandas DataFrame.
5. Saves the DataFrame to a CSV file with the name formatted as `output_<last_date>.csv`.

## Files

- `scripts.py`: Python script containing the automated data retrieval and processing logic.
- `main.yml`: GitHub Actions workflow file for scheduling script execution.

## Usage

The script is scheduled to run automatically every Sunday at midnight using GitHub Actions. It utilizes environment variables (`COPERNICUS_USERNAME` and `COPERNICUS_PASSWORD`) to authenticate with the Copernicus Marine API.

## Dependencies

The script requires the following Python libraries:

- pandas
- requests
- numpy
- copernicusmarine

These dependencies are automatically installed using the provided GitHub Actions workflow file (`main.yml`).

## How to Run

To run the script manually, follow these steps:

1. Set up your environment by installing Python and the required dependencies.
2. Ensure you have set the environment variables `COPERNICUS_USERNAME` and `COPERNICUS_PASSWORD` with your Copernicus Marine API credentials.
3. Clone this repository to your local machine.
4. Navigate to the repository directory.
5. Execute the Python script using the command `python scripts.py`.

## Author

This script was authored by [Your Name].

## License

This project is licensed under the [License Name] License - see the [LICENSE](LICENSE) file for details.

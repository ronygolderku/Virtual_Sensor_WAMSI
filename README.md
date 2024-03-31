# Automated Python Script

This repository contains a Python script that automates the process of downloading and processing data from the Copernicus Marine dataset. The script retrieves chlorophyll-a (CHL) data for a specific geographical area and time range, converts it to a CSV file, and schedules the execution using GitHub Actions.

## Script Overview

The Python script performs the following tasks:

1. Opens the Copernicus Marine dataset remotely.
2. Extracts the first and last dates available in the dataset.
3. Opens the dataset for the last available date. 
4. Converts the dataset to a Pandas DataFrame.
5. Saves the DataFrame to a CSV file with the name formatted as `CHL_<last_date>.csv`.
6. Uploads the CSV file to an AWS S3 bucket.

## Data Source and Data Point Position
- [Data point position in the Map](https://rpubs.com/ronygolderku/1165520) Explore the data point positions on the interactive map.
- [Source of the data](https://data.marine.copernicus.eu/product/OCEANCOLOUR_GLO_BGC_L4_MY_009_104/download?dataset=cmems_obs-oc_glo_bgc-plankton_my_l4-gapfree-multi-4km_P1D_202311) Access the data from the Copernicus Marine Environment Monitoring Service.

## AWS Integration

The script also integrates with AWS S3 for storing the processed data. Here are the relevant details:

- **AWS Access Key**: `{your_aws_access_key}`
- **AWS Secret Key**: `{your_aws_secret_key}`
- **S3 Bucket Name**: `wamsi-westport-project-1`
- **S3 Folder Path**: `SH20221201_Westport_Deliverables/Raw_Data/Virtual_Sensor/`

## Files

- `scripts.py`: Python script containing the automated data retrieval, processing, and upload logic.
- `main.yml`: GitHub Actions workflow file for scheduling script execution.

## Usage

The script is scheduled to run automatically every Sunday at midnight using GitHub Actions. It utilizes environment variables (`COPERNICUS_USERNAME` and `COPERNICUS_PASSWORD`) to authenticate with the Copernicus Marine API and AWS credentials to upload the CSV file to an S3 bucket.

## Dependencies

The script requires the following Python libraries:

- pandas
- requests
- numpy
- copernicusmarine
- boto3

These dependencies are automatically installed using the provided GitHub Actions workflow file (`main.yml`).

## How to Run

To run the script manually, follow these steps:

1. Set up your environment by installing Python and the required dependencies.
2. Ensure you have set the environment variables `COPERNICUS_USERNAME`, `COPERNICUS_PASSWORD`, `AWS_ACCESS_KEY_ID`, and `AWS_SECRET_ACCESS_KEY` with your Copernicus Marine API credentials and AWS S3 credentials.
3. Clone this repository to your local machine.
4. Navigate to the repository directory.
5. Execute the Python script using the command `python scripts.py`.

## Author

This script was authored by **Md Rony Golder**.

## License

This project is licensed under the **MIT License** - see the LICENSE file for details.



import os
import numpy as np
import copernicusmarine
import pandas as pd
import boto3
from botocore.exceptions import ClientError

username = os.getenv('COPERNICUS_USERNAME')
password = os.getenv('COPERNICUS_PASSWORD')

aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

session = boto3.Session()

# Create an S3 client
s3_client = session.client('s3', endpoint_url='https://projects.pawsey.org.au')

# Specify the S3 bucket and folder
bucket_name = 'wamsi-westport-project-1'
s3_folder = 'SH20221201_Westport_Deliverables/Raw_Data/Virtual_Sensor/PFTs/'


def sort_dimension(dataset, dim_name):
    """
    Get the values for the specified dimension and verify if they are unsorted. If so, the function sorts them.
    """
    # Get the coordinate values for the specified dimension.
    coordinates = dataset[dim_name].values

    # Check if the coordinates are unsorted.
    if (coordinates[0] >= coordinates[:-1]).all():
        dataset = dataset.sortby(dim_name, ascending=True)
        
    return dataset

dataframe_coordinates = pd.read_csv("points.csv", sep = ',')


list_datasetID= ["cmems_obs-oc_glo_bgc-plankton_my_l4-multi-4km_P1M"]

# Output names
output_names = [
    'CMEMS_PFTs',
]

# Variables
variables = ["CHL", "DIATO", "DINO", "GREEN", "HAPTO", "MICRO", "NANO", "PICO", "PROCHLO", "PROKAR"]
output_dir = "Data/"
# Create directory if doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Assuming dataframe_coordinates is defined elsewhere
# iterating over the datasets
for dataset_id, output_name in zip(list_datasetID, output_names):

    # Read dataset with CMC
    dataset = copernicusmarine.open_dataset(dataset_id=dataset_id, username='mgolder', password="G@DVH26uGtb3BBq")

    # Select surface and rename dimensions
    for coordinate in dataset.coords:
        if coordinate == 'lon':
            dataset = dataset.rename({'lon': 'longitude'})
        if coordinate == 'lat':
            dataset = dataset.rename({'lat': 'latitude'})

    # Sort axis that were inverted
    dataset = sort_dimension(dataset, 'latitude')
    dataset = sort_dimension(dataset, 'longitude')

    # Update start and end times
    first_date = np.datetime_as_string(dataset.time[0].values, unit='D')
    last_date = np.datetime_as_string(dataset.time[-1].values, unit='D')

    # Download data
    for row in zip(dataframe_coordinates['latitude'], dataframe_coordinates['longitude'], dataframe_coordinates.index):
        # Do the subset
        dataset_point = dataset[variables].sel(time=slice(first_date, last_date)).sel(latitude=row[0], longitude=row[1], method="nearest")
        # Save in .csv
        dataset_point.to_dataframe().to_csv(output_dir + output_name + f"point_{row[2]+1}.csv")
        # Save in .nc
        #dataset_point.to_netcdf(output_dir + output_name + f"point_{row[2]}.nc")


for file_name in os.listdir(output_dir):
    if file_name.endswith('.csv'):  # Upload only CSV files
        csv_file_path = os.path.join(output_dir, file_name)
        
        # Upload the CSV file to S3
        try:
            s3_client.upload_file(csv_file_path, bucket_name, os.path.join(s3_folder, file_name))
            print(f"File '{file_name}' uploaded to S3 bucket '{bucket_name}' in folder '{s3_folder}'.")
        except Exception as e:
            print(f"Error uploading file '{file_name}' to S3: {e}")
        
        # Clean up: Delete the local CSV file
        os.remove(csv_file_path)
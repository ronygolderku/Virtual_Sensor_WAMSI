import os
import numpy as np
import copernicusmarine
import pandas as pd
import boto3
#from botocore.exceptions import ClientError
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Load environment variables
username = os.getenv('COPERNICUS_USERNAME')
password = os.getenv('COPERNICUS_PASSWORD')
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")


def process_and_upload_dataset(dataset_id, variables, output_name, s3_folder, points):
    # Create an S3 client
    session = boto3.Session()
    s3_client = session.client('s3', endpoint_url='https://projects.pawsey.org.au')
    bucket_name = 'wamsi-westport-project-1'

    for index, row in points.iterrows():
        # Extract information from the row
        longitude = row['longitude']
        latitude = row['latitude']
        
        # Download data using the extracted information
        data = copernicusmarine.open_dataset(
            dataset_id=dataset_id,
            variables=variables,
            minimum_longitude=longitude,
            maximum_longitude=longitude,
            minimum_latitude=latitude,
            maximum_latitude=latitude,
            username=username,
            password=password
        )
        data.to_dataframe().to_csv(f"{output_name}_point_{index + 1}.csv")

    # Upload files to S3
    upload_files_to_s3(s3_client, bucket_name, s3_folder)

def upload_files_to_s3(s3_client, bucket_name, s3_folder):
    for file_name in os.listdir():
        if file_name.endswith('.csv'):
            csv_file_path = os.path.join(file_name)
            try:
                s3_client.upload_file(csv_file_path, bucket_name, os.path.join(s3_folder, file_name))
                print(f"File '{file_name}' uploaded to S3 bucket '{bucket_name}' in folder '{s3_folder}'.")
            except (NoCredentialsError, PartialCredentialsError) as e:
                print(f"Error uploading file '{file_name}' to S3: {e}")
            os.remove(csv_file_path)

# Specify points
bucket_name = 'wamsi-westport-project-1'
points = pd.read_csv('points_olci_ghrsst.txt', sep="\t")


process_and_upload_dataset(
    dataset_id="cmems_obs-oc_glo_bgc-plankton_my_l3-olci-300m_P1D",
    variables=["CHL"],
    output_name="CMEMS_OLCI_CHL",
    s3_folder="SH20221201_Westport_Deliverables/Raw_Data/Virtual_Sensor/Sentinel/Points/",
    points=points,
)



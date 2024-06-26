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
bucket_name = 'wamsi-westport-project-1-1'
s3_folder = 'csiem-data/data-lake/UKMO/OSTIA/Temperature/Points/'


# data= copernicusmarine.open_dataset(
#     dataset_id="METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2",
#     variables=["analysed_sst"],
#     username=username,
#     password=password,
# )

# last_date = np.datetime_as_string(data.time[-1].values, unit='D')

# #Exract the first date available
# first_date = np.datetime_as_string(data.time[0].values, unit='D')

points = pd.read_csv('points.txt', sep="\t")

output_name ='CMEMS_SST'


for index, row in points.iterrows():
    # Extract information from the row
    longitude = row['longitude']
    latitude = row['latitude']
    # Download data using the extracted information
    data=copernicusmarine.open_dataset(
        dataset_id="METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2",
        variables= ["analysed_sst"],
        minimum_longitude=longitude,
        maximum_longitude=longitude,
        minimum_latitude=latitude,
        maximum_latitude=latitude,
        username=username,
        password=password)
    data.to_dataframe().to_csv(f"{output_name}_point_{index + 1}.csv")


for file_name in os.listdir():
    if file_name.endswith('.csv'):  # Upload only CSV files
        csv_file_path = os.path.join(file_name) 
        
        # Upload the CSV file to S3
        try:
            s3_client.upload_file(csv_file_path, bucket_name, os.path.join(s3_folder, file_name))
            print(f"File '{file_name}' uploaded to S3 bucket '{bucket_name}' in folder '{s3_folder}'.")
        except Exception as e:
            print(f"Error uploading file '{file_name}' to S3: {e}")
        
        # Clean up: Delete the local CSV file
        os.remove(csv_file_path)

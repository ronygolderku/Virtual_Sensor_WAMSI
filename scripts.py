import os
import numpy as np
import copernicusmarine
username = os.getenv('COPERNICUS_USERNAME')
password = os.getenv('COPERNICUS_PASSWORD')

aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

session = boto3.Session()

# Create an S3 client
s3_client = session.client('s3', endpoint_url='https://projects.pawsey.org.au')

# Specify the S3 bucket and folder
bucket_name = 'wamsi-westport-project-1'
s3_folder = 'SH20221201_Westport_Deliverables/Raw_Data/Virtual_Sensor/'

# Remotely open the whole dataset
data = copernicusmarine.open_dataset(
    dataset_id="cmems_obs-oc_glo_bgc-plankton_my_l4-gapfree-multi-4km_P1D",
    variables=["CHL"],
    minimum_longitude=115.590368,
    maximum_longitude=115.590368,
    minimum_latitude=-32.086885,
    maximum_latitude=-32.086885,
    username=username,
    password=password,
)

# Extract last date available
last_date = np.datetime_as_string(data.time[-1].values, unit='D')

#Exract the first date available
first_date = np.datetime_as_string(data.time[0].values, unit='D')


# Open dataset for last date available
data = copernicusmarine.open_dataset(
    dataset_id="cmems_obs-oc_glo_bgc-plankton_my_l4-gapfree-multi-4km_P1D",
    variables=["CHL"],
    minimum_longitude=115.590368,
    maximum_longitude=115.590368,
    minimum_latitude=-32.086885,
    maximum_latitude=-32.086885,
    start_datetime=f"{first_date}T00:00:00",
    end_datetime=f"{last_date}T00:00:00",
    username=username,
    password=password,
)
df = data.to_dataframe().reset_index()
csv_file_path = f'CHL_{last_date}.csv'
df.to_csv(csv_file_path, index=False)

# Upload the CSV file to S3
try:
    s3_client.upload_file(csv_file_path, bucket_name, os.path.join(s3_folder, os.path.basename(csv_file_path)))
    print(f"File '{csv_file_path}' uploaded to S3 bucket '{bucket_name}' in folder '{s3_folder}'.")
except Exception as e:
    print(f"Error uploading file to S3: {e}")

# Clean up: Delete the local CSV file
os.remove(csv_file_path)

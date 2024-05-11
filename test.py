import os
import numpy as np
import copernicusmarine
import pandas as pd
import geopandas as gpd
import rioxarray
import boto3
#from botocore.exceptions import ClientError
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Load environment variables
username = os.getenv('COPERNICUS_USERNAME')
password = os.getenv('COPERNICUS_PASSWORD')
aws_access_key = os.getenv("AWS_ACCESS_KEY_ID")
aws_secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")


def process_and_upload_dataset(dataset_id, variables, output_name, s3_folder, shapefiles):
    # Create an S3 client
    session = boto3.Session()
    s3_client = session.client('s3', endpoint_url='https://projects.pawsey.org.au')
    bucket_name = 'wamsi-westport-project-1'

    # Open dataset
    ds = copernicusmarine.open_dataset(
        dataset_id=dataset_id,
        variables=variables,
        username=username,
        password=password,
        minimum_longitude=115.10,
        maximum_longitude=115.75,
        minimum_latitude=-32.77,
        maximum_latitude=-31.44)

    # Process shapefiles
    for idx, shapefile in enumerate(shapefiles):
        gdf = gpd.read_file(shapefile).geometry.to_list()
        ds.rio.write_crs("epsg:4326", inplace=True)
        polygon = ds.rio.clip(gdf, crs="epsg:4326")
        polygon_mean = polygon.mean(dim=['latitude', 'longitude'])
        polygon_mean = polygon_mean.drop_vars(['spatial_ref', 'Equirectangular'])
        polygon_mean.to_dataframe().to_csv(f"{output_name}_polygon_{idx+1}.csv")

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

# Specify shapefiles
shapefiles = [
    "shapefile/Polygons_1_MultiPolygon.shp",
    "shapefile/Polygons_2_MultiPolygon.shp",
    "shapefile/Polygons_3_MultiPolygon.shp",
    "shapefile/Polygons_4_MultiPolygon.shp",
    "shapefile/Polygons_5_MultiPolygon.shp",
    "shapefile/Polygons_6_MultiPolygon.shp"
]


process_and_upload_dataset(
    dataset_id="c3s_obs-oc_glo_bgc-plankton_my_l3-multi-4km_P1D",
    variables=["CHL", "MICRO", "NANO", "PICO"],
    output_name="CMEMS_PFTs",
    s3_folder="SH20221201_Westport_Deliverables/Raw_Data/Virtual_Sensor/PFTs_poly/",
    shapefiles=shapefiles,
)

process_and_upload_dataset(
    dataset_id="cmems_obs-oc_glo_bgc-transp_my_l4-gapfree-multi-4km_P1D",
    variables=["KD490", "ZSD"],
    output_name="CMEMS_KD490_ZSD",
    s3_folder="SH20221201_Westport_Deliverables/Raw_Data/Virtual_Sensor/Transp_poly/",
    shapefiles=shapefiles,
)

process_and_upload_dataset(
    dataset_id="cmems_obs-oc_glo_bgc-optics_my_l3-multi-4km_P1D",
    variables=["BBP", "CDM"],
    output_name="CMEMS_BBP_CDM",
    s3_folder="SH20221201_Westport_Deliverables/Raw_Data/Virtual_Sensor/Optics_poly/",
    shapefiles=shapefiles,
)

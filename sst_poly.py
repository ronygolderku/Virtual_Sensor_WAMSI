import os
import numpy as np
import copernicusmarine
import pandas as pd
import geopandas as gpd
import rioxarray
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
s3_folder = 'csiem-data/data-lake/UKMO/OSTIA/Temperature/Polygon/'


ds= copernicusmarine.open_dataset(
    dataset_id="METOFFICE-GLO-SST-L4-NRT-OBS-SST-V2",
    variables=["analysed_sst"],
    username=username,
    password=password,
    minimum_longitude=115.10,
    maximum_longitude=115.75,
    minimum_latitude=-32.77,
    maximum_latitude=-31.44)

shapefiles = [
    "shapefile/Polygons_1_MultiPolygon.shp",
    "shapefile/Polygons_2_MultiPolygon.shp",
    "shapefile/Polygons_3_MultiPolygon.shp",
    "shapefile/Polygons_4_MultiPolygon.shp",
    "shapefile/Polygons_5_MultiPolygon.shp",
    "shapefile/Polygons_6_MultiPolygon.shp"
]

output_name ='CMEMS_SST'

for idx, shapefile in enumerate(shapefiles):
    gdf = gpd.read_file(shapefile).geometry.to_list()
    ds.rio.write_crs("epsg:4326", inplace=True)
    polygon = ds.rio.clip(gdf, crs="epsg:4326")
    polygon_mean= polygon.mean(dim=['latitude', 'longitude'])
    polygon_mean = polygon_mean.drop_vars(['spatial_ref'])
    polygon_mean.to_dataframe().to_csv(f"{output_name}_polygon_{idx+1}.csv")


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

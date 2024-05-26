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
    bucket_name = 'wamsi-westport-project-1-1'

    # Open dataset
    ds = copernicusmarine.open_dataset(
        dataset_id=dataset_id,
        variables=variables,
        username=username,
        password=password,
        minimum_longitude=115.10,
        maximum_longitude=115.75,
        minimum_latitude=-32.77,
        maximum_latitude=-31.44,
        minimum_depth=0.4940253794193268,
        maximum_depth=130.66598510742188)

    # Process shapefiles
    for idx, shapefile in enumerate(shapefiles):
        gdf = gpd.read_file(shapefile).geometry.to_list()
        ds.rio.write_crs("epsg:4326", inplace=True)
        polygon = ds.rio.clip(gdf, crs="epsg:4326", all_touched=True)
        polygon_mean = polygon.mean(dim=['latitude', 'longitude'])
        polygon_mean = polygon_mean.drop_vars(['spatial_ref'])
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
    dataset_id="cmems_mod_glo_bgc-car_anfc_0.25deg_P1D-m",
    variables=["dissic", "ph", "talk"],
    output_name="CMEMS_car",
    s3_folder="csiem-data/data-lake/MOI/PISCES/Model_car/Polygon/",
    shapefiles=shapefiles,
)

process_and_upload_dataset(
    dataset_id="cmems_mod_glo_bgc-nut_anfc_0.25deg_P1D-m",
    variables=["fe", "no3", "po4", "si"],
    output_name="CMEMS_nut",
    s3_folder="csiem-data/data-lake/MOI/PISCES/Model_Nut/Polygon/",
    shapefiles=shapefiles,
)

process_and_upload_dataset(
    dataset_id="cmems_mod_glo_bgc-co2_anfc_0.25deg_P1D-m",
    variables=["spco2"],
    output_name="CMEMS_co2",
    s3_folder="csiem-data/data-lake/MOI/PISCES/Model_co2/Polygon/",
    shapefiles=shapefiles,
)

process_and_upload_dataset(
    dataset_id="cmems_mod_glo_bgc-bio_anfc_0.25deg_P1D-m",
    variables=["nppv", "o2"],
    output_name="CMEMS_bio",
    s3_folder="csiem-data/data-lake/MOI/PISCES/Model_bio/Polygon/",
    shapefiles=shapefiles,
)

process_and_upload_dataset(
    dataset_id="cmems_mod_glo_bgc-pft_anfc_0.25deg_P1D-m",
    variables=["chl", "phyc"],
    output_name="CMEMS_pft",
    s3_folder="csiem-data/data-lake/MOI/PISCES/Model_pft/Polygon/",
    shapefiles=shapefiles,
)

process_and_upload_dataset(
    dataset_id="cmems_mod_glo_bgc-optics_anfc_0.25deg_P1D-m",
    variables=["kd"],
    output_name="CMEMS_optics",
    s3_folder="csiem-data/data-lake/MOI/PISCES/Model_optics/Polygon/",
    shapefiles=shapefiles,
)

process_and_upload_dataset(
    dataset_id="cmems_mod_glo_phy-so_anfc_0.083deg_PT6H-i",
    variables=["so"],
    output_name="CMEMS_Salt",
    s3_folder="csiem-data/data-lake/MOI/NEMO/Model_salinity/Polygon/",
    shapefiles=shapefiles,
)


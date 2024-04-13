# import os
# import numpy as np
# #import copernicusmarine
# import xarray as xr
# import pandas as pd
# import boto3
# from botocore.exceptions import ClientError

# # username = os.getenv('COPERNICUS_USERNAME')
# # password = os.getenv('COPERNICUS_PASSWORD')

# aws_access_key = os.environ.get("AWS_ACCESS_KEY_ID")
# aws_secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY")

# session = boto3.Session()

# # Create an S3 client
# s3_client = session.client('s3', endpoint_url='https://projects.pawsey.org.au')

# # Specify the S3 bucket and folder
# bucket_name = 'wamsi-westport-project-1'
# s3_folder = 'SH20221201_Westport_Deliverables/Raw_Data/Virtual_Sensor/PP/'

# ds=xr.open_dataset('https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdMH1pp1day')
# ds=ds.sel(latitude=slice(-31, -32), longitude=slice(114,116))
# print(ds)
# points = pd.read_csv('points.txt', sep="\t")
# output_name ='MODIS_PP'

# for index, row in points.iterrows():
#     # Extract information from the row
#     longitude = row['longitude']
#     latitude = row['latitude']
#     # Download data using the extracted information
#     data=ds.sel(latitude=latitude, longitude=longitude, method='nearest')
#     data.to_dataframe().to_csv(f"{output_name}_point_{index + 1}.csv")


# for file_name in os.listdir():
#     if file_name.endswith('.csv'):  # Upload only CSV files
#         csv_file_path = os.path.join(file_name) 
        
#         # Upload the CSV file to S3
#         try:
#             s3_client.upload_file(csv_file_path, bucket_name, os.path.join(s3_folder, file_name))
#             print(f"File '{file_name}' uploaded to S3 bucket '{bucket_name}' in folder '{s3_folder}'.")
#         except Exception as e:
#             print(f"Error uploading file '{file_name}' to S3: {e}")
        
#         # Clean up: Delete the local CSV file
#         os.remove(csv_file_path)
import netCDF4 as nc
import pandas as pd

# Open the NetCDF dataset
nc_file = nc.Dataset('https://coastwatch.pfeg.noaa.gov/erddap/griddap/erdMH1pp1day', 'r')

# Extract latitude and longitude slices
latitude_slice = slice(-31, -32)
longitude_slice = slice(114, 116)

# Filter dataset based on latitude and longitude slices
latitude = nc_file.variables['latitude'][:]
longitude = nc_file.variables['longitude'][:]
lat_indices = (latitude >= latitude_slice.start) & (latitude <= latitude_slice.stop)
lon_indices = (longitude >= longitude_slice.start) & (longitude <= longitude_slice.stop)
data = nc_file.variables['chlorophyll'][lat_indices, lon_indices, :]

# Read points from points.txt
points = pd.read_csv('points.txt', sep="\t")

output_name ='MODIS_PP'

for index, row in points.iterrows():
    # Extract information from the row
    longitude = row['longitude']
    latitude = row['latitude']
    
    # Find nearest indices for the given latitude and longitude
    lat_index = (np.abs(latitude - latitude_slice.start)).argmin()
    lon_index = (np.abs(longitude - longitude_slice.start)).argmin()
    
    # Extract data for the nearest point
    point_data = data[:, lat_index, lon_index]
    
    # Convert the data to DataFrame and save to CSV
    df = pd.DataFrame({'chlorophyll': point_data})
    df.to_csv(f"{output_name}_point_{index + 1}.csv", index=False)

# Close the NetCDF file
nc_file.close()

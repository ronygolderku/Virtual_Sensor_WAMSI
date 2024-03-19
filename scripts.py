import os
import numpy as np
import copernicusmarine
username = os.getenv('COPERNICUS_USERNAME')
password = os.getenv('COPERNICUS_PASSWORD')

# Remotely open the whole dataset
data = copernicusmarine.open_dataset(
    dataset_id="cmems_obs-oc_glo_bgc-plankton_my_l4-gapfree-multi-4km_P1D",
    variables=["CHL"],
    minimum_longitude=115.590368,
    maximum_longitude=115.590368,
    minimum_latitude=-32.086885,
    maximum_latitude=-32.086885,
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
)

# Conversion to CSV
data.to_dataframe().reset_index().to_csv(f'output_{last_date}.csv', index=False)

print("Data downloaded in file", f'output_{last_date}.csv', "for the last date available in the dataset:", last_date)

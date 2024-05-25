# Make virtual sensor with satellite data

This repository contains a Python script that automates the process of downloading and processing data from the Copernicus Marine dataset and ERDDAP. The script retrieves long-term temperature and bio-optical data for a specific geographical area and time range, converts it to a CSV file, and schedules the execution using GitHub Actions.

## Script Overview

The Python script performs the following tasks:

1. Opens the Copernicus Marine and NASA dataset remotely.
2. Extracts the first and last dates available in the dataset.
3. Opens the dataset for the last available date. 
4. Converts the dataset to a Pandas DataFrame.
5. Saves the DataFrame to a CSV file.
6. Uploads the CSV file to an AWS S3 bucket.

## Data Source and Data Point Position
- [Data point position in the Map](https://ronygolderku.github.io/cs_map/) Explore the data point positions on the interactive map.
- [Source of the data](https://data.marine.copernicus.eu/) Access the data from the Copernicus Marine Environment Monitoring Service.

## AWS Integration

The script also integrates with AWS S3 for storing the processed data. Here are the relevant details:

- **AWS Access Key**: `{your_aws_access_key}`
- **AWS Secret Key**: `{your_aws_secret_key}`
- **S3 Bucket Name**: `wamsi-westport-project-1-1`
- **S3 Folder Path**: `csiem-data/data-lake/`



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

# Data catalogue

```markdown
📦
├── 🌍 European Space Agency (ESA)
│   ├── 🚀 Globcolor
│   │   ├── 🌈 Reflectance
│   │   │   ├── RRS412
│   │   │   ├── RRS443
│   │   │   ├── RRS490
│   │   │   ├── RRS555
│   │   │   └── RRS670
│   │   ├── 🅿️ PP
│   │   ├── 🔍 Optics
│   │   │   ├── BBP (Backscattering coefficient)
│   │   │   └── CDM (Colored Dissolved Organic Matter)
│   │   ├── 📀 Transp
│   │   │   ├── KD490 (Diffuse attenuation coefficient at 490 nm)
│   │   │   ├── ZSD (Secchi disk depth)
│   │   │   └── SPM (Suspended Particulate Matter)
│   │   └── 🐠 Plankton
│   │       ├── CHL (Chlorophyll concentration)
│   │       ├── DIATO (Diatoms)
│   │       ├── DINO (Dinoflagellates)
│   │       ├── GREEN (Green algae)
│   │       ├── HAPTO (Haptophytes)
│   │       ├── MICRO (Microplankton)
│   │       ├── NANO (Nanoplankton)
│   │       ├── PICO (Picoplankton)
│   │       ├── PROCHLO (Prochlorococcus)
│   │       └── PROKAR (Prokaryotes)
│   └── 🛰️ Sentinel
│       └── 📸 OLCI
│           └── 🌊 CHL
├── UK Met Office (UKMO)
│   └── 🚀 OSTIA
│       └── 🌡️ Temp
├── 🚀 NASA
│   ├── 🛰️ GHRSST
│   │   └── 🌊 MUR
│   │       └── 🌡️ SST
│   └── 🛰️ MODIS
│       ├── 🌊 POC
│       ├── 🌊 PIC
│       └── 🌞 PAR
└── Mercator Ocean International (MOI)
    └── 🌐 MODEL
        ├── 🐠 PISCES
        │   ├── 🧪 Bio
        │   │   ├── Net Primary Production (nppv)
        │   │   └── Oxygen (o2)
        │   ├── 🧪 Nut
        │   │   ├── Iron (fe)
        │   │   ├── Nitrate (no3)
        │   │   ├── Phosphate (po4)
        │   │   └── Silicate (si)
        │   ├── 🔍 Optics
        │   │   └── Light Attenuation Coefficient (kd)
        │   ├── 🌱 Car
        │   │   ├── Dissolved Inorganic Carbon (dissic)
        │   │   ├── pH
        │   │   └── Total Alkalinity (talk)
        │   ├── 🌬️ CO2
        │   │   └── Partial Pressure of CO2 (spco2)
        │   └── 🌱 PFTs
        │       ├── Chlorophyll (chl)
        │       └── Phytoplankton (phyc)
        ├── 🐟 SEAPODYM
        │   └── 🌱 Biomass
        │       ├── PP (Primary productivity)
        │       └── ZOO (Zooplankton)
        └── 🌊 NEMO
            └── 💧 Salinity
```

## How to Run

To run the script manually, follow these steps:

1. Set up your environment by installing Python and the required dependencies.
2. Ensure you have set the environment variables `COPERNICUS_USERNAME`, `COPERNICUS_PASSWORD`, `AWS_ACCESS_KEY_ID`, and `AWS_SECRET_ACCESS_KEY` with your Copernicus Marine API credentials and AWS S3 credentials.
3. Clone this repository to your local machine.
4. Navigate to the repository directory.
5. Execute the Python script

## Author

This script was authored by **Md Rony Golder**.

## License

This project is licensed under the **MIT License** - see the LICENSE file for details.



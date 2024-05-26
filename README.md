# Make virtual sensor with satellite data in CS
There are numerous sensors currently deployed around Cockburn Sound (CS) that provide continuous data streams of oceanic and atmospheric parameters. These data streams are often accessible through data centers and agencies such as BOM, DWER, WAMSI, and UWA and so on. Despite these extensive monitoring efforts, in situ data may not always be available for specific areas of interest. For example, assessing the environmental impact of on going development activities (WESTPORT) requires data from regions outside of the immediate CS environment.

Setting up sensors in those locations is expensive, including the costs of purchase, deployment, and ongoing maintenance. 
To address these challenges, using satellite data to create virtual sensors offers a viable solution for monitoring surface environmental conditions at locations where physical sensors cannot be installed. Satellite data can provide comprehensive and continuous coverage, overcoming the limitations of in situ sensor deployment and enabling effective environmental monitoring.

## About this repo
This repository contains Python scripts designed to automate the downloading and processing of data from several key agencies: the *European Space Agency (ESA)*, *UK Met Office (UKMO)*, *NASA*, *Mercator Ocean International (MOI)*. The scripts are capable of retrieving long-term datasets for specified geographical areas [points, polygons] and time ranges, converting the data into CSV files, and scheduling the execution using GitHub Actions. The final processed data is then stored in the **Pawsey** S3 bucket.

## Data Source and Data Point Position
- [Data point position in the Map](https://ronygolderku.github.io/cs_map/) Explore the data point positions on the interactive map.

## Data Sources

- [ESA](https://data.marine.copernicus.eu/): GLOBCOLOR (resolution: 4km) and Sentinel (resolution: 300m) marine environment products.
- [MOI](https://data.marine.copernicus.eu/): Numerious MODEL output
- [UKMO](https://data.marine.copernicus.eu/): Access data from OSTIA temperature (resolution: 0.05 °) products.
- [NASA](https://coastwatch.pfeg.noaa.gov/erddap/griddap/): Access data from the Group for High-Resolution Sea Surface Temperature (GHRSST (resolution: 0.01 °)) and MODIS (resolution: 4km) through ERDDAP.


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
- geopandas
- rioxarray


These dependencies are automatically installed using the provided GitHub Actions workflow file (`main.yml`).

# Folder Sturcture

```markdown
📦
├── 🌍 European Space Agency (ESA)
│   ├── 🚀 Globcolor (4 km) [DAILY]
│   │   ├── 🌈 Reflectance
│   │   │   ├── RRS412 (Remote Sensing Reflectance at 412 nm) [sr⁻¹]
│   │   │   ├── RRS443 (Remote Sensing Reflectance at 443 nm) [sr⁻¹]
│   │   │   ├── RRS490 (Remote Sensing Reflectance at 490 nm) [sr⁻¹]
│   │   │   ├── RRS555 (Remote Sensing Reflectance at 555 nm) [sr⁻¹]
│   │   │   └── RRS670 (Remote Sensing Reflectance at 670 nm) [sr⁻¹]
│   │   ├── 🅿️ PP [mg C m⁻² d⁻¹]
│   │   ├── 🔍 Optics
│   │   │   ├── BBP (Backscattering coefficient) [m⁻¹]
│   │   │   └── CDM (Colored Dissolved Organic Matter) [m⁻¹]
│   │   ├── 📀 Transp
│   │   │   ├── KD490 (Diffuse attenuation coefficient at 490 nm) [m⁻¹]
│   │   │   ├── ZSD (Secchi disk depth) [m]
│   │   │   └── SPM (Suspended Particulate Matter) [g m⁻³]
│   │   └── 🐠 Plankton
│   │       ├── CHL (Chlorophyll concentration) [mg m⁻³]
│   │       ├── DIATO (Diatoms) [mg m⁻³]
│   │       ├── DINO (Dinoflagellates) [mg m⁻³]
│   │       ├── GREEN (Green algae) [mg m⁻³]
│   │       ├── HAPTO (Haptophytes) [mg m⁻³]
│   │       ├── MICRO (Microplankton) [mg m⁻³]
│   │       ├── NANO (Nanoplankton) [mg m⁻³]
│   │       ├── PICO (Picoplankton) [mg m⁻³]
│   │       ├── PROCHLO (Prochlorococcus) [mg m⁻³]
│   │       └── PROKAR (Prokaryotes) [mg m⁻³]
│   └── 🛰️ Sentinel (300 m) [DAILY]
│       └── 📸 OLCI
│           └── 🌊 CHL [mg m⁻³]
├── UK Met Office (UKMO)
│   └── 🚀 OSTIA (~ 5 km) [DAILY]
│       └── 🌡️ Temp [°K]
├── 🚀 NASA
│   ├── 🛰️ GHRSST (~1 km) [DAILY]
│   │   └── 🌊 MUR
│   │       └── 🌡️ SST [°C]
│   └── 🛰️ MODIS [MONTHLY]
│       ├── 🌊 POC (Particulate Organic Carbon) [mg m⁻³]
│       ├── 🌊 PIC (Particulate Inorganic Carbon) [mg m⁻³]
│       └── 🌞 PAR (Photosynthetically Active Radiation) [Einstein m⁻² d⁻¹]
└── Mercator Ocean International (MOI)
    └── 💻 MODEL
        ├── 🐠 PISCES (~25 km) [DAILY]
        │   ├── 🧪 Bio
        │   │   ├── Net Primary Production (NPPV) [mg C m⁻³ d⁻¹]
        │   │   └── Oxygen (O2) [mmol O₂ m⁻³]
        │   ├── 🧪 Nut
        │   │   ├── Iron (Fe) [mmol Fe m⁻³]
        │   │   ├── Nitrate (NO3) [mmol N m⁻³]
        │   │   ├── Phosphate (PO4) [mmol P m⁻³]
        │   │   └── Silicate (Si) [mmol Si m⁻³]
        │   ├── 🔍 Optics
        │   │   └── Light Attenuation Coefficient (KD) [m⁻¹]
        │   ├── 🌱 Car
        │   │   ├── Dissolved Inorganic Carbon (DIC) [mmol C m⁻³]
        │   │   ├── pH
        │   │   └── Total Alkalinity (TALK) [mmol eq m⁻³]
        │   ├── 🌬️ CO2
        │   │   └── Partial Pressure of CO2 (pCO2) [Pa]
        │   └── 🌱 PFTs
        │       ├── Chlorophyll (Chl) [mg m⁻³]
        │       └── Phytoplankton (Phyc) [mmol m⁻³]
        ├── 🐟 SEAPODYM (~ 9 km) [DAILY]
        │   └── 🌱 Biomass
        │       ├── PP (Primary productivity) [mg C m⁻² d⁻¹]
        │       └── ZOO (Zooplankton) [mg C m⁻²]
        └── 🌊 NEMO (~ 9 km) [EVERY 6 HOUR]
            └── 💧 Salinity [10⁻³]
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




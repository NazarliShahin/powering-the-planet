# Powering the Planet

How do countries produce and consume energy, and what does it cost the planet?
This project analyses decades of global energy and CO₂ data from
[Our World in Data](https://ourworldindata.org/) to study the energy
transition. It was developed as an individual project for the Python module
at the University of Milan (UniMI).

## Questions

1. **Decoupling:** which countries grew their economy (GDP) while reducing
   their CO₂ emissions?
2. **Energy mix:** how has the mix of coal, oil, gas, nuclear and renewables
   changed over time in a given country?

## Data

| Dataset | Content | Source |
|---|---|---|
| `owid-co2-data.csv` | CO₂ emissions, GDP, population | [owid/co2-data](https://github.com/owid/co2-data) |
| `owid-energy-data.csv` | Primary energy consumption by source | [OWID energy dataset](https://catalog.ourworldindata.org/energy/owid_energy/owid_energy.csv) |

Both files have one row per country and year. The data is licensed under
[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/); please cite
*Our World in Data* and the underlying sources when reusing it.

The energy dataset used here is the **new release** of OWID. The version in
the `owid/energy-data` repository is legacy and no longer updated, and the
primary energy methodology changed between the two, so the numbers are not
directly comparable.

The `data/` folder is excluded from the repository (see `.gitignore`), so the
files must be downloaded as explained below.

## Setup

Requires Python 3. The commands below are for macOS/Linux.

```bash
# 1. clone the repository
git clone https://github.com/NazarliShahin/powering-the-planet.git
cd powering-the-planet

# 2. create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# 3. install the libraries
pip install -r requirements.txt

# 4. download the data
python -m src.download
```

The script saves four files in `data/raw/`: the two datasets and their
codebooks. The codebooks describe every column and are only needed for
reference. If a download fails, the script stops with an explicit error
message; run it again once the connection is back.



## Usage

**Streamlit app** (interactive):

```bash
streamlit run app.py
```

The app has three tabs: the energy mix of a country over time, the
decoupling of GDP and CO₂ between two chosen years, and the relationship
between GDP per capita and CO₂ per capita across countries.

**Notebook:** open `notebooks/01_explore.ipynb` in VS Code or JupyterLab,
select the `.venv` kernel and run all cells. Both the app and the notebook
only call the functions in `src/`; the logic is not duplicated.

## Project structure

```
powering-the-planet/
├── data/raw/              # downloaded CSV files (not tracked by git)
├── notebooks/
│   └── 01_explore.ipynb   # data exploration and analysis
├── src/
│   ├── download.py        # download_all: downloads the CSV files
│   ├── data_loader.py     # load_csv: reads a CSV with error handling
│   ├── cleaning.py        # keep_countries: removes regional aggregates
│   ├── dataset.py         # build_dataset: cleans and merges CO2 + energy data
│   ├── analysis.py        # change_between, find_decoupled, energy_mix
│   └── visualization.py   # plot_change_scatter, plot_energy_mix
├── requirements.txt
└── README.md
```

## Method

1. **Loading:** only the needed columns are read from each CSV. A missing
   file or a missing column raises an explicit error.
2. **Cleaning:** the OWID files also contain regional aggregates such as
   "World", "Africa" or "High-income countries". They have no ISO code, so
   rows without `iso_code` are removed and only countries are kept.
3. **Merging:** the CO₂ and energy tables are joined on country, year and ISO
   code (inner join). The result has 210 countries and 16,964 rows.
4. **Decoupling analysis:** for each country, the percentage change of GDP and
   CO₂ emissions between two years is computed. A country is *decoupled* if
   its GDP grew while its CO₂ emissions fell.
5. **Energy mix:** the share of coal, oil, gas, nuclear and renewables in
   primary energy is extracted for one country and shown as a stacked area
   chart.

## Results so far

- Between **1990 and 2022**, 37 of the 155 countries with data for both years
  grew their GDP while reducing CO₂ emissions.
- Between **2000 and 2022** this holds for 42 countries; 29 countries are in
  both groups. Many Eastern European countries appear in the 1990 group,
  probably because of the collapse of heavy industry in the early 1990s, so
  the 2000 starting year gives a fairer picture.
- In the United Kingdom, the share of coal in primary energy fell sharply
  between 1990 and 2022, while gas and renewables grew.

These results are preliminary.

## Limitations

- **GDP ends in 2022** in the data, so the GDP and CO₂ comparison stops there.
- **The energy mix by source** (coal, oil, gas, nuclear, renewables) is
  available for only about 77-79 countries. They account for roughly 97% of
  the CO₂ emissions of the 210 countries in the dataset in 2022, and include
  all the largest emitters.
- Before about 1990 the set of countries with energy data changes over time
  (for example, the successor states of the Soviet Union appear only
  afterwards), so the energy analysis starts in 1990.
- Countries without an ISO code are dropped with the aggregates. This
  removes Kosovo, as well as states that no longer exist, such as
  Czechoslovakia and East Germany.
- Percentage changes can be very large for countries that started from a very
  low level. The scatter plot is zoomed in on GDP changes from -50% to 600%
  and CO₂ changes from -80% to 400%, so a few extreme countries are outside
  the visible area (they are still in the data).

## Author

Shahin Nazarli

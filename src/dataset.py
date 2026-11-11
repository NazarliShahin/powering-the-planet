"""Build the combined CO2 and energy dataset."""

import pandas as pd

from src.cleaning import keep_countries
from src.data_loader import load_csv

CO2_COLUMNS = [
    "country", "year", "iso_code", "population", "gdp",
    "co2", "co2_per_capita", "co2_per_gdp", "cumulative_co2",
    "coal_co2", "oil_co2", "gas_co2", "cement_co2", "share_global_co2",
]

ENERGY_COLUMNS = [
    "country", "year", "iso_code",
    "coal_energy_twh", "oil_energy_twh", "gas_energy_twh",
    "nuclear_energy_twh", "renewables_energy_twh",
    "coal_energy_share_pct", "oil_energy_share_pct", "gas_energy_share_pct",
    "nuclear_energy_share_pct", "renewables_energy_share_pct",
    "fossil_fuels_energy_share_pct", "low_carbon_energy_share_pct",
    "total_energy_twh", "total_energy_per_capita_kwh",
]


def build_dataset(co2_path, energy_path):
    """Load, clean and merge the CO2 and energy datasets.

    Only countries are kept (regional aggregates are removed) and the two
    tables are joined on country, year and ISO code.

    Parameters
    ----------
    co2_path : str or Path
        Path to the OWID CO2 CSV file.
    energy_path : str or Path
        Path to the OWID energy CSV file.

    Returns
    -------
    pandas.DataFrame
        One row per country and year, with CO2, GDP, population and
        energy mix columns.
    """
    co2 = keep_countries(load_csv(co2_path, CO2_COLUMNS))
    energy = keep_countries(load_csv(energy_path, ENERGY_COLUMNS))
    return co2.merge(energy, on=["country", "year", "iso_code"], how="inner")
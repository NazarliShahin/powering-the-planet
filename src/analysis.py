"""Functions for analysing the relationship between GDP and CO2 emissions."""

import pandas as pd


def change_between(df, start_year, end_year):
    """Compute the percentage change of GDP and CO2 between two years.

    Parameters
    ----------
    df : pandas.DataFrame
        Combined dataset with 'country', 'year', 'gdp' and 'co2' columns.
    start_year : int
        First year of the comparison.
    end_year : int
        Last year of the comparison.

    Returns
    -------
    pandas.DataFrame
        One row per country with 'gdp_change_pct' and 'co2_change_pct'.
        Countries with missing data in either year are dropped.
    """
    start = df[df["year"] == start_year].set_index("country")
    end = df[df["year"] == end_year].set_index("country")

    changes = pd.DataFrame(
        {
            "gdp_change_pct": (end["gdp"] / start["gdp"] - 1) * 100,
            "co2_change_pct": (end["co2"] / start["co2"] - 1) * 100,
        }
    )
    return changes.dropna()


def find_decoupled(changes):
    """Select countries whose GDP grew while their CO2 emissions fell.

    Parameters
    ----------
    changes : pandas.DataFrame
        Output of change_between().

    Returns
    -------
    pandas.DataFrame
        The subset of countries with positive GDP change and negative
        CO2 change.
    """
    grew_and_cut = (changes["gdp_change_pct"] > 0) & (changes["co2_change_pct"] < 0)
    return changes[grew_and_cut].copy()



#next-----------------------------




ENERGY_SHARE_COLUMNS = {
    "coal_energy_share_pct": "Coal",
    "oil_energy_share_pct": "Oil",
    "gas_energy_share_pct": "Gas",
    "nuclear_energy_share_pct": "Nuclear",
    "renewables_energy_share_pct": "Renewables",
}


def energy_mix(df, country, start_year=1990, end_year=2022):
    """Select the energy mix of one country over a range of years.

    Parameters
    ----------
    df : pandas.DataFrame
        Combined dataset with 'country', 'year' and the energy share columns.
    country : str
        Name of the country, as it appears in the 'country' column.
    start_year : int, optional
        First year to include.
    end_year : int, optional
        Last year to include.

    Returns
    -------
    pandas.DataFrame
        Indexed by year, with one column per energy source (share of
        primary energy, in percent).

    Raises
    ------
    ValueError
        If there is no data for the country in the given years.
    """
    in_country = df["country"] == country
    in_years = df["year"].between(start_year, end_year)
    mix = df[in_country & in_years].set_index("year")

    if mix.empty:
        raise ValueError(f"No data for {country} between {start_year} and {end_year}.")

    return mix[list(ENERGY_SHARE_COLUMNS)].rename(columns=ENERGY_SHARE_COLUMNS)
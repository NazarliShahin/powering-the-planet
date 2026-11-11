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
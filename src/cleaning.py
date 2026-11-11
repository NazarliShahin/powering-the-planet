"""Functions for cleaning the OWID datasets."""

import pandas as pd


def keep_countries(df):
    """Keep only rows that refer to countries, dropping regional aggregates.

    Regions such as 'World', 'Africa' or 'High-income countries' have no
    ISO code in the OWID data, so rows with a missing iso_code are removed.

    Parameters
    ----------
    df : pandas.DataFrame
        Data with an 'iso_code' column.

    Returns
    -------
    pandas.DataFrame
        A copy of the data containing only countries.
    """
    is_country = df["iso_code"].notna()
    return df[is_country].copy()
"""Functions for loading the OWID datasets."""

from pathlib import Path

import pandas as pd


def load_csv(path, columns=None):
    """Load a CSV file into a DataFrame.

    Parameters
    ----------
    path : str or Path
        Location of the CSV file.
    columns : list of str, optional
        Columns to keep. If None, all columns are loaded.

    Returns
    -------
    pandas.DataFrame
        The loaded data.

    Raises
    ------
    FileNotFoundError
        If the file does not exist.
    ValueError
        If one of the requested columns is not in the file.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"File not found: {path}. Download the data first, "
            "see the instructions in README.md."
        )

    try:
        return pd.read_csv(path, usecols=columns)
    except ValueError as error:
        raise ValueError(
            f"Could not read columns {columns} from {path}: {error}"
        ) from error
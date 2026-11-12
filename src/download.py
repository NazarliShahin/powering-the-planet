"""Download the OWID datasets used by the project."""

import sys
from pathlib import Path

import requests

DEFAULT_FOLDER = Path("data/raw")
TIMEOUT_SECONDS = 60

DATA_URLS = {
    "owid-co2-data.csv":
        "https://owid-public.owid.io/data/co2/owid-co2-data.csv",
    "owid-energy-data.csv":
        "https://catalog.ourworldindata.org/energy/owid_energy/owid_energy.csv",
    "owid-co2-codebook.csv":
        "https://raw.githubusercontent.com/owid/co2-data/master/owid-co2-codebook.csv",
    "owid-energy-codebook.csv":
        "https://catalog.ourworldindata.org/energy/owid_energy/owid_energy.codebook.csv",
}


def download_file(url, destination, overwrite=False):
    """Download one file, skipping it if it already exists.

    The file is first written to a temporary '.part' file and renamed at the
    end, so an interrupted download never leaves a broken CSV behind.

    Parameters
    ----------
    url : str
        Address of the file to download.
    destination : str or Path
        Where to save the file. Missing folders are created.
    overwrite : bool, optional
        If True, download again even when the file already exists.

    Returns
    -------
    bool
        True if the file was downloaded, False if it was skipped.

    Raises
    ------
    RuntimeError
        If the download fails (no connection, timeout, HTTP error).
    """
    destination = Path(destination)
    if destination.exists() and not overwrite:
        return False

    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = destination.with_suffix(destination.suffix + ".part")

    try:
        with requests.get(url, stream=True, timeout=TIMEOUT_SECONDS) as response:
            response.raise_for_status()
            with open(temporary, "wb") as file:
                for chunk in response.iter_content(chunk_size=1024 * 1024):
                    file.write(chunk)
    except requests.RequestException as error:
        temporary.unlink(missing_ok=True)
        raise RuntimeError(f"Could not download {url}: {error}") from error

    temporary.replace(destination)
    return True


def download_all(folder=DEFAULT_FOLDER, overwrite=False):
    """Download all the datasets used by the project.

    Parameters
    ----------
    folder : str or Path, optional
        Folder where the files are saved.
    overwrite : bool, optional
        If True, download again the files that already exist.

    Returns
    -------
    dict
        Maps each file name to True (downloaded) or False (skipped).
    """
    folder = Path(folder)
    return {
        name: download_file(url, folder / name, overwrite)
        for name, url in DATA_URLS.items()
    }


def main():
    """Download the data from the command line.

    Usage: python -m src.download [folder]
    """
    folder = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_FOLDER
    for name, downloaded in download_all(folder).items():
        status = "downloaded" if downloaded else "already exists, skipped"
        print(f"{name}: {status}")


if __name__ == "__main__":
    main()
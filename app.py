"""Streamlit app for the Powering the Planet project."""

import streamlit as st

from src.analysis import energy_mix
from src.dataset import build_dataset
from src.visualization import plot_energy_mix

CO2_PATH = "data/raw/owid-co2-data.csv"
ENERGY_PATH = "data/raw/owid-energy-data.csv"


@st.cache_data
def load_data():
    """Load and merge the datasets once and keep them in memory."""
    return build_dataset(CO2_PATH, ENERGY_PATH)


st.title("Powering the Planet")

df = load_data()

countries = sorted(df.loc[df["coal_energy_share_pct"].notna(), "country"].unique())
country = st.selectbox("Country", countries, index=countries.index("United Kingdom"))
start_year, end_year = st.slider("Years", 1990, 2022, (1990, 2022))

try:
    mix = energy_mix(df, country, start_year, end_year)
except ValueError as error:
    st.warning(str(error))
else:
    fig = plot_energy_mix(mix, f"Energy mix of {country}, {start_year}-{end_year}")
    st.pyplot(fig)
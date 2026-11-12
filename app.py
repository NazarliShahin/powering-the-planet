"""Streamlit app for the Powering the Planet project."""

import streamlit as st

from src.analysis import (
    change_between,
    energy_mix,
    find_decoupled,
    gdp_co2_relationship,
)
from src.dataset import build_dataset
from src.visualization import (
    plot_change_scatter,
    plot_energy_mix,
    plot_gdp_co2_relationship,
)

CO2_PATH = "data/raw/owid-co2-data.csv"
ENERGY_PATH = "data/raw/owid-energy-data.csv"
ZOOM_X = (-50, 600)
ZOOM_Y = (-80, 400)


@st.cache_data
def load_data():
    """Load and merge the datasets once and keep them in memory."""
    return build_dataset(CO2_PATH, ENERGY_PATH)


st.title("Powering the Planet")
df = load_data()

tab_mix, tab_decoupling, tab_relationship = st.tabs(
    ["Energy mix", "GDP vs CO2 change", "GDP vs CO2 per capita"]
)

with tab_mix:
    countries = sorted(df.loc[df["coal_energy_share_pct"].notna(), "country"].unique())
    country = st.selectbox(
        "Country", countries, index=countries.index("United Kingdom")
    )
    mix_start, mix_end = st.slider("Years", 1990, 2022, (1990, 2022), key="mix_years")

    try:
        mix = energy_mix(df, country, mix_start, mix_end)
    except ValueError as error:
        st.warning(str(error))
    else:
        title = f"Energy mix of {country}, {mix_start}-{mix_end}"
        st.pyplot(plot_energy_mix(mix, title))

with tab_decoupling:
    start_year, end_year = st.slider(
        "Years", 1960, 2022, (1990, 2022), key="decoupling_years"
    )
    zoom = st.checkbox("Zoom in (hide extreme countries)", value=True)

    if start_year == end_year:
        st.warning("Choose two different years.")
    else:
        changes = change_between(df, start_year, end_year)
        decoupled = find_decoupled(changes)
        st.write(
            f"{len(decoupled)} of {len(changes)} countries grew their GDP "
            "while reducing their CO2 emissions."
        )
        fig = plot_change_scatter(
            changes,
            decoupled,
            f"GDP vs CO2 change, {start_year}-{end_year}",
            xlim=ZOOM_X if zoom else None,
            ylim=ZOOM_Y if zoom else None,
        )
        st.pyplot(fig)
        st.dataframe(decoupled.sort_values("co2_change_pct").round(1))

with tab_relationship:
    year = st.slider("Year", 1990, 2022, 2022, key="relationship_year")
    data, result = gdp_co2_relationship(df, year)

    col_countries, col_slope, col_r2 = st.columns(3)
    col_countries.metric("Countries", len(data))
    col_slope.metric("Slope", f"{result.slope:.2f}")
    col_r2.metric("R²", f"{result.rvalue ** 2:.2f}")

    st.pyplot(plot_gdp_co2_relationship(data, result, year))
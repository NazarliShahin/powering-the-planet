"""Functions for plotting the results of the analysis."""
import numpy as np
import matplotlib.pyplot as plt


def plot_change_scatter(changes, decoupled, title, xlim=None, ylim=None):
    """Scatter plot of GDP change against CO2 change for each country.

    Countries whose GDP grew while their CO2 emissions fell are highlighted.

    Parameters
    ----------
    changes : pandas.DataFrame
        Output of change_between(), indexed by country.
    decoupled : pandas.DataFrame
        Output of find_decoupled(), the highlighted subset of countries.
    title : str
        Title of the plot.
    xlim : tuple of float, optional
        Limits (min, max) of the horizontal axis, to zoom in on the plot.
    ylim : tuple of float, optional
        Limits (min, max) of the vertical axis, to zoom in on the plot.

    Returns
    -------
    matplotlib.figure.Figure
        The figure with the scatter plot.
    """
    is_decoupled = changes.index.isin(decoupled.index)
    others = changes[~is_decoupled]
    highlighted = changes[is_decoupled]

    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(
        others["gdp_change_pct"], others["co2_change_pct"],
        color="grey", alpha=0.6, label="Other countries",
    )
    ax.scatter(
        highlighted["gdp_change_pct"], highlighted["co2_change_pct"],
        color="green", alpha=0.8, label="GDP up, CO2 down",
    )
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(0, color="black", linewidth=0.8)
    ax.set_xlabel("GDP change (%)")
    ax.set_ylabel("CO2 emissions change (%)")
    ax.set_title(title)
    ax.legend()

    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:
        ax.set_ylim(ylim)
    return fig


#next--------------------------



def plot_energy_mix(mix, title):
    """Stacked area chart of the energy mix of one country over time.

    Parameters
    ----------
    mix : pandas.DataFrame
        Output of energy_mix(): indexed by year, one column per source.
    title : str
        Title of the plot.

    Returns
    -------
    matplotlib.figure.Figure
        The figure with the stacked area chart.
    """
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.stackplot(mix.index, mix.T.values, labels=mix.columns)
    ax.set_xlabel("Year")
    ax.set_ylabel("Share of primary energy (%)")
    ax.set_title(title)
    ax.set_xlim(mix.index.min(), mix.index.max())
    ax.legend(loc="upper left", bbox_to_anchor=(1.02, 1))
    fig.tight_layout()
    return fig



#then create other graph



def plot_gdp_co2_relationship(data, result, year):
    """Log-log scatter plot of CO2 per capita against GDP per capita.

    Parameters
    ----------
    data : pandas.DataFrame
        First output of gdp_co2_relationship(), with 'gdp_per_capita' and
        'co2_per_capita' columns.
    result : scipy.stats.LinregressResult
        Second output of gdp_co2_relationship().
    year : int
        Year shown in the title.

    Returns
    -------
    matplotlib.figure.Figure
        The figure with the scatter plot and the fitted line.
    """
    fig, ax = plt.subplots(figsize=(9, 6))
    ax.scatter(data["gdp_per_capita"], data["co2_per_capita"], alpha=0.6)

    x = np.logspace(
        np.log10(data["gdp_per_capita"].min()),
        np.log10(data["gdp_per_capita"].max()),
        100,
    )
    y = 10 ** (result.intercept + result.slope * np.log10(x))
    ax.plot(
        x, y, color="red",
        label=f"slope = {result.slope:.2f}, R² = {result.rvalue ** 2:.2f}",
    )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("GDP per capita (log scale)")
    ax.set_ylabel("CO2 per capita, tonnes (log scale)")
    ax.set_title(f"GDP and CO2 emissions per capita, {year}")
    ax.legend()
    return fig
"""
Module for plotting adherence trends and analytics.
"""
from datetime import datetime
from datetime import timedelta

import numpy as np
import plotly
import plotly.graph_objects as go

from app.utils import adherence


def plot_top_general_adherence_by_drug_name(prescriptions, n=5):
    top_general = adherence.most_adhered_by_drug_name(
        prescriptions, n=n, measure="general"
    )

    top_general_names = []
    top_general_frac = []
    for drug in top_general:
        top_general_names.append(drug[0])
        top_general_frac.append(drug[1])

    fig = go.Figure(
        data=[
            go.Bar(name="General adherence", x=top_general_names, y=top_general_frac),
        ]
    )

    fig.update_layout(
        title="Top adhered medications",
        xaxis_title="Date",
        yaxis_title="Adherence %",
        font=dict(color="#7f7f7f"),
    )

    output = plotly.offline.plot(fig, include_plotlyjs=False, output_type="div")
    return output


def plot_top_ontime_adherence_by_drug_name(prescriptions, n=5):
    top_ontime = adherence.most_adhered_by_drug_name(
        prescriptions, n=n, measure="ontime"
    )

    top_ontime_names = []
    top_ontime_frac = []
    for drug in top_ontime:
        top_ontime_names.append(drug[0])
        top_ontime_frac.append(drug[1])

    fig = go.Figure(
        data=[go.Bar(name="ontime adherence", x=top_ontime_names, y=top_ontime_frac),]
    )

    fig.update_layout(
        title="Top on-time medications",
        xaxis_title="Date",
        yaxis_title="On time %",
        font=dict(color="#7f7f7f"),
    )

    output = plotly.offline.plot(fig, include_plotlyjs=False, output_type="div")
    return output


def plot_adherence_rates_over_time(patients, prescriptions):
    """
    Plot on-time and on-track adherence rates over time.
    TODO: use real data
    """

    curr_date = datetime(year=2020, month=3, day=15)
    end = datetime.now()
    dates = []
    while curr_date <= end:
        curr_date += timedelta(days=1)
        dates.append(curr_date)

    np.random.seed(3)
    x = np.arange(1, len(dates) + 1)
    noise = np.random.uniform(-0.1, 0.1, len(dates))
    patient_adh = np.clip(1 / (1 + np.exp(-(-0.3 + 0.03 * x))) + noise, 0.3, 0.96)
    noise = np.random.uniform(-0.2, 0.05, len(dates))
    rx_adh = patient_adh + noise

    # Create traces
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dates, y=patient_adh, mode="lines", name="General"))
    fig.add_trace(go.Scatter(x=dates, y=rx_adh, mode="lines", name="On-time"))

    fig.update_layout(
        title="Adherence rates over time",
        xaxis_title="Date",
        yaxis_title="Adherence %",
        font=dict(color="#7f7f7f"),
    )

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list(
                [
                    dict(count=1, label="1m", step="month", stepmode="backward"),
                    dict(count=6, label="6m", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all"),
                ]
            )
        ),
    )

    output = plotly.offline.plot(fig, include_plotlyjs=False, output_type="div")

    return output

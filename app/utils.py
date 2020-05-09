from collections import defaultdict
from datetime import datetime, timedelta
import math
import numpy as np
import plotly
import plotly.graph_objects as go

# TODO: add more options
DOSAGE_TO_FREQ = {
    "QD - 1x per day": {"freq": 1, "freq_repeat": 1, "freq_repeat_unit": "day"},
    "BID - 2x per day": {"freq": 2, "freq_repeat": 1, "freq_repeat_unit": "day"},
    "TID - 3x per day": {"freq": 3, "freq_repeat": 1, "freq_repeat_unit": "day"},
    "QID - 4x per day": {"freq": 4, "freq_repeat": 1, "freq_repeat_unit": "day"},
}

DAY_STD = {"day": 1, "week": 7, "month": 30}


# TODO: Refactor such that the functions below can go in Prescription class.


def get_next_refill_date(
    last_refill_date, duration, duration_unit, refills, refill_num
):
    """
    Return next refill date based on most recent (last) refill date 
    and dosage information.

    last_refill_date: datetime
    duration: int
    duration_unit: string - either 'day', 'week', or 'month'
    refills: int - number of refills for entire treatment
    refill_num: int - the refill the patient is currently on
    """

    if refill_num == refills or refills == 0:
        return None
    days_per_cycle = math.floor(duration * DAY_STD[duration_unit] / (refills + 1))
    return last_refill_date + timedelta(days=days_per_cycle)


def get_days_until_refill(curr_date, next_refill_date):
    """
    Return number of days until next refill.
    If curr_date > next_refill_date, for instance, if refill was not fulfilled
        in time, then days until refill is still 0.

    curr_date: datetime - the date against which next refill date is compared
    next_refill_date: datetime
    """
    if next_refill_date is None:
        return None
    return max([(next_refill_date - curr_date).days, 0])


def adherence_by_drug_name(prescriptions, measure="general"):
    """
    Return average adherence rates by drug name.
    e.g. {'Acetominophen: 0.89', 'Ibuprofen: 0.73'}
    prescriptions: list - list of Prescription objects
    measure: string - measure of adherence, either 'general'
                      (taking the right number of pills expected)
                      or 'ontime' (taking pills at the right time)
    """
    if measure not in ["general", "ontime"]:
        raise ValueError('`measure` must be "general" or "ontime"')
    med_adh = defaultdict(list)
    for rx in prescriptions:
        if measure == "general":
            med_adh[rx.drug].append(rx.frac_required_intakes())
        else:
            med_adh[rx.drug].append(rx.frac_on_time())
    for name in med_adh.keys():
        rates = med_adh[name]
        med_adh[name] = np.mean(rates)
    return med_adh


def least_adhered_by_drug_name(prescriptions, n=5, measure="general"):
    """
    Get least adhered to medications by drug name.
    prescriptions: list - list of Prescription objects
    n: int - how many to return
    measure: string - measure of adherence, either 'general'
                      (taking the right number of pills expected)
                      or 'ontime' (taking pills at the right time)
    """
    med_adh = adherence_by_drug_name(prescriptions, measure=measure)
    sorted_adh = [
        (name, frac)
        for name, frac in sorted(med_adh.items(), key=lambda x: x[1], reverse=True)
    ]
    return sorted_adh[:n]


def most_adhered_by_drug_name(prescriptions, n=5, measure="general"):
    """
    Get most adhered to medications by drug name.
    prescriptions: list - list of Prescription objects
    n: int - how many to return
    measure: string - measure of adherence, either 'general'
                      (taking the right number of pills expected)
                      or 'ontime' (taking pills at the right time)
    """
    med_adh = adherence_by_drug_name(prescriptions, measure=measure)
    sorted_adh = [
        (name, frac)
        for name, frac in sorted(med_adh.items(), key=lambda x: x[1], reverse=True)
    ]
    return sorted_adh[:n]


def plot_top_general_adherence_by_drug_name(prescriptions, n=5):
    top_general = most_adhered_by_drug_name(prescriptions, n=n, measure="general")

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
    top_ontime = most_adhered_by_drug_name(prescriptions, n=n, measure="ontime")

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

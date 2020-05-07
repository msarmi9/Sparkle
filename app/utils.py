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

def plotly_map():
    # token = 'pk.eyJ1IjoiYWNoZW9uIiwiYSI6ImNrM3FuYzJhNDAxZHozb3BrcTFrZGtnMjYifQ.8jxG2wR9AgTm98dhJYIgQA'

    # fig = go.Figure(go.Scattermapbox(
    #     lat=['45.5017'],
    #     lon=['-73.5673'],
    #     mode='markers',
    #     marker=go.scattermapbox.Marker(
    #         size=14
    #     ),
    #     text=['Montreal'],
    # ))

    # fig.update_layout(
    #     hovermode='closest',
    #     mapbox=dict(
    #         accesstoken=token,
    #         bearing=0,
    #         center=go.layout.mapbox.Center(
    #             lat=45,
    #             lon=-73
    #         ),
    #         pitch=0,
    #         zoom=5
    #     )
    # )

    # np.random.seed(1)

    # N = 100
    # random_x = np.linspace(0, 1, N)
    # random_y0 = np.random.randn(N) + 5
    # random_y1 = np.random.randn(N)
    # random_y2 = np.random.randn(N) - 5

    date = [datetime(year=2020, month=m, day=i) for m in range(6, 9) for i in range(1, 31)]
    patient_adh = np.random.randn(90) + 90
    rx_adh = np.random.randn(90) + 80

    # Create traces
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=date, y=patient_adh, mode='lines', name='lines'))
    fig.add_trace(go.Scatter(x=date, y=rx_adh, mode='lines', name='lines'))

    fig.update_layout(
        title="Adherence rates over time",
        xaxis_title="Date",
        yaxis_title="Adherence %",
        font=dict(
            color="#7f7f7f"
        )
    )

    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1m", step="month", stepmode="backward"),
                dict(count=6, label="6m", step="month", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(step="all")
            ])
        )
    )

    output = plotly.offline.plot(fig, include_plotlyjs=False,
                                 output_type='div')

    return output

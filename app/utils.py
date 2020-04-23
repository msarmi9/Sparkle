from datetime import datetime, timedelta
import math


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

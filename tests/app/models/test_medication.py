"""
Tests each class in the ``app.medication`` module.
"""

from datetime import datetime

from app.medication import Prescription


# Prescription with an expired start date
# Treatment has also ended, as all medication should have been consumed prior to today.
rx_past = Prescription(
    drug="TestDrug1",
    desc="test",
    strength=30,
    strength_unit="mg",
    quantity=30,
    form="tab",
    amount=1,
    route="oral",
    freq=1,
    freq_repeat=1,
    freq_repeat_unit="day",
    duration=1,
    duration_unit="month",
    refills=0,
    time_of_day="AM",
    start_date=datetime.fromisoformat("2000-01-01"),
    created=datetime.fromisoformat("2000-01-01"),
)

# Prescription with future start date
rx_future = Prescription(
    drug="TestDrug2",
    desc="test",
    strength=30,
    strength_unit="mg",
    quantity=30,
    form="tab",
    amount=1,
    route="oral",
    freq=1,
    freq_repeat=1,
    freq_repeat_unit="day",
    duration=1,
    duration_unit="month",
    refills=0,
    time_of_day="AM",
    start_date=datetime.fromisoformat("2999-12-31"),
    created=datetime.fromisoformat("2999-12-31"),
)


class TestPrescription:
    """Tests for ``medication.Prescription`` class."""

    def test_has_started(self):
        """Only prescriptions with expired start date are marked as started."""
        assert rx_past.has_started()
        assert not rx_future.has_started()

    def test_is_adherent(self):
        """New prescriptions are marked as non-adherent by default."""
        assert not rx_past.is_adherent()
        assert not rx_future.is_adherent()

    def test_frac_on_time(self):
        """New prescriptions have no intakes marked on time by default."""
        assert rx_past.frac_on_time() == 0
        assert rx_future.frac_on_time() == 0

    def test_frac_required_intakes(self):
        """Completed treatments have no required intakes; future treatments do."""
        assert rx_past.frac_required_intakes() == 0
        assert rx_future.frac_required_intakes() == 1

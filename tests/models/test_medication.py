"""
Tests each class in the ``sparkle.medication`` module.
"""


class TestPrescription:
    """Tests for ``medication.Prescription`` class."""

    def test_has_started(self, rx_past, rx_new):
        """Prescriptions with current or expired start date are marked as started."""
        assert rx_past.has_started()
        assert rx_new.has_started()

    def test_is_adherent(self, rx_past):
        """Prescriptions with no intakes are marked non-adherent."""
        assert not rx_past.is_adherent()

    def test_frac_on_time(self, rx_past, rx_new):
        """Prescriptions with no intakes are marked not on time."""
        assert rx_past.frac_on_time() == 0
        assert rx_new.frac_on_time() == 0

    def test_frac_required_intakes(self, rx_past, rx_new):
        """Completed treatments have no required intakes; new treatments do."""
        assert rx_past.frac_required_intakes() == 0
        assert rx_new.frac_required_intakes() == 1

    def test_next_refill_date(self, rx_past, rx_new):
        """Past prescriptions have no refill date; new ones with refills > 0 do."""
        assert not rx_past.next_refill_date()
        assert rx_new.next_refill_date() > rx_new.start_date

    def test_days_until_refill(self, rx_past, rx_new):
        """Past treatments have no refills remaining; new ones with refills > 0 do."""
        assert not rx_past.days_until_refill()
        assert rx_new.days_until_refill() > 0

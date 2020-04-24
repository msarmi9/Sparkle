from app.classes import *
from datetime import datetime

def test_prescription_fns():
	doctor = User('Testuserfirst', 'Testuserlast', 'testuser',
				  'testuser@gmail.com', '123')
	patient = Patient(firstname='Testfirst', lastname='Testlast',
					  email='test@gmail.com', age=50, weight=150,
					  user=doctor)
	rx1 = Prescription(drug='TestDrug1', desc='test', strength=30,
					   strength_unit='mg', quantity=30, form='tab',
					   amount=1, route='oral', freq=1, freq_repeat=1,
					   freq_repeat_unit='day', duration=1,
					   duration_unit='month', refills=0, time_of_day='AM',
					   start_date=datetime.strptime('2020-04-01', '%Y-%m-%d'),
					   created=datetime.strptime('2020-04-01', '%Y-%m-%d'),
					   patient=patient)
	rx2 = Prescription(drug='TestDrug2', desc='test', strength=30,
					   strength_unit='mg', quantity=30, form='tab',
					   amount=1, route='oral', freq=1, freq_repeat=1,
					   freq_repeat_unit='day', duration=1,
					   duration_unit='month', refills=0, time_of_day='AM',
					   start_date=datetime.strptime('2020-04-10', '%Y-%m-%d'),
					   created=datetime.strptime('2020-04-10', '%Y-%m-%d'),
					   patient=patient)
	assert rx1.has_started() is True
	assert rx1.is_adherent() is False
	assert rx1.frac_on_time() == 1.0
	assert rx1.frac_required_intakes() == 0.0

	assert rx2.has_started() is True
	assert rx2.is_adherent() is False
	assert rx2.frac_on_time() == 1.0
	assert rx2.frac_required_intakes() == 0.0
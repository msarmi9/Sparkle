from flask import Blueprint
from flask import render_template
from flask_login import current_user
from flask_login import login_required

from sparkle import ploting
from sparkle.models.persons import Patient

bp = Blueprint("dashboard", __name__)


@bp.route("/dashboard")
@login_required
def dashboard():
    """Render medication adherence plots, trends, and analytics."""
    patients = Patient.query.filter_by(doctor_id=current_user.id).all()
    rxs = []
    for p in patients:
        rxs += p.prescriptions
    adh_over_time = ploting.plot_adherence_rates_over_time(patients, rxs)
    top_general_adh = ploting.plot_top_general_adherence_by_drug_name(rxs, n=5)
    top_ontime_adh = ploting.plot_top_ontime_adherence_by_drug_name(rxs, n=5)

    return render_template(
        "dashboard/dashboard.html",
        adh_over_time=adh_over_time,
        top_general_adh=top_general_adh,
        top_ontime_adh=top_ontime_adh,
    )

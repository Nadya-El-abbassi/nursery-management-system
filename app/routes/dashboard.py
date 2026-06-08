from flask import Blueprint, render_template

from app.services.dashboard_service import DashboardService

bp = Blueprint("dashboard", __name__)
dashboard_service = DashboardService()


@bp.route("/")
def index():
    data = dashboard_service.get_dashboard_data()
    return render_template(
        "index.html",
        stats=data["stats"],
        plant_count=data["plant_count"],
        total_stock=data["total_stock"],
        low_stock=data["low_stock"],
    )

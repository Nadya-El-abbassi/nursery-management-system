from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.services.plant_service import PlantService
from app.services.sale_service import SaleService

bp = Blueprint("sales", __name__, url_prefix="/sales")
sale_service = SaleService()
plant_service = PlantService()


@bp.route("/")
def list_sales():
    sales = sale_service.list_sales()
    stats = sale_service.get_stats()
    return render_template("sales/list.html", sales=sales, stats=stats)


@bp.route("/new", methods=["GET", "POST"])
def new_sale():
    plants = [p for p in plant_service.list_plants() if p["quantity"] > 0]

    if request.method == "POST":
        try:
            sale_service.register_sale(request.form)
            flash("Vente enregistrée. Stock mis à jour.", "success")
            return redirect(url_for("sales.list_sales"))
        except (ValueError, TypeError) as exc:
            flash(str(exc), "error")

    return render_template("sales/form.html", plants=plants)

from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.services.plant_service import PlantService

bp = Blueprint("plants", __name__, url_prefix="/plants")
from app.factories.service_factory import ServiceFactory

plant_service = ServiceFactory.create_plant_service()


@bp.route("/")
def list_plants():
    plants = plant_service.list_plants()
    low_stock_ids = {p["id"] for p in plant_service.list_low_stock()}
    return render_template(
        "plants/list.html",
        plants=plants,
        low_stock_ids=low_stock_ids,
    )


@bp.route("/add", methods=["GET", "POST"])
def add_plant():
    if request.method == "POST":
        try:
            plant_service.add_plant(request.form)
            flash("Plante ajoutée avec succès.", "success")
            return redirect(url_for("plants.list_plants"))
        except (ValueError, TypeError) as exc:
            flash(str(exc), "error")

    return render_template("plants/form.html", plant=None, action="add")


@bp.route("/<int:plant_id>/edit", methods=["GET", "POST"])
def edit_plant(plant_id):
    plant = plant_service.get_plant(plant_id)
    if plant is None:
        flash("Plante introuvable.", "error")
        return redirect(url_for("plants.list_plants"))

    if request.method == "POST":
        try:
            plant_service.edit_plant(plant_id, request.form)
            flash("Plante mise à jour.", "success")
            return redirect(url_for("plants.list_plants"))
        except (ValueError, TypeError) as exc:
            flash(str(exc), "error")

    return render_template("plants/form.html", plant=plant, action="edit")


@bp.route("/<int:plant_id>/delete", methods=["POST"])
def delete_plant(plant_id):
    try:
        plant_service.remove_plant(plant_id)
        flash("Plante supprimée.", "success")
    except ValueError as exc:
        flash(str(exc), "error")
    return redirect(url_for("plants.list_plants"))

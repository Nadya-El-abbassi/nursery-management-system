from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.services.category_service import CategoryService

bp = Blueprint("categories", __name__, url_prefix="/categories")
category_service = CategoryService()


@bp.route("/")
def list_categories():
    categories = category_service.list_categories()
    return render_template("categories/list.html", categories=categories)


@bp.route("/add", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        try:
            category_service.add_category(request.form)
            flash("Catégorie ajoutée avec succès.", "success")
            return redirect(url_for("categories.list_categories"))
        except (ValueError, TypeError) as exc:
            flash(str(exc), "error")

    return render_template("categories/form.html", category=None, action="add")


@bp.route("/<int:category_id>/edit", methods=["GET", "POST"])
def edit_category(category_id):
    category = category_service.get_category(category_id)
    if category is None:
        flash("Catégorie introuvable.", "error")
        return redirect(url_for("categories.list_categories"))

    if request.method == "POST":
        try:
            category_service.edit_category(category_id, request.form)
            flash("Catégorie mise à jour.", "success")
            return redirect(url_for("categories.list_categories"))
        except (ValueError, TypeError) as exc:
            flash(str(exc), "error")

    return render_template("categories/form.html", category=category, action="edit")


@bp.route("/<int:category_id>/delete", methods=["POST"])
def delete_category(category_id):
    try:
        category_service.remove_category(category_id)
        flash("Catégorie supprimée.", "success")
    except ValueError as exc:
        flash(str(exc), "error")
    return redirect(url_for("categories.list_categories"))

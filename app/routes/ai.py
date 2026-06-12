from flask import Blueprint, flash, render_template, request

from app.services.ai_service import AIService

bp = Blueprint("ai", __name__, url_prefix="/ai")
ai_service = AIService()


@bp.route("/", methods=["GET", "POST"])
def advisor():
    result = None
    if request.method == "POST":
        action = request.form.get("action", "recommend")
        try:
            if action == "recommend":
                result = {
                    "type": "recommend",
                    "data": ai_service.recommend_plants(
                        request.form.get("garden_description", "")
                    ),
                }
            elif action == "description":
                result = {
                    "type": "description",
                    "data": ai_service.generate_description(
                        request.form.get("plant_name", ""),
                        request.form.get("species", ""),
                    ),
                }
            elif action == "stock":
                result = {
                    "type": "stock",
                    "data": ai_service.advise_stock_management(
                        request.form.get("stock_question", "")
                    ),
                }
        except ValueError as exc:
            flash(str(exc), "error")
        except Exception as exc:
            flash(ai_service.format_api_error(exc), "error")

    return render_template(
        "ai/advisor.html",
        result=result,
        ai_configured=ai_service.is_configured(),
    )
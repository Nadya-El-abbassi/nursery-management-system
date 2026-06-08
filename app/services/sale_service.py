"""gestion des ventes."""

from app.repositories.plant_repository import PlantRepository
from app.repositories.sale_repository import SaleRepository


class SaleService:
    def __init__(self, sale_repo=None, plant_repo=None):
        self.sale_repo = sale_repo or SaleRepository()
        self.plant_repo = plant_repo or PlantRepository()

    def list_sales(self):
        return self.sale_repo.find_all()

    def register_sale(self, form_data):
        plant_id = int(form_data.get("plant_id", 0))
        quantity = int(form_data.get("quantity", 0))
        customer_name = form_data.get("customer_name", "").strip()

        if quantity <= 0:
            raise ValueError("La quantité doit être supérieure à 0.")

        plant = self.plant_repo.find_by_id(plant_id)
        if plant is None:
            raise ValueError("Plante introuvable.")

        if plant["quantity"] < quantity:
            raise ValueError(
                f"Stock insuffisant : {plant['quantity']} disponible(s), "
                f"{quantity} demandé(s)."
            )

        unit_price = plant["price"]
        total_price = round(unit_price * quantity, 2)

        sale_id = self.sale_repo.create(
            plant_id, quantity, unit_price, total_price, customer_name
        )
        self.plant_repo.update_quantity(plant_id, plant["quantity"] - quantity)
        return sale_id

    def get_stats(self):
        return {
            "total_revenue": self.sale_repo.total_revenue(),
            "sales_today": self.sale_repo.count_today(),
            "revenue_today": self.sale_repo.revenue_today(),
        }

"""alertes stock et données pour l'IA."""

from app.repositories.plant_repository import PlantRepository


class StockAlertService:
    def __init__(self, repository=None):
        self.repository = repository or PlantRepository()

    def get_low_stock(self):
        return self.repository.find_low_stock()

    def get_out_of_stock(self):
        return [p for p in self.repository.find_all() if p["quantity"] == 0]

    def get_critical_stock(self):
        return self.get_low_stock()

    def get_catalog_for_ai(self):
        return self.repository.get_catalog_for_ai()

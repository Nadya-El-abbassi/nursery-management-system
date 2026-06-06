"""gestion des plantes."""

from app.repositories.plant_repository import PlantRepository


class PlantService:
    def __init__(self, repository=None):
        self.repository = repository or PlantRepository()

    def list_plants(self):
        return self.repository.find_all()

    def get_plant(self, plant_id):
        return self.repository.find_by_id(plant_id)

    def list_low_stock(self):
        return self.repository.find_low_stock()

    def add_plant(self, form_data):
        name = form_data.get("name", "").strip()
        species = form_data.get("species", "").strip()
        price = float(form_data.get("price", 0))
        quantity = int(form_data.get("quantity", 0))
        alert_threshold = int(form_data.get("alert_threshold", 5))
        description = form_data.get("description", "").strip()

        if not name or not species:
            raise ValueError("Le nom et l'espèce sont obligatoires.")
        if price < 0 or quantity < 0 or alert_threshold < 0:
            raise ValueError("Les valeurs numériques doivent être positives.")

        return self.repository.create(
            name, species, price, quantity, alert_threshold, description
        )

    def edit_plant(self, plant_id, form_data):
        plant = self.repository.find_by_id(plant_id)
        if plant is None:
            raise ValueError("Plante introuvable.")

        name = form_data.get("name", "").strip()
        species = form_data.get("species", "").strip()
        price = float(form_data.get("price", 0))
        quantity = int(form_data.get("quantity", 0))
        alert_threshold = int(form_data.get("alert_threshold", 5))
        description = form_data.get("description", "").strip()

        if not name or not species:
            raise ValueError("Le nom et l'espèce sont obligatoires.")

        self.repository.update(
            plant_id, name, species, price, quantity, alert_threshold, description
        )

    def remove_plant(self, plant_id):
        plant = self.repository.find_by_id(plant_id)
        if plant is None:
            raise ValueError("Plante introuvable.")
        self.repository.delete(plant_id)

    def count_plants(self):
        return len(self.repository.find_all())

    def total_stock_units(self):
        plants = self.repository.find_all()
        return sum(p["quantity"] for p in plants)

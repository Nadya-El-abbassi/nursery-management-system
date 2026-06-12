"""gestion des plantes."""

from app.repositories.plant_repository import PlantRepository


class PlantService:

    def __init__(self, repository=None):
        self.repository = repository or PlantRepository()

    def _validate_plant_data(self, form_data):
        """
        Validation centralisée des données d'une plante.
        """

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

        return {
            "name": name,
            "species": species,
            "price": price,
            "quantity": quantity,
            "alert_threshold": alert_threshold,
            "description": description,
        }

    def list_plants(self):
        return self.repository.find_all()

    def get_plant(self, plant_id):
        return self.repository.find_by_id(plant_id)

    def list_low_stock(self):
        return self.repository.find_low_stock()

    def add_plant(self, form_data):

        data = self._validate_plant_data(form_data)

        return self.repository.create(
            data["name"],
            data["species"],
            data["price"],
            data["quantity"],
            data["alert_threshold"],
            data["description"],
        )

    def edit_plant(self, plant_id, form_data):

        plant = self.repository.find_by_id(plant_id)

        if plant is None:
            raise ValueError("Plante introuvable.")

        data = self._validate_plant_data(form_data)

        self.repository.update(
            plant_id,
            data["name"],
            data["species"],
            data["price"],
            data["quantity"],
            data["alert_threshold"],
            data["description"],
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

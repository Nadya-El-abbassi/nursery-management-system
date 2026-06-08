from app.repositories.plant_repository import PlantRepository
from app.services.plant_service import PlantService


class ServiceFactory:

    @staticmethod
    def create_plant_service():
        repository = PlantRepository()
        return PlantService(repository)
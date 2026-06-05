"""gestion des catégories."""

from app.repositories.category_repository import CategoryRepository


class CategoryService:
    def __init__(self, repository=None):
        self.repository = repository or CategoryRepository()

    def list_categories(self):
        return self.repository.find_all()

    def get_category(self, category_id):
        return self.repository.find_by_id(category_id)

    def add_category(self, form_data):
        name = form_data.get("name", "").strip()
        description = form_data.get("description", "").strip()

        if not name:
            raise ValueError("Le nom de la catégorie est obligatoire.")

        return self.repository.create(name, description)

    def edit_category(self, category_id, form_data):
        category = self.repository.find_by_id(category_id)
        if category is None:
            raise ValueError("Catégorie introuvable.")

        name = form_data.get("name", "").strip()
        description = form_data.get("description", "").strip()

        if not name:
            raise ValueError("Le nom de la catégorie est obligatoire.")

        self.repository.update(category_id, name, description)

    def remove_category(self, category_id):
        category = self.repository.find_by_id(category_id)
        if category is None:
            raise ValueError("Catégorie introuvable.")
        self.repository.delete(category_id)

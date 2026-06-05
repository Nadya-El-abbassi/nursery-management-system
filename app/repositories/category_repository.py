"""catégories produits (plantes, engrais…)."""

from app.database import get_db


class CategoryRepository:
    def find_all(self):
        db = get_db()
        return db.execute(
            "SELECT * FROM categories ORDER BY name ASC"
        ).fetchall()

    def find_by_id(self, category_id):
        db = get_db()
        return db.execute(
            "SELECT * FROM categories WHERE id = ?",
            (category_id,),
        ).fetchone()

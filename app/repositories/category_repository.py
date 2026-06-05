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

    def create(self, name, description=""):
        db = get_db()
        cursor = db.execute(
            """
            INSERT INTO categories (name, description)
            VALUES (?, ?)
            """,
            (name, description),
        )
        db.commit()
        return cursor.lastrowid

    def update(self, category_id, name, description=""):
        db = get_db()
        db.execute(
            """
            UPDATE categories
            SET name = ?, description = ?
            WHERE id = ?
            """,
            (name, description, category_id),
        )
        db.commit()

    def delete(self, category_id):
        db = get_db()
        db.execute("DELETE FROM categories WHERE id = ?", (category_id,))
        db.commit()

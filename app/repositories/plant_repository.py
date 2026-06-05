"""accès aux données plantes."""

from app.database import get_db


class PlantRepository:
    def find_all(self):
        db = get_db()
        return db.execute(
            "SELECT * FROM plants ORDER BY name ASC"
        ).fetchall()

    def find_by_id(self, plant_id):
        db = get_db()
        return db.execute(
            "SELECT * FROM plants WHERE id = ?",
            (plant_id,),
        ).fetchone()

    def find_low_stock(self):
        db = get_db()
        return db.execute(
            """
            SELECT * FROM plants
            WHERE quantity <= alert_threshold
            ORDER BY quantity ASC
            """
        ).fetchall()

    def create(self, name, species, price, quantity, alert_threshold, description=""):
        db = get_db()
        cursor = db.execute(
            """
            INSERT INTO plants (name, species, price, quantity, alert_threshold, description)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (name, species, price, quantity, alert_threshold, description),
        )
        db.commit()
        return cursor.lastrowid

    def update(self, plant_id, name, species, price, quantity, alert_threshold, description=""):
        db = get_db()
        db.execute(
            """
            UPDATE plants
            SET name = ?, species = ?, price = ?, quantity = ?,
                alert_threshold = ?, description = ?
            WHERE id = ?
            """,
            (name, species, price, quantity, alert_threshold, description, plant_id),
        )
        db.commit()

    def delete(self, plant_id):
        db = get_db()
        db.execute("DELETE FROM plants WHERE id = ?", (plant_id,))
        db.commit()

    def update_quantity(self, plant_id, new_quantity):
        db = get_db()
        db.execute(
            "UPDATE plants SET quantity = ? WHERE id = ?",
            (new_quantity, plant_id),
        )
        db.commit()

    def get_catalog_for_ai(self):
        return [
            {
                "id": p["id"],
                "name": p["name"],
                "species": p["species"],
                "price": p["price"],
                "quantity": p["quantity"],
                "description": p["description"] or "",
            }
            for p in self.find_all()
            if p["quantity"] > 0
        ]

"""accès aux données ventes."""

from app.database import get_db


class SaleRepository:
    def find_all(self, limit=50):
        db = get_db()
        return db.execute(
            """
            SELECT s.*, p.name AS plant_name, p.species AS plant_species
            FROM sales s
            JOIN plants p ON p.id = s.plant_id
            ORDER BY s.sold_at DESC
            LIMIT ?
            """,
            (limit,),
        ).fetchall()

    def create(self, plant_id, quantity, unit_price, total_price, customer_name=""):
        db = get_db()
        cursor = db.execute(
            """
            INSERT INTO sales (plant_id, quantity, unit_price, total_price, customer_name)
            VALUES (?, ?, ?, ?, ?)
            """,
            (plant_id, quantity, unit_price, total_price, customer_name),
        )
        db.commit()
        return cursor.lastrowid

    def total_revenue(self):
        db = get_db()
        row = db.execute(
            "SELECT COALESCE(SUM(total_price), 0) AS total FROM sales"
        ).fetchone()
        return row["total"] if row else 0

    def count_today(self):
        db = get_db()
        row = db.execute(
            """
            SELECT COUNT(*) AS count FROM sales
            WHERE date(sold_at) = date('now', 'localtime')
            """
        ).fetchone()
        return row["count"] if row else 0

    def revenue_today(self):
        db = get_db()
        row = db.execute(
            """
            SELECT COALESCE(SUM(total_price), 0) AS total FROM sales
            WHERE date(sold_at) = date('now', 'localtime')
            """
        ).fetchone()
        return row["total"] if row else 0

"""Service dashboard — statistiques et données graphiques."""

from app.services.plant_service import PlantService
from app.services.sale_service import SaleService
from app.services.stock_alert_service import StockAlertService


class DashboardService:
    def __init__(self):
        self.plant_service = PlantService()
        self.sale_service = SaleService()
        self.stock_alert_service = StockAlertService()

    def get_dashboard_data(self):
        stats = self.sale_service.get_stats()
        return {
            "stats": stats,
            "plant_count": self.plant_service.count_plants(),
            "total_stock": self.plant_service.total_stock_units(),
            "low_stock": self.stock_alert_service.get_critical_stock(),
        }

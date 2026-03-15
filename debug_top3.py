from src.config import get_settings
from src.db import get_engine
from src.repository import DashboardRepository
from src.service import DashboardService

settings = get_settings()
engine = get_engine(settings)
repo = DashboardRepository(engine)
service = DashboardService(repo)

filters = {"usuario_id": None, "num_intento": None, "modalidad": None, "max_presupuesto": 1500, "max_duracion": None, "carrera": None, "institucion": None}

res = service.get_dashboard_data(filters)
print('KPIS:', res['kpis'])
print('Top3 raw:')
for r in res['top3']:
    print(r)

from dataclasses import dataclass
from typing import Optional

@dataclass
class DashboardFilters:
    usuario_id: Optional[int] = None
    num_intento: Optional[int] = None
    modalidad: Optional[str] = None
    max_presupuesto: Optional[int] = None
    max_duracion: Optional[int] = None
    carrera: Optional[str] = None
    institucion: Optional[str] = None
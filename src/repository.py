import logging
import pandas as pd
from sqlalchemy import text
from sqlalchemy.exc import OperationalError
from sqlalchemy.engine import Engine

from src.queries import (
    FILTER_OPTIONS_SQL,
    ATTEMPTS_SQL,
    MODALITIES_SQL,
    DURATIONS_SQL,
    CAREERS_SQL,
    INSTITUTIONS_SQL,
    BASE_DATA_SQL,
    TOP3_SQL,
)
from src.queries import BASE_FROM_SQL

logger = logging.getLogger(__name__)


class DashboardRepository:
    def __init__(self, engine: Engine):
        self.engine = engine

    def _read_df(self, sql: str, params: dict | None = None) -> pd.DataFrame:
        try:
            logger.debug("EJECUTANDO QUERY...")
            logger.debug("SQL: %s", sql)
            logger.debug("PARAMS: %s", params)

            with self.engine.connect() as conn:
                df = pd.read_sql(text(sql), conn, params=params or {})

                logger.debug("FILAS DEVUELTAS: %s", len(df))
                logger.debug("COLUMNAS: %s", list(df.columns))
                logger.debug("HEAD:\n%s", df.head())

            return df

        except Exception as e:
            # if the error is due to unknown column (1054), try a minimal safe fallback query
            msg = str(e)
            logger.exception("ERROR EN QUERY: %s", e)
            if "Unknown column" in msg or (isinstance(e, OperationalError) and "1054" in msg):
                logger.debug("Attempting fallback minimal query due to missing columns")
                fallback_sql = """
SELECT
    u.idUsuario AS id_usuario,
    it.idIntento AS id_intento,
    it.numeroIntento AS num_intento,
    c.nombre AS carrera,
    i.nombre AS institucion,
    oc.modalidad AS modalidad,
    oc.costoPension AS costo_pension,
    rc.afinidad AS afinidad
FROM usuario u
INNER JOIN intentotest it
    ON it.id_usuario = u.idUsuario
INNER JOIN recomendacion r
    ON r.id_intento = it.idIntento
INNER JOIN recomendacioncarrera rc
    ON rc.id_recomendacion = r.idRecomendacion
INNER JOIN carrera c
    ON c.idCarrera = rc.id_carrera
INNER JOIN ofertacarrera oc
    ON oc.id_carrera = c.idCarrera
INNER JOIN institucion i
    ON i.idInstitucion = oc.id_institucion
LIMIT 100;"""
                try:
                    with self.engine.connect() as conn:
                        df2 = pd.read_sql(text(fallback_sql), conn)
                        logger.debug("Fallback filas: %s", len(df2))
                        return df2
                except Exception:
                    logger.exception("Fallback query also failed")
            raise


    def get_filter_options(self) -> dict:
        # Build a user list with id and label (email) so the UI can show names while filtering by id
        try:
            user_sql = f"""
SELECT DISTINCT u.idUsuario AS id, u.email AS email
{BASE_FROM_SQL}
ORDER BY u.idUsuario;
"""
            users_df = self._read_df(user_sql)
            usuarios = []
            if not users_df.empty:
                for _, row in users_df.iterrows():
                    try:
                        uid = int(row.get("id"))
                    except Exception:
                        continue
                    label = str(row.get("email")) if row.get("email") is not None else str(uid)
                    usuarios.append({"id": uid, "label": label})
        except Exception:
            logger.exception("Error building usuarios list, falling back to id-only list")
            usuarios = self._read_df(FILTER_OPTIONS_SQL)["value"].dropna().astype(int).tolist()

        return {
            "usuarios": usuarios,
            "intentos": self._read_df(ATTEMPTS_SQL)["value"].dropna().astype(int).tolist(),
            "modalidades": self._read_df(MODALITIES_SQL)["value"].dropna().astype(str).tolist(),
            "duraciones": self._read_df(DURATIONS_SQL)["value"].dropna().astype(int).tolist(),
            "carreras": self._read_df(CAREERS_SQL)["value"].dropna().astype(str).tolist(),
            "instituciones": self._read_df(INSTITUTIONS_SQL)["value"].dropna().astype(str).tolist(),
        }

    def get_base_data(self, filters: dict) -> pd.DataFrame:
        return self._read_df(BASE_DATA_SQL, filters)

    def get_top3(self, filters: dict) -> pd.DataFrame:
        return self._read_df(TOP3_SQL, filters)

    def get_user_role(self, user_id: int) -> str | None:
        try:
            sql = "SELECT rol FROM usuario WHERE idUsuario = :uid LIMIT 1;"
            with self.engine.connect() as conn:
                df = pd.read_sql(text(sql), conn, params={"uid": user_id})
            if not df.empty and "rol" in df.columns:
                return df.iloc[0]["rol"]
            return None
        except Exception:
            logger.exception("Error reading user role for id %s", user_id)
            return None

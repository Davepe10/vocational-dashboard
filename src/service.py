import logging
import re
import html as _html
import pandas as pd
import streamlit as st
from src.repository import DashboardRepository

logger = logging.getLogger(__name__)


class DashboardService:
    def __init__(self, repo: DashboardRepository):
        self.repo = repo

    @st.cache_data(ttl=300, show_spinner=False)
    def get_filter_options(_self):
        data = _self.repo.get_filter_options()
        data["budget_options"] = ["Todas", 500, 800, 1000, 1500, 2000, 2500, 3000]
        return data

    @st.cache_data(ttl=180, show_spinner=False)
    def get_dashboard_data(_self, filters: dict) -> dict:
        df = _self.repo.get_base_data(filters)
        top3 = _self.repo.get_top3(filters)

        logger.debug("filas leidas (raw): %s", len(df))
        logger.debug("columnas leidas: %s", list(df.columns))

        # Evitar duplicados por multiples sedes/ofertas: priorizar mayor afinidad y menor costo
        if not df.empty:
            df = df.sort_values([col for col in ["afinidad", "costo_pension"] if col in df.columns], ascending=[False, True][:2])
            if "id_oferta" in df.columns:
                before = len(df)
                df = df.drop_duplicates(subset=["id_oferta"], keep="first")
                logger.debug("dedupe por id_oferta %s -> %s", before, len(df))
            else:
                # dedupe by a stable set of columns if no oferta id
                subset = [c for c in ["carrera", "institucion", "modalidad", "duracion", "costo_pension"] if c in df.columns]
                if subset:
                    before = len(df)
                    df = df.drop_duplicates(subset=subset, keep="first")
                    logger.debug("dedupe por %s %s -> %s", subset, before, len(df))

        if df.empty:
            empty_df = pd.DataFrame()
            return {
                "kpis": {
                    "opciones_compatibles": 0,
                    "mensualidad_promedio": 0,
                    "duracion_promedio": 0,
                    "top_modalidad": "Sin datos",
                    "rango_presupuesto": "Sin datos",
                },
                "bubble_df": empty_df,
                "modality_df": empty_df,
                "top3": [],
                "comparison_df": empty_df,
            }

        # normalización ligera por si hay nulls y defensa ante columnas faltantes
        for col in ["costo_pension", "costo_matricula", "duracion", "afinidad"]:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors="coerce")
            else:
                df[col] = pd.NA

        if "sede" in df.columns:
            df["sede"] = df["sede"].fillna("Sin sede")
        else:
            df["sede"] = "Sin sede"

        if "modalidad" in df.columns:
            df["modalidad"] = df["modalidad"].fillna("Sin modalidad")
        else:
            df["modalidad"] = "Sin modalidad"

        # KPIs defensivos
        opciones_compatibles = int(df["carrera"].nunique()) if "carrera" in df.columns else 0
        mensualidad_promedio = float(df["costo_pension"].dropna().mean()) if "costo_pension" in df.columns and df["costo_pension"].notna().any() else 0
        duracion_promedio = float(df["duracion"].dropna().mean()) if "duracion" in df.columns and df["duracion"].notna().any() else 0
        top_modalidad = df["modalidad"].mode().iloc[0] if ("modalidad" in df.columns and not df["modalidad"].mode().empty) else "Sin datos"
        if "costo_pension" in df.columns and df["costo_pension"].notna().any():
            try:
                rango_presupuesto = f"S/. {int(df['costo_pension'].min())} - S/. {int(df['costo_pension'].max())}"
            except Exception:
                rango_presupuesto = "Sin datos"
        else:
            rango_presupuesto = "Sin datos"

        kpis = {
            "opciones_compatibles": opciones_compatibles,
            "mensualidad_promedio": mensualidad_promedio,
            "duracion_promedio": duracion_promedio,
            "top_modalidad": top_modalidad,
            "rango_presupuesto": rango_presupuesto,
        }

        # Gráfico burbuja: agrupar solo con columnas disponibles
        gb_cols = [c for c in ["carrera", "duracion", "institucion"] if c in df.columns]
        if gb_cols:
            bubble_df = (
                df.groupby(gb_cols, as_index=False)
                .agg(
                    costo_pension=("costo_pension", "mean") if "costo_pension" in df.columns else ("costo_pension", "first"),
                    afinidad=("afinidad", "max") if "afinidad" in df.columns else ("afinidad", "first"),
                )
            )
            if "duracion" in bubble_df.columns:
                bubble_df["tipo_origen"] = bubble_df["duracion"].apply(
                    lambda x: "Universidad" if pd.notna(x) and x >= 5 else "Instituto"
                )
            else:
                bubble_df["tipo_origen"] = "Instituto"
        else:
            bubble_df = pd.DataFrame()

        # Modalidad: programas por modalidad (defensivo)
        if "modalidad" in df.columns and "carrera" in df.columns:
            modality_df = (
                df.groupby("modalidad", as_index=False)
                .agg(programas=("carrera", "nunique"))
            )
        else:
            modality_df = pd.DataFrame()

        # Comparador: asegurar columnas y evitar KeyError
        desired = [
            "carrera",
            "institucion",
            "sede",
            "modalidad",
            "duracion",
            "costo_matricula",
            "costo_pension",
            "afinidad",
            "razon",
        ]
        for col in desired:
            if col not in df.columns:
                df[col] = pd.NA

        comparison_df = (
            df[desired]
            .drop_duplicates()
            .sort_values([c for c in ["afinidad", "costo_pension"] if c in df.columns], ascending=[False, True][:2])
        )

        # sanitize top3: strip HTML tags from string fields and ensure numeric columns are numeric
        if top3 is None:
            top3_cards = []
        else:
            def _strip_tags(val):
                if pd.isna(val):
                    return val
                if isinstance(val, str):
                    # unescape HTML entities then remove tags
                    txt = _html.unescape(val)
                    return re.sub(r"<[^>]+>", "", txt).strip()
                return val

            for c in top3.select_dtypes(include=[object]).columns:
                top3[c] = top3[c].apply(_strip_tags)
            for c in ["afinidad", "costo_matricula", "costo_pension", "duracion"]:
                if c in top3.columns:
                    top3[c] = pd.to_numeric(top3[c], errors="coerce")

            top3_cards = top3.to_dict(orient="records")

        return {
            "kpis": kpis,
            "bubble_df": bubble_df,
            "modality_df": modality_df,
            "top3": top3_cards,
            "comparison_df": comparison_df,
        }

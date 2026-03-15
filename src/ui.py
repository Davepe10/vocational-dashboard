import re
import streamlit as st
import plotly.express as px
import pandas as pd
import html as _html
import textwrap


def render_global_css():
    st.markdown("""
    <style>
        .stApp {
            background: linear-gradient(180deg, #f6f7fb 0%, #f3f5fb 100%);
        }

        .block-container {
            max-width: 1380px;
            padding-top: 1.8rem;
            padding-bottom: 2rem;
        }

        .main-title {
            font-size: 2.2rem;
            font-weight: 800;
            color: #1e293b;
            margin-bottom: 0.15rem;
        }

        .subtitle {
            color: #64748b;
            margin-bottom: 1.3rem;
            font-size: 1rem;
        }

        .kpi-card {
            background: #ffffff;
            border-radius: 20px;
            padding: 22px;
            border: 1px solid #e9edf5;
            box-shadow: 0 8px 30px rgba(15, 23, 42, 0.06);
            min-height: 132px;
        }

        .kpi-label {
            font-size: 0.82rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-bottom: 10px;
        }

        .kpi-value {
            font-size: 2rem;
            font-weight: 800;
            color: #0f172a;
            line-height: 1.1;
        }

        .kpi-sub {
            color: #64748b;
            margin-top: 8px;
            font-size: 0.92rem;
        }

        .section-card {
            background: #ffffff;
            border-radius: 22px;
            padding: 18px 18px 10px 18px;
            border: 1px solid #e9edf5;
            box-shadow: 0 8px 30px rgba(15, 23, 42, 0.06);
        }

        .section-title {
            font-size: 1.2rem;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 8px;
        }

        .top3-title {
            margin-top: 18px;
            margin-bottom: 10px;
            font-size: 1.8rem;
            font-weight: 800;
            color: #0f172a;
        }

        .career-card {
            background: #ffffff;
            border-radius: 24px;
            padding: 22px;
            border: 1px solid #e9edf5;
            box-shadow: 0 10px 35px rgba(15, 23, 42, 0.08);
            position: relative;
            min-height: 355px;
        }

        .badge-match {
            position: absolute;
            top: 0;
            right: 0;
            background: #111827;
            color: white;
            font-weight: 800;
            padding: 10px 14px;
            border-radius: 0 24px 0 16px;
            font-size: 0.9rem;
        }

        .muted {
            color: #475569;
            font-size: 0.93rem;
        }

        .metric-box {
            background: #f8fafc;
            border-radius: 16px;
            padding: 14px;
            margin-top: 14px;
            border: 1px solid #eef2f7;
            color: #0f172a;
            word-break: break-word;
            white-space: pre-wrap;
        }

        .tag {
            display: inline-block;
            padding: 6px 10px;
            border-radius: 999px;
            font-size: 0.76rem;
            margin-right: 6px;
            margin-top: 8px;
            font-weight: 700;
        }

        .tag-presencial {
            background: #dbeafe;
            color: #2563eb;
        }

        .tag-virtual {
            background: #dcfce7;
            color: #16a34a;
        }

        .tag-semipresencial {
            background: #f3e8ff;
            color: #9333ea;
        }

        .filter-block {
            background: #ffffff;
            border-radius: 20px;
            padding: 12px;
            border: 1px solid #e9edf5;
            box-shadow: 0 8px 25px rgba(15, 23, 42, 0.05);
            margin-bottom: 18px;
        }

        div[data-baseweb="select"] > div {
            border-radius: 14px !important;
            min-height: 44px !important;
            border-color: #dbe3ee !important;
        }

        .stButton button {
            border-radius: 14px !important;
            min-height: 44px !important;
            font-weight: 700 !important;
            border: 1px solid #dbe3ee !important;
            background: white !important;
            color: #0f172a !important;
        }

        .stDataFrame {
            background: white !important;
            border-radius: 18px !important;
        }
        .badge-match { background:#6366F1; color:white; }
        .career-card .title { color: #0f172a; font-weight:800; }
        .career-card .institution { color:#6366F1; font-weight:700; }
        .career-card .sede { color:#475569; }
        .career-card .metric-label { color:#64748b; font-size:0.86rem; }
        .career-card .metric-value { color:#0f172a; font-weight:800; font-size:1rem; }
    </style>
    """, unsafe_allow_html=True)

    # Additional responsive tweaks
    st.markdown("""
    <style>
        /* Responsive adjustments */
        @media (max-width: 900px) {
            .block-container { padding-left: 12px !important; padding-right: 12px !important; }
            .main-title { font-size: 1.4rem !important; }
            .subtitle { font-size: 0.95rem !important; }
            .top3-title { font-size: 1.2rem !important; }
            .kpi-card { padding: 12px !important; min-height: 96px !important; }
            .kpi-value { font-size: 1.4rem !important; }
            .career-card { min-height: auto !important; padding: 14px !important; }
            .career-card .badge-match { position: static !important; display: inline-block !important; margin-bottom: 8px !important; border-radius: 10px !important; padding: 6px 10px !important; }
        }

        @media (max-width: 480px) {
            .kpi-card { min-height: 80px !important; }
            .kpi-value { font-size: 1.1rem !important; }
            .main-title { font-size: 1.1rem !important; }
            .career-card .title { font-size: 1.1rem !important; }
            .career-card .institution { font-size: 0.95rem !important; }
        }

        /* Subtle professional accent colors for headings */
        .section-title { color: #0b2545 !important; }
        .career-card { transition: transform .18s ease, box-shadow .18s ease; }
        .career-card:hover { transform: translateY(-6px); box-shadow: 0 18px 45px rgba(15,23,42,0.12); }
    </style>
    """, unsafe_allow_html=True)

    # Top3 rendering implemented below using Streamlit primitives (no raw HTML insertion)

def _get_modality_tag_class(modalidad: str) -> str:
    if modalidad == "Presencial":
        return "tag tag-presencial"
    if modalidad == "Virtual":
        return "tag tag-virtual"
    if modalidad == "Semipresencial":
        return "tag tag-semipresencial"
    return "tag"


def render_top3(top3: list[dict]):
    st.header("🏆 Tu Top 3 Personalizado")

    if not top3:
        st.info("No hay recomendaciones para los filtros seleccionados.")
        return

    cols = st.columns(3)

    def _clean_text(v):
        if v is None:
            return ""
        if not isinstance(v, str):
            return str(v)
        # remove tags and control whitespace
        t = _html.unescape(v)
        t = re.sub(r'(?is)<(script|style).*?>.*?</\1>', '', t)
        t = re.sub(r'<[^>]+>', '', t)
        t = _html.unescape(t)
        t = t.replace('\n', ' ').replace('\r', ' ')
        t = re.sub(r"\s+", " ", t).strip()
        if len(t) > 280:
            return t[:240].rstrip() + "..."
        return t

    for idx, raw_item in enumerate(top3[:3]):
        item = {k: raw_item.get(k) for k in raw_item.keys()}
        area = _clean_text(item.get('area'))
        carrera = _clean_text(item.get('carrera'))
        institucion = _clean_text(item.get('institucion'))
        sede = _clean_text(item.get('sede') or 'Sin sede')
        razon = _clean_text(item.get('razon') or '')
        modalidad = _clean_text(item.get('modalidad') or '')
        try:
            afinidad = float(item.get('afinidad') or 0)
        except Exception:
            afinidad = 0.0
        try:
            dur = int(float(item.get('duracion')))
            duracion_display = f"{dur} años"
        except Exception:
            duracion_display = _clean_text(item.get('duracion') or '—')
        try:
            mat = float(item.get('costo_matricula') or 0)
            matricula_display = f"S/. {mat:,.0f}"
        except Exception:
            matricula_display = _clean_text(item.get('costo_matricula') or '—')
        try:
            pen = float(item.get('costo_pension') or 0)
            pension_display = f"S/. {pen:,.0f}"
        except Exception:
            pension_display = _clean_text(item.get('costo_pension') or '—')

        with cols[idx]:
            st.caption(area.upper())
            st.subheader(carrera)
            st.markdown(f"**{institucion}**")
            st.write(f"📍 {sede}")
            st.write(f"**{afinidad:.0f}% Match**")
            # metrics as plain text (no HTML)
            st.write(f"Duración: {duracion_display}   •   Matrícula: {matricula_display}   •   Mensualidad: {pension_display}")
            # modalidades shown as simple comma-separated badges/text
            if modalidad:
                st.write(f"Modalidad: {modalidad}")
            if razon:
                st.write(f"Razón: {razon}")
            if razon:
                st.write(f"Razón: {razon}")


def render_header():
    st.markdown(
        """
    <div class="main-title">Orientación Vocacional</div>
    <div class="subtitle">Encuentra las mejores opciones según tu perfil</div>
    """,
        unsafe_allow_html=True,
    )


def render_kpis(kpis: dict):
    cols = st.columns(4)
    labels = [
        ("Opciones", kpis.get("opciones_compatibles", 0)),
        (
            "Mensualidad",
            f"S/. {kpis.get('mensualidad_promedio', 0):,.0f}" if kpis.get("mensualidad_promedio") else "S/. 0",
        ),
        ("Duración (años)", f"{kpis.get('duracion_promedio', 0):.1f}"),
        ("Top modalidad", kpis.get("top_modalidad", "Sin datos")),
    ]
    for c, (label, value) in zip(cols, labels):
        with c:
            st.markdown(
                f"<div class=\"kpi-card\"><div class=\"kpi-label\">{label}</div><div class=\"kpi-value\">{value}</div></div>",
                unsafe_allow_html=True,
            )


def render_charts(bubble_df: pd.DataFrame, modality_df: pd.DataFrame):
    st.markdown("### Visualizaciones")
    if not bubble_df.empty:
        fig = px.scatter(
            bubble_df,
            x="costo_pension",
            y="afinidad",
            size="costo_pension",
            color="tipo_origen" if "tipo_origen" in bubble_df.columns else None,
            hover_data=bubble_df.columns.tolist(),
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay datos para el gráfico de burbuja.")

    if not modality_df.empty:
        st.bar_chart(modality_df.set_index("modalidad")["programas"])
    else:
        st.info("No hay datos por modalidad.")


def render_comparison_table(df: pd.DataFrame):
    st.markdown("### Comparador de programas")

    if df.empty:
        st.info("No hay información comparativa para mostrar.")
        return

    show_df = df.copy()
    show_df.columns = [
        "Carrera",
        "Institución",
        "Sede",
        "Modalidad",
        "Duración (años)",
        "Matrícula",
        "Mensualidad",
        "Afinidad",
        "Razón",
    ]

    st.dataframe(show_df, use_container_width=True, hide_index=True)


def render_footer():
    st.caption("Dashboard profesional de orientación vocacional · Vista dummy con filtros funcionales")
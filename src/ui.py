import html as _html
import re

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


def render_global_css():
    st.markdown(
        """
    <style>
        :root {
            --text-strong: #000000;
            --text-soft: #000000;
            --border-soft: #e5e7eb;
            --panel-bg: #ffffff;
            --panel-alt: #f8fafc;
            --brand-blue: #5b6ee1;
            --brand-green: #27b48a;
            --brand-gold: #d9a63a;
            --brand-violet: #a855f7;
        }

        .stApp {
            background: linear-gradient(180deg, #fbfbfd 0%, #f5f7fb 100%);
        }

        .block-container {
            max-width: 1380px;
            padding-top: 1.8rem;
            padding-bottom: 2rem;
        }

        .main-title {
            font-size: 2.2rem;
            font-weight: 800;
            color: var(--text-strong);
            margin-bottom: 0.15rem;
        }

        .subtitle {
            color: var(--text-soft);
            margin-bottom: 1.3rem;
            font-size: 1rem;
        }

        .kpi-card {
            background: var(--panel-bg);
            border-radius: 20px;
            padding: 22px;
            border: 1px solid var(--border-soft);
            box-shadow: 0 6px 20px rgba(15, 23, 42, 0.05);
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
            color: var(--text-strong);
            line-height: 1.1;
        }

        .kpi-sub {
            color: var(--text-soft);
            margin-top: 8px;
            font-size: 0.92rem;
        }

        .kpi-blue {
            background: #eef2ff;
        }

        .kpi-blue .kpi-label {
            color: var(--brand-blue);
        }

        .kpi-green {
            background: #ecfdf6;
        }

        .kpi-green .kpi-label {
            color: var(--brand-green);
        }

        .kpi-gold {
            background: #fff9e9;
        }

        .kpi-gold .kpi-label {
            color: var(--brand-gold);
        }

        .kpi-violet {
            background: #faf1ff;
        }

        .kpi-violet .kpi-label {
            color: var(--brand-violet);
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

        label,
        .stSelectbox label,
        .stCaption,
        .stMarkdown,
        .stText,
        .stSubheader,
        .stHeader,
        p,
        span,
        div {
            color: var(--text-strong) !important;
        }

        [data-baseweb="select"] * {
            color: var(--text-strong) !important;
        }

        div[data-baseweb="select"] > div {
            border-radius: 14px !important;
            min-height: 44px !important;
            border-color: #dbe3ee !important;
            background: #ffffff !important;
        }

        .stButton button {
            border-radius: 14px !important;
            min-height: 44px !important;
            font-weight: 700 !important;
            border: 1px solid #dbe3ee !important;
            background: white !important;
            color: var(--text-strong) !important;
        }

        .stDataFrame {
            background: white !important;
            border-radius: 18px !important;
        }

        .table-card {
            background: #ffffff;
            border: 1px solid var(--border-soft);
            border-radius: 22px;
            padding: 14px;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
        }

        .career-card {
            background: var(--panel-bg);
            border-radius: 22px;
            padding: 22px;
            border: 1px solid var(--border-soft);
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
            min-height: 100%;
        }

        .career-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 16px 36px rgba(15, 23, 42, 0.1);
        }

        @media (max-width: 900px) {
            .block-container {
                padding-left: 12px !important;
                padding-right: 12px !important;
            }

            .main-title {
                font-size: 1.4rem !important;
            }

            .subtitle {
                font-size: 0.95rem !important;
            }

            .kpi-card {
                padding: 12px !important;
                min-height: 96px !important;
            }

            .kpi-value {
                font-size: 1.4rem !important;
            }
        }

        @media (max-width: 480px) {
            .kpi-card {
                min-height: 80px !important;
            }

            .kpi-value {
                font-size: 1.1rem !important;
            }

            .main-title {
                font-size: 1.1rem !important;
            }
        }
    </style>
    """,
        unsafe_allow_html=True,
    )


def _get_modality_tag_class(modalidad: str) -> str:
    if modalidad == "Presencial":
        return "tag tag-presencial"
    if modalidad == "Virtual":
        return "tag tag-virtual"
    if modalidad == "Semipresencial":
        return "tag tag-semipresencial"
    return "tag"


def render_header():
    st.markdown(
        """
    <div class="main-title">Dashboard de Decisión</div>
    <div class="subtitle">Filtra y compara para elegir la mejor opción según tu presupuesto y tiempo.</div>
    """,
        unsafe_allow_html=True,
    )


def render_kpis(kpis: dict):
    cols = st.columns(4)
    cards = [
        ("Opciones compatibles", kpis.get("opciones_compatibles", 0), "Instituciones según filtros", "kpi-blue"),
        (
            "Mensualidad prom.",
            f"S/. {kpis.get('mensualidad_promedio', 0):,.0f}" if kpis.get("mensualidad_promedio") else "S/. 0",
            "Costo mensual estimado",
            "kpi-green",
        ),
        ("Duración prom.", f"{kpis.get('duracion_promedio', 0):.1f} años", "Tiempo promedio de estudio", "kpi-gold"),
        ("Top modalidad", kpis.get("top_modalidad", "Sin datos"), "Modalidad más frecuente", "kpi-violet"),
    ]

    for col, (label, value, sublabel, card_class) in zip(cols, cards):
        with col:
            st.markdown(
                f"<div class=\"kpi-card {card_class}\"><div class=\"kpi-label\">{label}</div><div class=\"kpi-value\">{value}</div><div class=\"kpi-sub\">{sublabel}</div></div>",
                unsafe_allow_html=True,
            )


def render_charts(bubble_df: pd.DataFrame, modality_df: pd.DataFrame):
    st.markdown("### Visualizaciones")
    chart_col1, chart_col2 = st.columns([2.1, 1.05])

    with chart_col1:
        if not bubble_df.empty:
            color_map = {
                "Pública": "#5b6ee1",
                "Privada": "#27b48a",
                "Instituto": "#27b48a",
                "Universidad": "#8b7cf6",
            }
            fig = px.scatter(
                bubble_df,
                x="duracion" if "duracion" in bubble_df.columns else "costo_pension",
                y="costo_pension",
                size="afinidad" if "afinidad" in bubble_df.columns else "costo_pension",
                color="tipo_origen" if "tipo_origen" in bubble_df.columns else None,
                color_discrete_map=color_map,
                hover_data=bubble_df.columns.tolist(),
            )
            fig.update_traces(
                marker=dict(line=dict(color="#ffffff", width=1.5), opacity=0.8),
            )
            fig.update_layout(
                title="Inversión vs. Tiempo de Estudio",
                paper_bgcolor="#ffffff",
                plot_bgcolor="#ffffff",
                font=dict(color="#1f2937", size=13),
                margin=dict(l=20, r=20, t=60, b=20),
                legend=dict(
                    title="Tipo",
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="left",
                    x=0,
                    font=dict(color="#1f2937"),
                    title_font=dict(color="#1f2937"),
                ),
                xaxis=dict(
                    title="Duración (años)" if "duracion" in bubble_df.columns else "Costo de pensión",
                    gridcolor="#e5e7eb",
                    zeroline=False,
                    tickfont=dict(color="#1f2937"),
                    title_font=dict(color="#1f2937"),
                ),
                yaxis=dict(
                    title="Mensualidad (S/.)",
                    gridcolor="#e5e7eb",
                    zeroline=False,
                    tickfont=dict(color="#1f2937"),
                    title_font=dict(color="#1f2937"),
                ),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos para el gráfico de burbuja.")

    with chart_col2:
        if not modality_df.empty:
            donut_colors = ["#4285f4", "#a855f7", "#27b48a", "#f59e0b", "#0ea5e9"]
            total_programas = int(modality_df["programas"].sum())
            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=modality_df["modalidad"],
                        values=modality_df["programas"],
                        hole=0.68,
                        textinfo="none",
                        domain=dict(x=[0.0, 0.68], y=[0.0, 1.0]),
                        marker=dict(
                            colors=donut_colors[: len(modality_df)],
                            line=dict(color="#ffffff", width=2),
                        ),
                    )
                ]
            )
            fig.add_annotation(
                text=f"<b>{total_programas}</b><br><span style='font-size:12px;color:#6b7280'>Programas</span>",
                x=0.5,
                y=0.5,
                showarrow=False,
                font=dict(color="#1f2937", size=18),
            )
            fig.update_layout(
                title="Oferta por Modalidad",
                paper_bgcolor="#ffffff",
                plot_bgcolor="#ffffff",
                font=dict(color="#1f2937", size=13),
                margin=dict(l=20, r=20, t=60, b=20),
                legend=dict(
                    title="Modalidad",
                    orientation="v",
                    yanchor="middle",
                    y=0.5,
                    xanchor="left",
                    x=0.75,
                    font=dict(color="#1f2937"),
                    title_font=dict(color="#1f2937"),
                ),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No hay datos por modalidad.")


def render_top3(top3):
    st.header("Tu Top 3 Personalizado")

    if not top3:
        st.info("No hay recomendaciones para los filtros seleccionados.")
        return

    cols = st.columns(3)

    def _clean_text(value):
        if value is None:
            return ""
        if not isinstance(value, str):
            return str(value)
        text = _html.unescape(value)
        text = re.sub(r"(?is)<(script|style).*?>.*?</\1>", "", text)
        text = re.sub(r"<[^>]+>", "", text)
        text = _html.unescape(text)
        text = text.replace("\n", " ").replace("\r", " ")
        text = re.sub(r"\s+", " ", text).strip()
        if len(text) > 280:
            return text[:240].rstrip() + "..."
        return text

    for idx, raw_item in enumerate(top3[:3]):
        item = {k: raw_item.get(k) for k in raw_item.keys()}
        area = _clean_text(item.get("area"))
        carrera = _clean_text(item.get("carrera"))
        institucion = _clean_text(item.get("institucion"))
        sede = _clean_text(item.get("sede") or "Sin sede")
        razon = _clean_text(item.get("razon") or "")
        modalidad = _clean_text(item.get("modalidad") or "")

        try:
            afinidad = float(item.get("afinidad") or 0)
        except Exception:
            afinidad = 0.0

        try:
            dur = int(float(item.get("duracion")))
            duracion_display = f"{dur} años"
        except Exception:
            duracion_display = _clean_text(item.get("duracion") or "-")

        try:
            mat = float(item.get("costo_matricula") or 0)
            matricula_display = f"S/. {mat:,.0f}"
        except Exception:
            matricula_display = _clean_text(item.get("costo_matricula") or "-")

        try:
            pen = float(item.get("costo_pension") or 0)
            pension_display = f"S/. {pen:,.0f}"
        except Exception:
            pension_display = _clean_text(item.get("costo_pension") or "-")

        with cols[idx]:
            st.markdown('<div class="career-card">', unsafe_allow_html=True)
            st.caption(area.upper())
            st.subheader(carrera)
            st.markdown(f"**{institucion}**")
            st.write(f"Sede: {sede}")
            st.write(f"**{afinidad:.0f}% de afinidad**")
            st.write(f"Duración: {duracion_display}   •   Matrícula: {matricula_display}   •   Mensualidad: {pension_display}")
            if modalidad:
                st.write(f"Modalidad: {modalidad}")
            if razon:
                st.write(f"Razón: {razon}")
            st.markdown("</div>", unsafe_allow_html=True)


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

    st.markdown('<div class="table-card">', unsafe_allow_html=True)
    st.dataframe(show_df, use_container_width=True, hide_index=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render_footer():
    st.caption("Dashboard profesional de orientación vocacional")

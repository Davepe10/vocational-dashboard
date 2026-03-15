import streamlit as st
import plotly.express as px
import pandas as pd
import html as _html


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
            color: #64748b;
            font-size: 0.93rem;
        }

        .metric-box {
            background: #f8fafc;
            border-radius: 16px;
            padding: 14px;
            margin-top: 14px;
            border: 1px solid #eef2f7;
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
        }

        .stDataFrame {
            background: white !important;
            border-radius: 18px !important;
        }
    </style>
    """, unsafe_allow_html=True)


def render_header():
    st.markdown('<div class="main-title">📊 Dashboard de Decisión</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle">Filtra y compara para elegir la mejor opción según tu presupuesto, tiempo y afinidad vocacional.</div>',
        unsafe_allow_html=True
    )


def render_kpis(kpis: dict):
    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label" style="color:#6366F1;">Opciones compatibles</div>
            <div class="kpi-value">{kpis["opciones_compatibles"]}</div>
            <div class="kpi-sub">Programas compatibles</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label" style="color:#10B981;">Mensualidad prom.</div>
            <div class="kpi-value">S/. {kpis["mensualidad_promedio"]:,.0f}</div>
            <div class="kpi-sub">Rango: {kpis["rango_presupuesto"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label" style="color:#F59E0B;">Duración prom.</div>
            <div class="kpi-value">{kpis["duracion_promedio"]:.1f} años</div>
            <div class="kpi-sub">Entre instituciones y universidades</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label" style="color:#A855F7;">Top modalidad</div>
            <div class="kpi-value" style="font-size:1.6rem;">{kpis["top_modalidad"]}</div>
            <div class="kpi-sub">La modalidad más frecuente</div>
        </div>
        """, unsafe_allow_html=True)


def render_charts(bubble_df: pd.DataFrame, modality_df: pd.DataFrame):
    col1, col2 = st.columns([2.1, 1])

    with col1:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Inversión vs. Tiempo de Estudio</div>', unsafe_allow_html=True)

        if bubble_df.empty:
            st.info("No hay datos para el gráfico principal.")
        else:
            fig = px.scatter(
                bubble_df,
                x="duracion",
                y="costo_pension",
                size="afinidad",
                color="tipo_origen",
                hover_name="carrera",
                hover_data={
                    "institucion": True,
                    "duracion": True,
                    "costo_pension": ":.0f",
                    "afinidad": ":.0f",
                },
                size_max=42,
            )
            fig.update_layout(
                height=430,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="white",
                plot_bgcolor="white",
                legend_title_text="Tipo institución",
            )
            fig.update_xaxes(title_text="Duración (Años)", gridcolor="#e5e7eb")
            fig.update_yaxes(title_text="Mensualidad (S/.)", gridcolor="#e5e7eb")
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-card">', unsafe_allow_html=True)
        st.markdown('<div class="section-title">Oferta por Modalidad</div>', unsafe_allow_html=True)

        if modality_df.empty:
            st.info("No hay datos para el gráfico de modalidad.")
        else:
            fig2 = px.pie(
                modality_df,
                values="programas",
                names="modalidad",
                hole=0.65,
            )
            fig2.update_layout(
                height=430,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="white",
                showlegend=True,
            )
            st.plotly_chart(fig2, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)


def _get_modality_tag_class(modalidad: str) -> str:
    if modalidad == "Presencial":
        return "tag tag-presencial"
    if modalidad == "Virtual":
        return "tag tag-virtual"
    if modalidad == "Semipresencial":
        return "tag tag-semipresencial"
    return "tag"


def render_top3(top3: list[dict]):
    st.markdown('<div class="top3-title">🏆 Tu Top 3 Personalizado</div>', unsafe_allow_html=True)

    if not top3:
        st.info("No hay recomendaciones para los filtros seleccionados.")
        return

    cols = st.columns(3)
    for idx, item in enumerate(top3[:3]):
        modalidad_val = (item.get("modalidad") or "Sin modalidad")
        tag_class = _get_modality_tag_class(modalidad_val)
        afinidad_val = float(item.get("afinidad") or 0)
        duracion_val = item.get("duracion") if item.get("duracion") is not None else "—"
        costo_matricula_val = float(item.get("costo_matricula") or 0)
        costo_pension_val = float(item.get("costo_pension") or 0)
        # escape any HTML coming from DB to avoid injecting markup into the card
        area_val = _html.escape(str(item.get("area") or ""))
        carrera_val = _html.escape(str(item.get("carrera") or ""))
        institucion_val = _html.escape(str(item.get("institucion") or ""))
        sede_val = _html.escape(str(item.get("sede") or "Sin sede"))
        razon_val = _html.escape(str(item.get("razon") or ""))

        with cols[idx]:
            st.markdown(f"""
            <div class="career-card">
                <div class="badge-match">{afinidad_val:.0f}% Match</div>
                <div class="muted" style="margin-top:8px;font-weight:700;text-transform:uppercase;">{area_val}</div>
                <div style="font-size:2rem;font-weight:800;color:#0f172a;margin-top:10px;">{carrera_val}</div>
                <div style="font-size:1rem;font-weight:700;color:#6366F1;margin-top:4px;">{institucion_val}</div>
                <div class="muted" style="margin-top:6px;">📍 {sede_val}</div>

                <div class="metric-box">
                    <div class="muted">⏱ Duración</div>
                    <div style="font-weight:800;">{duracion_val} años</div>
                    <div class="muted" style="margin-top:8px;">🧾 Matrícula</div>
                    <div style="margin-top:8px;">💸 Mensualidad</div>
                    <div style="font-weight:800;">S/. {costo_matricula_val:,.2f}</div>
                </div>

                <div style="margin-top:12px;">
                    <span class="{tag_class}">{modalidad_val}</span>
                </div>

                <div class="muted" style="margin-top:14px;"><b>Razón:</b> {razon_val}</div>
            </div>
            """, unsafe_allow_html=True)


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
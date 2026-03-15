import re
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
            .metric-box { padding: 10px !important; }
            .tag { padding: 5px 8px !important; font-size: 0.72rem !important; }
            .career-card { margin-bottom: 14px !important; }
            .stButton button { min-height: 40px !important; }
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
                font=dict(color="#0f172a"),
            )
            fig.update_xaxes(title_text="Duración (Años)", gridcolor="#e5e7eb", tickfont=dict(color="#0f172a"), title_font=dict(color="#0b2545"))
            fig.update_yaxes(title_text="Mensualidad (S/.)", gridcolor="#e5e7eb", tickfont=dict(color="#0f172a"), title_font=dict(color="#0b2545"))
            fig.update_traces(marker=dict(opacity=0.85, line=dict(width=1, color="#ffffff")), selector=dict(mode="markers"))
            fig.update_traces(hoverlabel=dict(bgcolor="#fff", font=dict(color="#0f172a")))
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
                color_discrete_sequence=["#2563eb", "#a855f7", "#10B981"],
            )
            fig2.update_traces(textinfo='none')
            fig2.update_layout(
                height=430,
                margin=dict(l=10, r=10, t=10, b=10),
                paper_bgcolor="white",
                showlegend=True,
                legend=dict(font=dict(color="#0f172a")),
                annotations=[dict(text=f"{int(modality_df['programas'].sum())}<br>Programas", x=0.5, y=0.5, font_size=16, showarrow=False, font_color="#0f172a")],
            )
            fig2.update_traces(marker=dict(line=dict(color="#ffffff", width=1)))
            # ensure pie is centered and uses most of the card area
            fig2.update_traces(domain=dict(x=[0.15, 0.85], y=[0.15, 0.85]))
            fig2.update_layout(legend=dict(orientation='v', x=1.02, xanchor='left'))
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
    def _strip_tags(s: str) -> str:
        if s is None:
            return ""
        if not isinstance(s, str):
            return str(s)
        txt = _html.unescape(s)
        txt = re.sub(r"<[^>]+>", "", txt)
        # collapse long HTML remnants
        if len(txt) > 300:
            return txt[:240].rstrip() + "..."
        return txt

    def _clean_value(v):
        # ensure string values don't contain any HTML-like fragments
        if v is None:
            return ""
        if isinstance(v, str):
            t = _html.unescape(v)
            # remove tags and angle brackets aggressively
            t = re.sub(r"<[^>]*>", "", t)
            t = t.replace("&lt;", "").replace("&gt;", "")
            # remove leftover HTML attribute patterns
            t = re.sub(r"\w+\s*=\s*\"[^"]*\"", "", t)
            # collapse whitespace
            t = re.sub(r"\s+", " ", t).strip()
            if len(t) > 280:
                return t[:240].rstrip() + "..."
            return t
        return str(v)

    for idx, raw_item in enumerate(top3[:3]):
        # prefer numeric-safe values; build metric box from numbers only (ignore any HTML blobs)
        item = {k: raw_item.get(k) for k in raw_item.keys()}
        modalidad_raw = item.get("modalidad") or "Sin modalidad"
        # modalidad may be comma-separated; render individual tags
        modalidades = [m.strip() for m in str(modalidad_raw).split(",") if m.strip()]
        # numeric-safe parsing
        try:
            afinidad_val = float(item.get("afinidad") or 0)
        except Exception:
            afinidad_val = 0.0
        # duracion may be numeric or textual; prefer numeric
        try:
            duracion_val = int(float(item.get("duracion")))
            duracion_display = f"{duracion_val} años"
        except Exception:
            duracion_display = _clean_value(item.get("duracion") or "—")

        try:
            costo_matricula_val = float(item.get("costo_matricula") or 0)
            costo_matricula_display = f"S/. {costo_matricula_val:,.0f}"
        except Exception:
            costo_matricula_display = _clean_value(item.get("costo_matricula") or "—")

        try:
            costo_pension_val = float(item.get("costo_pension") or 0)
            costo_pension_display = f"S/. {costo_pension_val:,.0f}"
        except Exception:
            costo_pension_display = _clean_value(item.get("costo_pension") or "—")

        area_val = _clean_value(item.get("area") or "")
        carrera_val = _clean_value(item.get("carrera") or "")
        institucion_val = _clean_value(item.get("institucion") or "")
        sede_val = _clean_value(item.get("sede") or "Sin sede")
        razon_val = _clean_value(item.get("razon") or "")

        with cols[idx]:
            # build HTML for card using sanitized values
            tags_html = "".join([f'<span class="{_get_modality_tag_class(m)}" style="margin-right:6px">{_html.escape(m)}</span>' for m in modalidades])
            st.markdown(f"""
            <div class="career-card">
                <div class="badge-match">{afinidad_val:.0f}% Match</div>
                <div class="muted" style="margin-top:8px;font-weight:700;text-transform:uppercase;">{area_val}</div>
                <div class="title" style="font-size:1.4rem;margin-top:8px;">{carrera_val}</div>
                <div class="institution" style="margin-top:6px;">{institucion_val}</div>
                <div class="sede" style="margin-top:6px;">📍 {sede_val}</div>

                <div class="metric-box">
                    <div style="display:flex;justify-content:space-between;align-items:center">
                        <div>
                            <div class="metric-label">⏱ Duración</div>
                            <div class="metric-value">{duracion_display}</div>
                        </div>
                        <div style="text-align:right">
                            <div class="metric-label">🧾 Matrícula</div>
                            <div class="metric-value">{costo_matricula_display}</div>
                            <div style="height:6px"></div>
                            <div class="metric-label">💸 Mensualidad</div>
                            <div class="metric-value">{costo_pension_display}</div>
                        </div>
                    </div>
                </div>

                <div style="margin-top:12px;">{tags_html}</div>

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
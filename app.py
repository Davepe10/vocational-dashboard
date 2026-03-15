import streamlit as st
from src.config import get_settings
from src.logging_config import setup_logging
from src.db import get_engine
from src.repository import DashboardRepository
from src.service import DashboardService
from src.ui import render_global_css, render_header, render_kpis, render_charts, render_top3, render_comparison_table, render_footer
from src.utils import safe_int

setup_logging()
settings = get_settings()

st.set_page_config(
    page_title="Dashboard de Decisión Vocacional",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed",
)

render_global_css()

@st.cache_resource
def build_service():
    engine = get_engine(settings)
    repo = DashboardRepository(engine)
    return DashboardService(repo)

service = build_service()

# Load filter options
try:
    filter_options = service.get_filter_options()
except Exception as e:
    st.error("No se pudieron cargar los filtros iniciales. Revisa logs y conexión a la base.")
    st.exception(e)
    st.stop()

# Read URL params to allow pre-filtering by user (e.g. ?user_id=25)
query_params = st.query_params
url_user = None
if "user_id" in query_params:
    try:
        url_user = int(query_params.get("user_id")[0])
    except Exception:
        url_user = None

# prepare user options and default before creating widgets
# filter_options["usuarios"] is a list of dicts: {"id": int, "label": str}
user_map = {u["id"]: u["label"] for u in filter_options.get("usuarios", [])}
user_ids = [u["id"] for u in filter_options.get("usuarios", [])]
user_options = ["Todos"] + [str(x) for x in user_ids]
default_user = "Todos"
if url_user is not None and url_user in user_ids:
    default_user = str(url_user)

# fetch role for url_user (if present) to allow admin viewing
url_user_role = None
if url_user is not None:
    try:
        url_user_role = service.repo.get_user_role(url_user)
    except Exception:
        url_user_role = None

render_header()

# If URL contains user_id, show notice and role
if url_user is not None:
    role_label = url_user_role or "(rol desconocido)"
    st.info(f"Vista filtrada por usuario {url_user} — rol: {role_label}")
    if str(url_user_role).lower() != "admin":
        st.warning("Usuario no administrador: sólo verás tus datos. Para ver otros usuarios necesita un rol admin.")

col_f1, col_f2, col_f3, col_f4, col_f5, col_f6 = st.columns([1, 1, 1, 1, 1, 1])

with col_f1:
    user_options = ["Todos"] + [str(x) for x in user_ids]
    default_user = default_user

    # initialize session state for filters so we can reset them when requested
    if "filter_usuario" not in st.session_state:
        st.session_state["filter_usuario"] = default_user

    # If url_user is present and the role is not admin, lock the selector to that user
    disable_user = False
    if url_user is not None and (url_user_role is None or (str(url_user_role).lower() != "admin")):
        disable_user = True

    # display labels (email) while options remain the id strings
    def _user_format(x):
        return "Todos" if x == "Todos" else user_map.get(int(x), str(x))

    selected_user = st.selectbox(
        "Usuario",
        options=user_options,
        key="filter_usuario",
        format_func=_user_format,
        disabled=disable_user,
    )

with col_f2:
    attempts_options = ["Todos"] + filter_options["intentos"]
    if "filter_intento" not in st.session_state:
        st.session_state["filter_intento"] = "Todos"
    def _format_intento(opt):
        return "Todos" if opt == "Todos" else f"Intento {opt}"
    selected_attempt = st.selectbox("Intento", options=attempts_options, key="filter_intento", format_func=_format_intento)

with col_f3:
    modality_options = ["Todas"] + filter_options["modalidades"]
    if "filter_modalidad" not in st.session_state:
        st.session_state["filter_modalidad"] = "Todas"
    selected_modality = st.selectbox("Modalidad", options=modality_options, key="filter_modalidad")

with col_f4:
    if "filter_budget" not in st.session_state:
        st.session_state["filter_budget"] = filter_options["budget_options"][min(4, len(filter_options["budget_options"]) - 1) if filter_options["budget_options"] else 0]
    max_budget = st.selectbox("Presupuesto Máx.", options=filter_options["budget_options"], key="filter_budget")

with col_f5:
    duration_options = ["Todas"] + filter_options["duraciones"]
    if "filter_duration" not in st.session_state:
        st.session_state["filter_duration"] = "Todas"
    def _format_duration(opt):
        return "Todas" if opt == "Todas" else f"Hasta {opt} años"
    max_duration = st.selectbox("Duración Máx. (años)", options=duration_options, key="filter_duration", format_func=_format_duration)

with col_f6:
    institution_options = ["Todas"] + filter_options["instituciones"]
    if "filter_institution" not in st.session_state:
        st.session_state["filter_institution"] = "Todas"
    selected_institution = st.selectbox("Institución", options=institution_options, key="filter_institution")

col_f7, col_f8 = st.columns([1, 1])

with col_f7:
    career_options = ["Todas"] + filter_options["carreras"]
    if "filter_career" not in st.session_state:
        st.session_state["filter_career"] = "Todas"
    selected_career = st.selectbox("Carrera", options=career_options, key="filter_career")

def _clear_filters_callback(default_user_val: str, url_locked: bool):
    # clear URL params
    try:
        st.experimental_set_query_params()
    except Exception:
        # if setting query params is unavailable, ignore
        pass
    # Reset session_state keys; if a user is locked by URL keep it
    if "filter_usuario" in st.session_state:
        st.session_state["filter_usuario"] = default_user_val if url_locked else "Todos"
    for k, v in {
        "filter_intento": "Todos",
        "filter_modalidad": "Todas",
        "filter_budget": filter_options["budget_options"][min(4, len(filter_options["budget_options"]) - 1) if filter_options["budget_options"] else 0],
        "filter_duration": "Todas",
        "filter_institution": "Todas",
        "filter_career": "Todas",
    }.items():
        st.session_state[k] = v
    # mark for a safe rerun after widgets are created (avoid calling rerun from inside callbacks)
    st.session_state["_clear_filters_pending"] = True

with col_f8:
    st.button("Limpiar filtros", use_container_width=True, on_click=_clear_filters_callback, args=(default_user, disable_user))

# If a clear-filters action was requested in the callback, clear the flag.
# Streamlit will rerun after the callback returns, so an explicit rerun is unnecessary
if st.session_state.get("_clear_filters_pending"):
    st.session_state["_clear_filters_pending"] = False

filters = {
    "usuario_id": None if st.session_state["filter_usuario"] == "Todos" else safe_int(st.session_state["filter_usuario"]),
    "num_intento": None if st.session_state["filter_intento"] == "Todos" else safe_int(st.session_state["filter_intento"]),
    "modalidad": None if st.session_state["filter_modalidad"] == "Todas" else st.session_state["filter_modalidad"],
    "max_presupuesto": None if st.session_state["filter_budget"] == "Todas" else safe_int(str(st.session_state["filter_budget"]).replace("S/.", "").replace("S/", "").replace(",", "").strip()),
    "max_duracion": None if st.session_state["filter_duration"] == "Todas" else safe_int(st.session_state["filter_duration"]),
    "carrera": None if st.session_state["filter_career"] == "Todas" else st.session_state["filter_career"],
    "institucion": None if st.session_state["filter_institution"] == "Todas" else st.session_state["filter_institution"],
}

try:
    dataset = service.get_dashboard_data(filters)
except Exception as e:
    st.error("Error consultando la base de datos. Verifica variables, firewall y SSL.")
    st.exception(e)
    st.stop()

render_kpis(dataset["kpis"])
render_charts(dataset["bubble_df"], dataset["modality_df"])
render_top3(dataset["top3"])
render_comparison_table(dataset["comparison_df"])
render_footer()
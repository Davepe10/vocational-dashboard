import streamlit as st

from src.config import get_settings
from src.db import get_engine
from src.logging_config import setup_logging
from src.repository import DashboardRepository
from src.service import DashboardService
from src.ui import (
    render_charts,
    render_comparison_table,
    render_footer,
    render_global_css,
    render_header,
    render_kpis,
    render_top3,
)
from src.utils import safe_int

setup_logging()
settings = get_settings()

st.set_page_config(
    page_title="Dashboard de Decision Vocacional",
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

try:
    filter_options = service.get_filter_options()
except Exception as e:
    st.error("No se pudieron cargar los filtros iniciales. Revisa logs y conexion a la base.")
    st.exception(e)
    st.stop()


def _read_url_user_id():
    query_params = st.query_params
    if "user_id" not in query_params:
        return None

    try:
        raw_user_id = query_params.get("user_id")
        if isinstance(raw_user_id, list):
            raw_user_id = raw_user_id[0] if raw_user_id else None
        return int(raw_user_id) if raw_user_id is not None else None
    except Exception:
        return None


url_user = _read_url_user_id()

user_map = {u["id"]: u["label"] for u in filter_options.get("usuarios", [])}
user_ids = [u["id"] for u in filter_options.get("usuarios", [])]
user_options = ["Todos"] + [str(x) for x in user_ids]

default_user = "Todos"
if url_user is not None and url_user in user_ids:
    default_user = str(url_user)

url_user_info = None
url_user_role = None
active_user_label = None
if url_user is not None:
    try:
        url_user_info = service.repo.get_user_info(url_user)
    except Exception:
        url_user_info = None

    if url_user_info is None:
        st.error(f"No existe un usuario con id {url_user}.")
        st.stop()

    url_user_role = url_user_info.get("rol")
    active_user_label = str(url_user_info.get("email") or f"Usuario {url_user}")
    if url_user not in user_ids:
        user_map[url_user] = active_user_label
        user_ids.append(url_user)
        user_ids.sort()
        user_options = ["Todos"] + [str(x) for x in user_ids]
        default_user = str(url_user)


def _display_name(label: str) -> str:
    base = (label or "").strip()
    if "@" in base:
        base = base.split("@", 1)[0]
    base = base.replace(".", " ").replace("_", " ").replace("-", " ").strip()
    return " ".join(part.capitalize() for part in base.split()) or "Usuario"

render_header()

if url_user is not None:
    greeting_name = _display_name(active_user_label)
    role_label = url_user_role or "(rol desconocido)"
    st.info(f"Vista filtrada por usuario {url_user} - rol: {role_label}")
    if str(url_user_role).lower() == "admin":
        st.markdown(f"**Hola Admin, {greeting_name}**")
    else:
        st.markdown(f"**Hola, {greeting_name}**")
    if active_user_label:
        st.caption(f"Sesion: {active_user_label}")
    if str(url_user_role).lower() != "admin":
        st.warning("Usuario no administrador: solo veras tus datos. Para ver otros usuarios necesita un rol admin.")

col_f1, col_f2, col_f3, col_f4, col_f5, col_f6 = st.columns([1, 1, 1, 1, 1, 1])

with col_f1:
    if "filter_usuario" not in st.session_state:
        st.session_state["filter_usuario"] = default_user
    elif url_user is not None and str(url_user) in user_options and st.session_state.get("_last_url_user") != url_user:
        st.session_state["filter_usuario"] = str(url_user)

    st.session_state["_last_url_user"] = url_user

    disable_user = False
    if url_user is not None and (url_user_role is None or str(url_user_role).lower() != "admin"):
        disable_user = True

    def _user_format(x):
        return "Todos" if x == "Todos" else user_map.get(int(x), str(x))

    st.selectbox(
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

    st.selectbox("Intento", options=attempts_options, key="filter_intento", format_func=_format_intento)

with col_f3:
    modality_options = ["Todas"] + filter_options["modalidades"]
    if "filter_modalidad" not in st.session_state:
        st.session_state["filter_modalidad"] = "Todas"
    st.selectbox("Modalidad", options=modality_options, key="filter_modalidad")

with col_f4:
    if "filter_budget" not in st.session_state:
        st.session_state["filter_budget"] = filter_options["budget_options"][
            min(4, len(filter_options["budget_options"]) - 1) if filter_options["budget_options"] else 0
        ]
    st.selectbox("Presupuesto Max.", options=filter_options["budget_options"], key="filter_budget")

with col_f5:
    duration_options = ["Todas"] + filter_options["duraciones"]
    if "filter_duration" not in st.session_state:
        st.session_state["filter_duration"] = "Todas"

    def _format_duration(opt):
        return "Todas" if opt == "Todas" else f"Hasta {opt} anos"

    st.selectbox("Duracion Max. (anos)", options=duration_options, key="filter_duration", format_func=_format_duration)

with col_f6:
    institution_options = ["Todas"] + filter_options["instituciones"]
    if "filter_institution" not in st.session_state:
        st.session_state["filter_institution"] = "Todas"
    st.selectbox("Institucion", options=institution_options, key="filter_institution")

col_f7, col_f8 = st.columns([1, 1])

with col_f7:
    career_options = ["Todas"] + filter_options["carreras"]
    if "filter_career" not in st.session_state:
        st.session_state["filter_career"] = "Todas"
    st.selectbox("Carrera", options=career_options, key="filter_career")


def _clear_filters_callback(default_user_val: str, url_locked: bool):
    try:
        st.query_params = {}
    except Exception:
        pass

    if "filter_usuario" in st.session_state:
        st.session_state["filter_usuario"] = default_user_val if url_locked else "Todos"

    for key, value in {
        "filter_intento": "Todos",
        "filter_modalidad": "Todas",
        "filter_budget": filter_options["budget_options"][
            min(4, len(filter_options["budget_options"]) - 1) if filter_options["budget_options"] else 0
        ],
        "filter_duration": "Todas",
        "filter_institution": "Todas",
        "filter_career": "Todas",
    }.items():
        st.session_state[key] = value

    st.session_state["_clear_filters_pending"] = True


with col_f8:
    st.button("Limpiar filtros", use_container_width=True, on_click=_clear_filters_callback, args=(default_user, disable_user))

if st.session_state.get("_clear_filters_pending"):
    st.session_state["_clear_filters_pending"] = False

effective_user_filter = url_user if url_user is not None else (
    None if st.session_state["filter_usuario"] == "Todos" else safe_int(st.session_state["filter_usuario"])
)

filters = {
    "usuario_id": effective_user_filter,
    "num_intento": None if st.session_state["filter_intento"] == "Todos" else safe_int(st.session_state["filter_intento"]),
    "modalidad": None if st.session_state["filter_modalidad"] == "Todas" else st.session_state["filter_modalidad"],
    "max_presupuesto": None
    if st.session_state["filter_budget"] == "Todas"
    else safe_int(str(st.session_state["filter_budget"]).replace("S/.", "").replace("S/", "").replace(",", "").strip()),
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

if url_user is not None and dataset["comparison_df"].empty:
    st.warning(f"El usuario {url_user} existe, pero no tiene datos para mostrar con los filtros actuales.")

render_kpis(dataset["kpis"])
render_charts(dataset["bubble_df"], dataset["modality_df"])
render_top3(dataset["top3"])
render_comparison_table(dataset["comparison_df"])
render_footer()

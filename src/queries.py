BASE_FROM_SQL = """
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
-- Join a single sede per institucion to avoid duplicate rows when an institution has multiple sedes
LEFT JOIN (
  SELECT sd.id_institucion,
       sd.idSede,
       sd.nombre,
       sd.direccion,
       sd.latitud,
       sd.longitud
  FROM sede sd
  JOIN (
    SELECT id_institucion, MIN(idSede) AS idSede
    FROM sede
    -- removed WHERE estado = 1 to be tolerant with schemas that lack 'estado'
    GROUP BY id_institucion
  ) smin ON sd.id_institucion = smin.id_institucion AND sd.idSede = smin.idSede
) s
  ON s.id_institucion = i.idInstitucion
WHERE 1 = 1
  -- Note: removed strict `estado = 1` filters because some tables may not have `estado` column in target DB
"""

FILTER_OPTIONS_SQL = f"""
SELECT DISTINCT u.idUsuario AS value
{BASE_FROM_SQL}
ORDER BY u.idUsuario;
"""

ATTEMPTS_SQL = f"""
SELECT DISTINCT it.numeroIntento AS value
{BASE_FROM_SQL}
ORDER BY it.numeroIntento;
"""

MODALITIES_SQL = f"""
SELECT DISTINCT oc.modalidad AS value
{BASE_FROM_SQL}
  AND oc.modalidad IS NOT NULL
  AND oc.modalidad <> ''
ORDER BY oc.modalidad;
"""

DURATIONS_SQL = f"""
SELECT DISTINCT oc.duracion AS value
{BASE_FROM_SQL}
  AND oc.duracion IS NOT NULL
ORDER BY oc.duracion;
"""

CAREERS_SQL = f"""
SELECT DISTINCT c.nombre AS value
{BASE_FROM_SQL}
  AND c.nombre IS NOT NULL
  AND c.nombre <> ''
ORDER BY c.nombre;
"""

INSTITUTIONS_SQL = f"""
SELECT DISTINCT i.nombre AS value
{BASE_FROM_SQL}
  AND i.nombre IS NOT NULL
  AND i.nombre <> ''
ORDER BY i.nombre;
"""

BASE_DATA_SQL = f"""
SELECT
    u.idUsuario AS id_usuario,
    u.email AS email_usuario,
    u.rol AS rol_usuario,

    it.idIntento AS id_intento,
    it.numeroIntento AS num_intento,
    it.fecha AS fecha_intento,

    r.idRecomendacion AS id_recomendacion,

    rc.idRecCarrera AS id_rec_carrera,
    rc.afinidad AS afinidad,

    c.idCarrera AS id_carrera,
    c.nombre AS carrera,
    c.area AS area,

    oc.idOferta AS id_oferta,
    oc.costoPension AS costo_pension,
    oc.duracion AS duracion,
    oc.modalidad AS modalidad,

    i.idInstitucion AS id_institucion,
    i.nombre AS institucion,

    s.idSede AS id_sede,
    s.nombre AS sede,
    s.direccion AS direccion,
    s.latitud AS latitud,
    s.longitud AS longitud
{BASE_FROM_SQL}
  AND (:usuario_id IS NULL OR u.idUsuario = :usuario_id)
  AND (:num_intento IS NULL OR it.numeroIntento = :num_intento)
  AND (:modalidad IS NULL OR oc.modalidad = :modalidad)
  AND (:max_presupuesto IS NULL OR oc.costoPension <= :max_presupuesto)
  AND (:max_duracion IS NULL OR oc.duracion <= :max_duracion)
  AND (:carrera IS NULL OR c.nombre = :carrera)
  AND (:institucion IS NULL OR i.nombre = :institucion);
"""

TOP3_SQL = f"""
SELECT
    c.area AS area,
    c.nombre AS carrera,
    i.nombre AS institucion,
    COALESCE(s.nombre, 'Sin sede') AS sede,
    oc.modalidad AS modalidad,
    oc.duracion AS duracion,
    oc.costoMatricula AS costo_matricula,
    oc.costoPension AS costo_pension,
    rc.afinidad AS afinidad
{BASE_FROM_SQL}
  AND (:usuario_id IS NULL OR u.idUsuario = :usuario_id)
  AND (:num_intento IS NULL OR it.numeroIntento = :num_intento)
  AND (:modalidad IS NULL OR oc.modalidad = :modalidad)
  AND (:max_presupuesto IS NULL OR oc.costoPension <= :max_presupuesto)
  AND (:max_duracion IS NULL OR oc.duracion <= :max_duracion)
  AND (:carrera IS NULL OR c.nombre = :carrera)
  AND (:institucion IS NULL OR i.nombre = :institucion)
ORDER BY rc.afinidad DESC, oc.costoPension ASC
LIMIT 3;
"""

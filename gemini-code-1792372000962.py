import streamlit as st
import datetime
import os
import csv

# Configuración de la página
st.set_page_config(
    page_title="Equipo 1 - Comando y Venta Táctica",
    page_icon="🛡️",
    layout="wide"
)

# Estilo visual táctico / militar moderno
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: #ffffff; }
    .agent-card {
        background-color: #1a1f2c;
        border: 1px solid #2d3748;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .alert-card {
        background-color: #3b1414;
        border: 1px solid #742a2a;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
    }
    .metric-card {
        background-color: #1f293d;
        border: 1px solid #3b82f6;
        padding: 15px;
        border-radius: 8px;
        text-align: center;
    }
    </style>
""", unsafe_allow_html=True)

# Archivos CSV centrales para almacenamiento estructurado
ARCHIVO_INVENTARIO = "inventario_equipo1.csv"
ARCHIVO_VENTAS = "ventas_equipo1.csv"

def inicializar_archivos():
    if not os.path.exists(ARCHIVO_INVENTARIO):
        with open(ARCHIVO_INVENTARIO, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                "SKU", "Producto", "Categoria", "Stock Actual", 
                "Stock Minimo", "Costo Unitario", "PVP Sugerido", "Estado Stock"
            ])
            writer.writerow(["CHAL-001", "Chaleco Modular Multipropósito NIJ IIIA", "Protección Balística", "4", "5", "35000", "49000", "ALERTA STOCK BAJO"])
            writer.writerow(["BOT-002", "Bota Táctica Waterproof High-Grip", "Calzado", "15", "4", "28000", "39200", "OK"])
            writer.writerow(["CAS-003", "Casco Balístico FAST NIJ IIIA", "Protección Balística", "6", "2", "65000", "91000", "OK"])

    if not os.path.exists(ARCHIVO_VENTAS):
        with open(ARCHIVO_VENTAS, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(["ID_Venta", "Fecha", "SKU", "Producto", "Cantidad", "Costo_Total", "Total_Venta", "Ganancia", "Segmento"])

inicializar_archivos()

# --- PANEL DE CONTROL LATERAL (INTERFAZ DUAL) ---
st.sidebar.title("🛡️ EQUIPO 1: Acceso")
modo_operacion = st.sidebar.selectbox("Seleccionar Interfaz:", [
    "👑 Comandante Maestro (War Room & IA)", 
    "🛒 Vendedor de Campo (Carga Rápida)"
])

st.sidebar.divider()
usuario_actual = st.sidebar.text_input("Operador a cargo:", "Comandante Principal")

# Leer inventario y ventas actuales
with open(ARCHIVO_INVENTARIO, mode='r', encoding='utf-8') as f:
    inventario_data = list(csv.DictReader(f))

ventas_data = []
if os.path.exists(ARCHIVO_VENTAS):
    with open(ARCHIVO_VENTAS, mode='r', encoding='utf-8') as f:
        ventas_data = list(csv.DictReader(f))


# ==========================================
# MODO 1: VENDEDOR DE CAMPO (Carga Rápida)
# ==========================================
if modo_operacion == "🛒 Vendedor de Campo (Carga Rápida)":
    st.title("🛒 Portal de Venta Táctica en Campo")
    st.markdown("##### *Terminal Móvil para registro inmediato de operaciones de venta.*")
    st.divider()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📝 Registrar Nueva Venta")
        with st.form("form_venta_campo"):
            sku_opciones = [p["SKU"] + " | " + p["Producto"] + " (Stock: " + str(p["Stock Actual"]) + ")" for p in inventario_data]
            prod_seleccionado = st.selectbox("Seleccionar Producto", sku_opciones)
            cantidad = st.number_input("Cantidad Vendida", min_value=1, value=1)
            segmento = st.selectbox("Segmento de Cliente", ["Fuerzas de Seguridad", "Corporativo / Empresas", "Particular / Airsoft"])
            
            btn_vender = st.form_submit_button("Confirmar Venta en Tiempo Real")

            if btn_vender:
                sku_limpio = prod_seleccionado.split(" | ")[0]
                fecha_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
                id_vta = "VNT-" + datetime.datetime.now().strftime("%H%M%S")
                
                # Procesar cálculos de stock y finanzas
                costo_unit = 0
                pvp_unit = 0
                nombre_prod = ""
                
                for p in inventario_data:
                    if p["SKU"] == sku_limpio:
                        nombre_prod = p["Producto"]
                        costo_unit = float(p["Costo Unitario"])
                        pvp_unit = float(p["PVP Sugerido"])
                        stock_actual = int(p["Stock Actual"])
                        
                        nuevo_stock = max(0, stock_actual - int(cantidad))
                        p["Stock Actual"] = str(nuevo_stock)
                        
                        if nuevo_stock <= int(p["Stock Minimo"]):
                            p["Estado Stock"] = "⚠️ ALERTA STOCK BAJO"
                        else:
                            p["Estado Stock"] = "🟢 OK"
                
                total_venta = pvp_unit * int(cantidad)
                costo_total = costo_unit * int(cantidad)
                ganancia_venta = total_venta - costo_total

                # Guardar venta
                with open(ARCHIVO_VENTAS, mode='a', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow([id_vta, fecha_str, sku_limpio, nombre_prod, cantidad, costo_total, total_venta, ganancia_venta, segmento])

                # Actualizar inventario CSV
                with open(ARCHIVO_INVENTARIO, mode='w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=inventario_data[0].keys())
                    writer.writeheader()
                    writer.writerows(inventario_data)

                st.success(f"✅ Venta {id_vta} registrada con éxito. Inventario actualizado y reportado a la base maestra.")

    with col2:
        st.subheader("📦 Estado Rápido de Stock en Campo")
        st.table([{ "SKU": p["SKU"], "Producto": p["Producto"], "Stock": p["Stock Actual"], "Estado": p["Estado Stock"] } for p in inventario_data])


# ==========================================
# MODO 2: COMANDANTE MAESTRO (War Room & IA)
# ==========================================
else:
    st.title("🛡️ EQUIPO 1: Sala de Situación y Comando Maestro")
    st.markdown("##### *Panel Ejecutivo de Control Financiero, Logístico y Coordinación del Colectivo de 8 Agentes IA*")
    st.divider()

    # Métricas Superiores de Rendimiento Financiero y Stock
    total_ingresos = sum([float(v["Total_Venta"]) for v in ventas_data]) if ventas_data else 0.0
    total_ganancias = sum([float(v["Ganancia"]) for v in ventas_data]) if ventas_data else 0.0
    total_unidades_vendidas = sum([int(v["Cantidad"]) for v in ventas_data]) if ventas_data else 0.0
    alertas_quiebre = sum([1 for p in inventario_data if "ALERTA" in p["Estado Stock"]])

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric(label="💰 Ingresos Totales", value=f"${total_ingresos:,.0f}")
    with m2:
        st.metric(label="📈 Ganancia Neta", value=f"${total_ganancias:,.0f}")
    with m3:
        st.metric(label="🛒 Unidades Vendidas", value=total_unidades_vendidas)
    with m4:
        st.metric(label="⚠️ Alertas de Quiebre", value=alertas_quiebre)

    st.divider()

    # Layout de la War Room: Estado de los Agentes
    col_izq, col_der = st.columns(2)

    with col_izq:
        st.subheader("📂 Agentes Internos (Operaciones y Finanzas)")
        
        if alertas_quiebre > 0:
            st.markdown("""
                <div class='alert-card'>
                    <h4>1. 📦 Logística y Stock</h4>
                    <p><b>Estado:</b> ⚠️ ALERTA DE QUIEBRE DETECTADA</p>
                    <p><i>El Agente 1 ha activado el protocolo de reposición con proveedores directos.</i></p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class='agent-card'>
                    <h4>1. 📦 Logística y Stock</h4>
                    <p><b>Estado:</b> 🟢 Niveles Óptimos</p>
                    <p><i>Inventario sincronizado y sin quiebres críticos en curso.</i></p>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class='agent-card'>
                <h4>2. 📊 Finanzas y Cumplimiento Legal</h4>
                <p><b>Estado:</b> 🟢 Operativo y Rentable</p>
                <p><i>Monitoreando márgenes comerciales (objetivo 40%) y normativas NIJ.</i></p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class='agent-card'>
                <h4>3. 🗂️ CRM y Operaciones Internas</h4>
                <p><b>Estado:</b> 🟢 Sincronizado</p>
                <p><i>Base de datos segmentada para Fuerzas de Seguridad y corporativos.</i></p>
            </div>
        """, unsafe_allow_html=True)

    with col_der:
        st.subheader("🎯 Agentes Externos (Mercado y Ventas)")
        st.markdown("""
            <div class='agent-card'>
                <h4>4. 🎯 Ventas y Asesoramiento Táctico</h4>
                <p><b>Estado:</b> 🟢 Atendiendo en Campo</p>
                <p><i>Procesando altas de ventas y asesoramiento técnico especializado.</i></p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class='agent-card'>
                <h4>5. 📣 Marketing y Captación</h4>
                <p><b>Estado:</b> 🟢 Activo</p>
                <p><i>Campañas de rendimiento extremo orientadas a equipamiento táctico.</i></p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class='agent-card'>
                <h4>6. 🤝 Postventa y Fidelización</h4>
                <p><b>Estado:</b> 🟢 Seguimiento OK</p>
                <p><i>Garantías balísticas y control de satisfacción en curso.</i></p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class='agent-card'>
                <h4>7. 🕵️‍♂️ Investigador (Mystery Shopper)</h4>
                <p><b>Estado:</b> 🟢 Escaneando Competencia</p>
                <p><i>Relevamiento activo de precios formales e informales en el mercado.</i></p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("""
            <div class='agent-card'>
                <h4>8. 🏭 Gestor de Proveedores / Compras</h4>
                <p><b>Estado:</b> 🟢 Negociando Costos</p>
                <p><i>Evaluando relación precio-calidad con talleres directos de fábrica.</i></p>
            </div>
        """, unsafe_allow_html=True)

    st.divider()

    # Tablas maestras de control de stock y ventas
    st.subheader("📊 Tabla Maestra de Inventario en Tiempo Real")
    st.table(inventario_data)

    if ventas_data:
        st.subheader("🛒 Historial Maestro de Ventas e Ingresos")
        st.table(ventas_data)
    else:
        st.info("ℹ️ Aún no se han registrado ventas en el sistema. Utiliza el 'Vendedor de Campo' para cargar la primera operación.")

    st.divider()

    # Consola de Interacción Maestra con los Agentes
    st.subheader("💬 Consola de Comando e Interacción con los 8 Agentes IA")
    pregunta_maestra = st.text_input("Asigna una orden, solicita un informe financiero o consulta al colectivo de agentes:")

    if st.button("Transmitir Directiva Maestra"):
        if pregunta_maestra:
            st.success(f"Orden ejecutada por {usuario_actual}: '{pregunta_maestra}'")
            st.info("🤖 **Respuesta del Colectivo de Agentes (Equipo 1):** Directiva analizada por los módulos de Logística, Finanzas y Ventas. Los registros en la base de datos se han sincronizado correctamente.")
        else:
            st.warning("Por favor, ingresa una directiva para los agentes.")

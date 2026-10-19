import streamlit as st
import datetime
import os
import csv

# Configuración de la página
st.set_page_config(
    page_title="Equipo 1 - Sala de Comando Táctico",
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
    </style>
""", unsafe_allow_html=True)

# Archivo CSV simulado / local para la nube
ARCHIVO_INVENTARIO = "inventario_equipo1.csv"

def inicializar_inventario_si_no_existe():
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

inicializar_inventario_si_no_existe()

# Encabezado principal
st.title("🛡️ EQUIPO 1: Sala de Situación y Comando Táctico")
st.markdown("##### *Ecosistema de 8 Agentes IA especializados en Equipamiento Militar y Táctico*")
st.divider()

# Sidebar para control general del Comandante
st.sidebar.title("🎛️ Panel de Control")
comandante = st.sidebar.text_input("Comandante a cargo:", "Usuario Principal")
modo_reunion = st.sidebar.selectbox("Estado de la Sala:", [
    "🟢 Reunión Operativa Normal", 
    "🚨 Alerta de Abastecimiento", 
    "🕵️‍♂️ Revisión de Competencia (Mystery Shopper)"
])

st.sidebar.divider()
st.sidebar.markdown("### 📂 Archivos Centrales en Línea")
st.sidebar.text("• inventario_equipo1.csv (Conectado)")
st.sidebar.text("• proveedores_equipo1.csv")
st.sidebar.text("• competencia_equipo1.csv")

# Layout de la Sala de Reuniones (Dos columnas: Internos y Externos)
col_izq, col_der = st.columns(2)

with col_izq:
    st.subheader("📂 Agentes Internos (Operaciones)")
    
    # Lectura dinámica del inventario para el Agente 1 (Logística)
    with open(ARCHIVO_INVENTARIO, mode='r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        inventario_data = list(reader)
    
    alerta_activa = False
    for prod in inventario_data:
        if "ALERTA" in prod["Estado Stock"] or int(prod["Stock Actual"]) <= int(prod["Stock Minimo"]):
            alerta_activa = True
            st.markdown(f"""
                <div class='alert-card'>
                    <h4>1. 📦 Logística y Stock</h4>
                    <p><b>Estado:</b> ⚠️ Alerta de Quiebre ({prod['SKU']} - {prod['Producto']})</p>
                    <p><i>Stock Actual: {prod['Stock Actual']} | Mínimo requerido: {prod['Stock Minimo']}</i></p>
                </div>
            """, unsafe_allow_html=True)
            break
            
    if not alerta_activa:
        st.markdown("""
            <div class='agent-card'>
                <h4>1. 📦 Logística y Stock</h4>
                <p><b>Estado:</b> 🟢 Niveles Óptimos de Stock</p>
                <p><i>Monitoreando inventario en tiempo real sin quiebres críticos.</i></p>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class='agent-card'>
            <h4>2. 📊 Finanzas y Cumplimiento Legal</h4>
            <p><b>Estado:</b> 🟢 Operativo</p>
            <p><i>Validando márgenes (40% objetivo) y normativas balísticas NIJ.</i></p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class='agent-card'>
            <h4>3. 🗂️ CRM y Operaciones Internas</h4>
            <p><b>Estado:</b> 🟢 Sincronizado</p>
            <p><i>Segmentando fuerzas de seguridad, corporativos y particulares.</i></p>
        </div>
    """, unsafe_allow_html=True)

with col_der:
    st.subheader("🎯 Agentes Externos (Mercado y Ventas)")
    
    st.markdown("""
        <div class='agent-card'>
            <h4>4. 🎯 Ventas y Asesoramiento Táctico</h4>
            <p><b>Estado:</b> 🟢 Atendiendo</p>
            <p><i>Dominio técnico en Cordura, Ripstop y especificaciones de campo.</i></p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class='agent-card'>
            <h4>5. 📣 Marketing y Captación</h4>
            <p><b>Estado:</b> 🟢 Activo</p>
            <p><i>Generando copys de rendimiento extremo para anuncios y redes.</i></p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class='agent-card'>
            <h4>6. 🤝 Postventa y Fidelización</h4>
            <p><b>Estado:</b> 🟢 Seguimiento OK</p>
            <p><i>Controlando entregas, garantías y venta cruzada de accesorios.</i></p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class='agent-card'>
            <h4>7. 🕵️‍♂️ Investigador (Mystery Shopper)</h4>
            <p><b>Estado:</b> 🟢 Escaneando</p>
            <p><i>Relevando precios formales e informales en canales digitales y locales.</i></p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class='agent-card'>
            <h4>8. 🏭 Gestor de Proveedores / Compras</h4>
            <p><b>Estado:</b> 🟢 Negociando</p>
            <p><i>Contactando talleres directos de fábrica por mejor precio/calidad.</i></p>
        </div>
    """, unsafe_allow_html=True)

st.divider()

# Visualizador y editor rápido de inventario en la misma War Room
st.subheader("📊 Inventario en Tiempo Real (Conectado a CSV)")
st.table(inventario_data)

st.divider()

# Consola central de interacción con la sala
st.subheader("💬 Consola de Debate y Órdenes al Equipo 1")
pregunta_usuario = st.text_input("Dirígete a la sala de reuniones o asigna una tarea a un agente:")

if st.button("Enviar Directiva a la Sala"):
    if pregunta_usuario:
        st.success(f"Orden emitida por {comandante}: '{pregunta_usuario}'")
        st.info("🤖 **Respuesta del Colectivo de Agentes:** Directiva registrada y distribuida al módulo correspondiente. Los registros en archivos CSV se actualizarán de forma automática.")
    else:
        st.warning("Por favor, escribe una directiva para el equipo.")

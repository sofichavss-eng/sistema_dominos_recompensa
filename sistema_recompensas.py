# sistema_recompensas.py
# Domino's – Sistema Interno de Recompensas 
import streamlit as st, json, os, pandas as pd, random
from datetime import datetime

st.set_page_config(page_title="Domino's Pizza - Sistema de Recompensas", page_icon="🍕")

# --- estilos ---
st.markdown("""
<style>
section.main {background: linear-gradient(180deg,#ffffff,#f5f6fa);}
.title {font-size:30px;font-weight:800;color:#E31837;}
.subtitle {font-size:16px;color:#004B91;margin-bottom:20px;}
.card {background:white;padding:16px;border-radius:15px;
box-shadow:0 6px 16px rgba(0,0,0,0.08);margin-bottom:18px;}
.stButton>button {background:linear-gradient(90deg,#004B91,#0072CE);
color:white;font-weight:600;border-radius:10px;padding:10px 18px;}
.stButton>button:hover {background:linear-gradient(90deg,#E31837,#ff4b5c);}
.points {font-size:28px;font-weight:800;color:#E31837;}
</style>
""", unsafe_allow_html=True)

DATA_FILE = "empleados.json"
def cargar(): 
    return json.load(open(DATA_FILE,"r",encoding="utf-8")) if os.path.exists(DATA_FILE) else {}
def guardar(d): 
    json.dump(d,open(DATA_FILE,"w",encoding="utf-8"),indent=2,ensure_ascii=False)

empleados = cargar()

# Datos iniciales si no existen
if not empleados:
    empleados = {
        "juan perez":{"puntos":820,"ventas":3200,"puntualidad":95,"servicio":90,"historial":[]},
        "maria lopez":{"puntos":430,"ventas":2100,"puntualidad":88,"servicio":92,"historial":[]},
        "lara chavez":{"puntos":500,"ventas":2500,"puntualidad":94,"servicio":91,"historial":[]}
    }
    guardar(empleados)

RECOMPENSAS=[
 {"nombre":"🍕 Pizza Gratis","costo":300,"desc":"Una pizza personal gratuita"},
 {"nombre":"🥤 Combo completo","costo":400,"desc":"Pizza + gaseosa + postre"},
 {"nombre":"🕐 Medio día libre","costo":500,"desc":"Descanso adicional de medio día"},
 {"nombre":"🏖️ Día libre completo","costo":1000,"desc":"Un día libre remunerado"},
 {"nombre":"💸 Bonificación S/100","costo":1500,"desc":"Bonificación económica"},
 {"nombre":"🏅 Empleado del mes","costo":200,"desc":"Reconocimiento especial en el equipo"},
]

RANGOS=[("🥉 Bronce",0,499),("🥈 Plata",500,999),("🥇 Oro",1000,99999)]
def nivel(p):
    for n,a,b in RANGOS:
        if a<=p<=b:return n,(p-a)/(b-a+1)
    return "🥉 Bronce",0

# encabezado
c1,c2=st.columns([1,5])
if os.path.exists("logo.png"): c1.image("logo.png",width=80)
c2.markdown("<div class='title'>Domino's Pizza</div>",unsafe_allow_html=True)
c2.markdown("<div class='subtitle'>Sistema Interno de Recompensas</div>",unsafe_allow_html=True)
st.markdown("---")

# login principal
st.markdown("<div class='card'>",unsafe_allow_html=True)
rol=st.radio("Selecciona tu rol:",["Empleado","Gerente"],horizontal=True)

# crear cuenta
if rol=="Empleado":
    sub=st.radio("Elige una opción:",["Iniciar sesión","Crear cuenta nueva"])
    nombre=st.text_input("Nombre del empleado:").lower().strip()
    if sub=="Crear cuenta nueva":
        if st.button("Crear cuenta"):
            if nombre and nombre not in empleados:
                empleados[nombre]={"puntos":0,"ventas":0,"puntualidad":100,"servicio":100,"historial":[]}
                guardar(empleados)
                st.success(f"Empleado {nombre.title()} creado correctamente ✅")
            else: st.warning("Ese nombre ya existe o está vacío.")
    elif st.button("Entrar"):
        if nombre in empleados:
            st.session_state["empleado"]=nombre
            st.session_state["rol"]="Empleado"
            st.success(f"Bienvenido/a, {nombre.title()} 🍕")
        else: st.error("Empleado no encontrado.")
elif rol=="Gerente":
    pwd=st.text_input("Contraseña del gerente:",type="password")
    if st.button("Entrar"):
        if pwd=="empleados":
            st.session_state["rol"]="Gerente"; st.success("Acceso concedido ✅")
        else: st.error("Contraseña incorrecta.")
st.markdown("</div>",unsafe_allow_html=True)

# --- vista empleado ---
# --- vista empleado (centrado, estilo anterior con botones) ---
if st.session_state.get("rol") == "Empleado":
    nombre = st.session_state["empleado"]
    emp = empleados[nombre]

    # --- saludo y frase ---
    frases = [
        "🔥 ¡Sigue así, tu esfuerzo te acerca a Oro!",
        "💪 La constancia te hace destacar.",
        "🍕 ¡Tu trabajo en equipo marca la diferencia!"
    ]
    frase = random.choice(frases)

    st.markdown(f"""
    <div style="text-align:center; margin-top:20px;">
        <h2>👋 Hola, {nombre.title()}!</h2>
        <p style="font-size:18px; color:#004B91;">{frase}</p>
        <hr style="margin:10px 0 30px 0;">
    </div>
    """, unsafe_allow_html=True)

    # --- menú centrado ---
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.markdown(
            "<div style='text-align:center; font-weight:600; font-size:18px;'>Selecciona una opción:</div>",
            unsafe_allow_html=True)
        opcion = st.radio(
            "",
            ["Ver mis puntos", "Canjear recompensas", "Ver desempeño", "Ver historial", "Cerrar sesión"],
            horizontal=False,
            label_visibility="collapsed"
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # --- contenido de cada opción ---
    if opcion == "Ver mis puntos":
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown(f"<div class='points'>{emp['puntos']} puntos</div>", unsafe_allow_html=True)
        nivel_act, progreso = nivel(emp["puntos"])
        st.progress(progreso)
        st.markdown(f"Nivel actual: **{nivel_act}**")
        st.markdown("#### Rangos de puntos:")
        for r in RANGOS:
            st.markdown(f"- {r[0]}: {r[1]} a {r[2]} pts")
        st.markdown("</div>", unsafe_allow_html=True)

    elif opcion == "Canjear recompensas":
        st.markdown("### 🎁 Catálogo de recompensas")
        for r in RECOMPENSAS:
            st.markdown(f"**{r['nombre']}** — {r['costo']} pts")
            st.caption(r['desc'])
            if st.button(f"Canjear {r['nombre']}", key=r['nombre']):
                if emp["puntos"] >= r["costo"]:
                    emp["puntos"] -= r["costo"]
                    emp["historial"].append({
                        "acción": "Canje",
                        "recompensa": r["nombre"],
                        "fecha": datetime.now().strftime("%d/%m/%Y %H:%M")
                    })
                    guardar(empleados)
                    st.balloons()
                    st.success(f"Canje realizado: {r['nombre']} ✅")
                else:
                    st.warning("No tienes puntos suficientes para canjear esta recompensa.")

    elif opcion == "Ver desempeño":
        st.markdown("### 📈 Mi desempeño")
        df = pd.DataFrame({
            "Métrica": ["Ventas (S/)", "Puntualidad (%)", "Servicio (%)"],
            "Valor": [emp["ventas"], emp["puntualidad"], emp["servicio"]]
        })
        st.table(df)

    elif opcion == "Ver historial":
        st.markdown("### 📜 Historial de acciones")
        if emp["historial"]:
            hist = pd.DataFrame(emp["historial"])
            st.dataframe(hist)
        else:
            st.info("Aún no tienes historial registrado.")

    elif opcion == "Cerrar sesión":
        for k in ["rol", "empleado"]:
            st.session_state.pop(k, None)
        st.success("Sesión cerrada correctamente.")
        st.experimental_rerun()

# --- vista gerente ---
elif st.session_state.get("rol")=="Gerente":
    st.markdown("## 👨‍💼 Panel del Gerente")

    # crear empleado
    st.markdown("### ➕ Crear nuevo empleado")
    nuevo=st.text_input("Nombre del nuevo empleado:").lower().strip()
    if st.button("Crear empleado"):
        if nuevo and nuevo not in empleados:
            empleados[nuevo]={"puntos":0,"ventas":0,"puntualidad":100,"servicio":100,"historial":[]}
            guardar(empleados); st.success(f"Empleado {nuevo.title()} añadido ✅")
        else: st.warning("Nombre vacío o ya existente.")

    st.markdown("### 👀 Todos los empleados")
    df=pd.DataFrame([
      {"Empleado":k.title(),"Puntos":v["puntos"],"Ventas":v["ventas"],
       "Puntualidad":v["puntualidad"],"Servicio":v["servicio"]}
      for k,v in empleados.items()])
    st.dataframe(df)

    st.markdown("### ✏️ Actualizar datos")
    sel=st.selectbox("Selecciona empleado:",list(empleados.keys()))
    puntos_add=st.number_input("Añadir puntos",min_value=0,max_value=5000,step=50)
    ventas_add=st.number_input("Añadir ventas (S/)",min_value=0,max_value=10000,step=100)
    motivos=["Venta destacada","Puntualidad","Buen servicio","Meta alcanzada"]
    motivo_sel=st.selectbox("Motivo:",motivos)
    motivo_text=st.text_input("Otro motivo (opcional):")
    if st.button("Actualizar empleado"):
        empleados[sel]["puntos"]+=puntos_add
        empleados[sel]["ventas"]+=ventas_add
        motivo_final=motivo_text if motivo_text else motivo_sel
        empleados[sel]["historial"].append({
          "acción":"Actualización del gerente","puntos añadidos":puntos_add,
          "ventas añadidas":ventas_add,"motivo":motivo_final,
          "fecha":datetime.now().strftime("%d/%m/%Y %H:%M")})
        guardar(empleados); st.success(f"{sel.title()} actualizado ✅")

    # top empleados y gráfico
    st.markdown("### 🏅 Top 3 empleados")
    top=sorted(empleados.items(),key=lambda x:x[1]["puntos"],reverse=True)[:3]
    for i,(k,v) in enumerate(top,1):
        st.write(f"{i}. {k.title()} — {v['puntos']} pts ({nivel(v['puntos'])[0]})")

    st.markdown("### 📊 Distribución de rangos")
    cont={"Bronce":0,"Plata":0,"Oro":0}
    for e in empleados.values():
        n,_=nivel(e["puntos"])
        if "Bronce" in n: cont["Bronce"]+=1
        elif "Plata" in n: cont["Plata"]+=1
        else: cont["Oro"]+=1
    st.bar_chart(pd.DataFrame.from_dict(cont,orient="index",columns=["Empleados"]))

    if st.button("Cerrar sesión del gerente"):
        st.session_state.pop("rol",None)
        st.experimental_rerun()

st.caption("🍕 Domino's Pizza · Sistema de Recompensas · Proyecto académico 2025")
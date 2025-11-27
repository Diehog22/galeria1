import streamlit as st
import os
import json
from PIL import Image

# -----------------------------
# CONFIGURACIÓN
# -----------------------------
UPLOAD_FOLDER = "uploads"
DATA_FILE = "data.json"

ADMIN_USER = "husarph1"
ADMIN_PASS = "SpaceGh0st"

# -----------------------------
# CREAR CARPETAS Y ARCHIVOS
# -----------------------------
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump([], f)

# -----------------------------
# GUARDAR COMENTARIOS
# -----------------------------
def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

# -----------------------------
# PÁGINA PRINCIPAL
# -----------------------------
def main_page():
    st.title("📸 Galería Comunitaria")
    st.write("Sube una foto y deja un comentario.")

    uploaded = st.file_uploader("Sube una imagen", type=["jpg", "jpeg", "png"])
    comment = st.text_input("Comentario")
    
    if st.button("Publicar"):
        if uploaded:
            img_path = os.path.join(UPLOAD_FOLDER, uploaded.name)
            with open(img_path, "wb") as f:
                f.write(uploaded.getbuffer())

            data = load_data()
            data.append({"image": img_path, "comment": comment})
            save_data(data)

            st.success("Publicado correctamente!")
        else:
            st.error("Sube una imagen primero.")

    st.write("---")
    st.subheader("🖼️ Galería")

    data = load_data()
    cols = st.columns(3)

    for i, item in enumerate(data):
        with cols[i % 3]:
            st.image(item["image"], use_column_width=True)
            st.caption(item["comment"])

    st.write("---")
    if st.button("Entrar como administrador"):
        st.session_state["admin_mode"] = True

# -----------------------------
# ADMIN PAGE
# -----------------------------
def admin_page():
    st.title("🔐 Administrador")

    user = st.text_input("Usuario")
    password = st.text_input("Contraseña", type="password")

    if st.button("Entrar"):
        if user == ADMIN_USER and password == ADMIN_PASS:
            st.session_state["auth"] = True
        else:
            st.error("Usuario o contraseña incorrectos")

    if st.session_state.get("auth"):
        st.success("Sesión iniciada")
        st.subheader("Borrar imágenes o comentarios")

        data = load_data()

        for i, item in enumerate(data):
            st.image(item["image"], width=200)
            st.write(f"Comentario: {item['comment']}")

            if st.button(f"Borrar {i}"):
                try:
                    os.remove(item["image"])
                except:
                    pass

                data.pop(i)
                save_data(data)
                st.warning("Eliminado.")
                st.experimental_rerun()

        if st.button("Salir del modo admin"):
            st.session_state["admin_mode"] = False
            st.session_state["auth"] = False
            st.experimental_rerun()


# -----------------------------
# ROUTER
# -----------------------------
if "admin_mode" not in st.session_state:
    st.session_state["admin_mode"] = False

if not st.session_state["admin_mode"]:
    main_page()
else:
    admin_page()

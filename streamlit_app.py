import streamlit as st
import json
import os
from pathlib import Path

# --------------------------------------------------
# CONFIG
# --------------------------------------------------
st.set_page_config(page_title="Galería Pública", layout="wide")

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

DATA_FILE = "data.json"

ADMIN_USER = "admin"
ADMIN_PASS = "12345"

# --------------------------------------------------
# UTILIDADES
# --------------------------------------------------
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def add_entry(filename, user, comment):
    data = load_data()
    data.append({
        "filename": filename,
        "user": user,
        "comment": comment
    })
    save_data(data)

def delete_entry(filename):
    data = load_data()
    data = [d for d in data if d["filename"] != filename]
    save_data(data)

    # borrar archivo
    try:
        os.remove(UPLOAD_DIR / filename)
    except:
        pass

# --------------------------------------------------
# INTERFAZ
# --------------------------------------------------
st.title("📸 Galería Pública sin Base de Datos")

st.write("Sube una imagen con un comentario para que aparezca en el tablero.")

# --------------------------------------------------
# SUBIR
# --------------------------------------------------
user = st.text_input("Tu nombre (opcional):", "")
comment = st.text_area("Comentario:")
image_file = st.file_uploader("Subir imagen", type=["jpg", "jpeg", "png"])

if image_file and st.button("📤 Publicar"):
    filepath = UPLOAD_DIR / image_file.name
    filepath.write_bytes(image_file.getvalue())

    add_entry(image_file.name, user if user else "Anónimo", comment)

    st.success("📸 Imagen publicada con éxito")
    st.experimental_rerun()

# --------------------------------------------------
# GALERÍA
# --------------------------------------------------
st.write("---")
st.header("🖼️ Galería")

entries = load_data()

cols = st.columns(4)

for idx, entry in enumerate(reversed(entries)):
    col = cols[idx % 4]
    with col:
        st.image(f"uploads/{entry['filename']}", use_column_width=True)
        st.caption(f"**{entry['user']}**: {entry['comment']}")

# --------------------------------------------------
# ADMIN
# --------------------------------------------------
st.write("---")
st.subheader("🔐 Administrador")

if "admin" not in st.session_state:
    st.session_state["admin"] = False

if not st.session_state["admin"]:
    a_user = st.text_input("Usuario:")
    a_pass = st.text_input("Contraseña:", type="password")

    if st.button("Entrar"):
        if a_user == ADMIN_USER and a_pass == ADMIN_PASS:
            st.session_state["admin"] = True
            st.success("Acceso concedido ✔")
        else:
            st.error("Credenciales incorrectas.")
else:
    st.success("Bienvenido administrador ✔")

    st.write("Puedes borrar imágenes inapropiadas:")

    for entry in entries:
        st.image(f"uploads/{entry['filename']}", width=150)
        st.write(f"{entry['user']}: {entry['comment']}")

        if st.button(f"🗑 Borrar {entry['filename']}"):
            delete_entry(entry["filename"])
            st.warning("Imagen eliminada.")
            st.experimental_rerun()

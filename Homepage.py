import ifcopenshell
import ifcopenshell.geom
import py3Dmol
import streamlit as st
import pandas as pd
import tempfile
import os

def convert_ifc_to_obj(ifc_file_path, obj_file_path):
    settings = ifcopenshell.geom.settings()
    settings.set(settings.USE_PYTHON_OPENCASCADE, True)
    ifc_file = ifcopenshell.open(ifc_file_path)

    with open(obj_file_path, "w") as obj_file:
        for product in ifc_file.by_type("IfcProduct"):
            try:
                shape = ifcopenshell.geom.create_shape(settings, product)
                obj_data = shape.geometry.to_obj()
                obj_file.write(obj_data)
            except Exception as e:
                print(f"Failed to process {product}: {e}")

def callback_upload():
    if "uploaded_file" not in session or session["uploaded_file"] is None:
        return

    # Save the uploaded IFC file to disk
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ifc") as ifc_file:
        ifc_file.write(session["uploaded_file"].getvalue())
        ifc_file_path = ifc_file.name

    # Convert the IFC file to an OBJ file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".obj") as obj_file:
        obj_file_path = obj_file.name

    convert_ifc_to_obj(ifc_file_path, obj_file_path)

    # Store the OBJ file path in the session state
    session["obj_file_path"] = obj_file_path

    # Read the IFC file using ifcopenshell
    session["ifc_file"] = ifcopenshell.open(ifc_file_path)
    session["is_file_loaded"] = True

def show_obj(obj_file_path):
    with open(obj_file_path, 'r') as obj_file:
        obj_data = obj_file.read()

    viewer = py3Dmol.view(width=800, height=600)
    viewer.addModel(obj_data, 'obj')
    viewer.setStyle({'stick': {}})
    viewer.setBackgroundColor('0xeeeeee')
    viewer.zoomTo()
    viewer.show()

def main():      
    if "is_file_loaded" not in session:
        session["is_file_loaded"] = False

    st.set_page_config(
        layout= "wide",
        page_title="IFC Stream",
        page_icon="✍️",
    )
    st.title("Streamlit IFC")
    st.markdown(
    """ 
    ###  📁 Click on Browse File in the Side Bar to start
    """
    )

    ## Add File uploader to Side Bar Navigation
    st.sidebar.header('Model Loader')
    st.sidebar.file_uploader("📁 Choose a file", type=['ifc', 'IFC'], key="uploaded_file", on_change=callback_upload)

    ## Add Reset Button
    if st.sidebar.button("🔄️ Reset"):
        session.clear()

    ## Add File Name and Success Message
    if "is_file_loaded" in session and session["is_file_loaded"]:
        st.sidebar.success(f'Project successfully loaded')
        st.sidebar.write("🔃 You can reload a new file  ")
        
        col1, col2 = st.columns([2,1])
        col1.subheader(f'Start Exploring "{get_project_name()}"')
        col2.text_input("✏️ Change Project Name", key="project_name_input")
        col2.button("✔️ Apply", key="change_project_name", on_click=change_project_name())
    st.sidebar.write("""
    --------------
    --------------
    
    
    """)
    st.write("")
    st.sidebar.write("")

if __name__ == "__main__":
    session = st.session_state
    main()

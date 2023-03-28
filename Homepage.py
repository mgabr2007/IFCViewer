import ifcopenshell
import py3Dmol
import streamlit as st
import pandas as pd
import os
import subprocess

def convert_ifc_to_obj(ifc_file_path, obj_file_path):
    ifc_convert_executable = './IfcConvert'  # Path to the IfcConvert executable
    if not os.path.exists(ifc_convert_executable):
        raise FileNotFoundError(f'IfcConvert executable not found at {ifc_convert_executable}')

    command = f"{ifc_convert_executable} {ifc_file_path} {obj_file_path}"
    result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    if result.returncode != 0:
        raise RuntimeError(f"Error during IFC to OBJ conversion: {result.stderr.decode('utf-8')}")

def callback_upload():
    session["file_name"] = session["uploaded_file"].name
    session["array_buffer"] = session["uploaded_file"].getvalue()
    session["ifc_file"] = ifcopenshell.file.from_string(session["array_buffer"].decode("utf-8"))
    session["is_file_loaded"] = True
    if "uploaded_file" not in session or session["uploaded_file"] is None:
        return

    session["file_name"] = session["uploaded_file"].name

    # Save the uploaded IFC file to disk
    ifc_file_path = f"temp_{session['file_name']}"
    with open(ifc_file_path, "wb") as ifc_file:
        ifc_file.write(session["array_buffer"])

    # Convert the IFC file to an OBJ file
    obj_file_path = f"temp_{session['file_name']}.obj"
    convert_ifc_to_obj(ifc_file_path, obj_file_path)

    # Store the OBJ file path in the session state
    session["obj_file_path"] = obj_file_path

    # Extract data from IFC file
    walls = session["ifc_file"].by_type("IfcWall")
    windows = session["ifc_file"].by_type("IfcWindow")
    doors = session["ifc_file"].by_type("IfcDoor")

    # Store data in session state
    session["data"] = {
        "walls": pd.DataFrame(walls),
        "windows": pd.DataFrame(windows),
        "doors": pd.DataFrame(doors),
    }

def get_project_name():
    return session.ifc_file.by_type("IfcProject")[0].Name

def change_project_name():
    if session.project_name_input:
        session.ifc_file.by_type("IfcProject")[0].Name = session.project_name_input
        st.sidebar.success("Project name changed successfully.")

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

    if "is_file_loaded" in session and session["is_file_loaded"]:
        # Display the 3D model
        show_obj(session["obj_file_path"])
    
    st.set_page_config(
        layout= "wide",
        page_title="IFC Stream",
        page_icon="✍️",
    )
    st.title("Streamlit IFC")
    st.markdown(
    """ 
    ###   📁 Click on Browse File in the Side Bar to start
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

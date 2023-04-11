import ifcopenshell
import streamlit as st
import pandas as pd
import os
from pages._🪟_Windows_info import windows_info_page

def callback_upload():
    session["file_name"] = session["uploaded_file"].name
    session["array_buffer"] = session["uploaded_file"].getvalue()
    session["ifc_file"] = ifcopenshell.file.from_string(session["array_buffer"].decode("utf-8"))
    session["is_file_loaded"] = True
    if "uploaded_file" not in session or session["uploaded_file"] is None:
        return

    session["file_name"] = session["uploaded_file"].name

def get_project_name():
    return session.ifc_file.by_type("IfcProject")[0].Name

def change_project_name():
    if session.project_name_input:
        session.ifc_file.by_type("IfcProject")[0].Name = session.project_name_input
        st.sidebar.success("Project name changed successfully.")

def main():      
    if "is_file_loaded" not in session:
        session["is_file_loaded"] = False
        
    st.set_page_config(
        layout= "wide",
        page_title="IFC Information",
        page_icon="✍️",
    )
    st.title("Streamlit IFC")
    st.markdown(
    """ 
    ###   📁 Click on Browse File in the Side Bar to start
    """
    )
    # Add a navigation menu to the sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Select a page:",
        ["Home", "Windows Info"],
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

    st.sidebar.write("""
    --------------
    --------------
    
    
    """)

    

    # Display the selected page
    if page == "Home":
        if "is_file_loaded" in session and session["is_file_loaded"]:
            col1, col2 = st.columns([2,1])
            col1.subheader(f'Start Exploring "{get_project_name()}"')
            col2.text_input("✏️ Change Project Name", key="project_name_input")
            col2.button("✔️ Apply", key="change_project_name", on_click=change_project_name())
    elif page == "Windows Info":
        windows_info_page(session.get("ifc_file"))

if __name__ == "__main__":
    session = st.session_state
    main()

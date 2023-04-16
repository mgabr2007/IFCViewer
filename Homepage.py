import ifcopenshell
import streamlit as st
import os
import glob
import importlib

def callback_upload():
    session.file_name = session.uploaded_file.name
    session.array_buffer = session.uploaded_file.getvalue()
    session.ifc_file = ifcopenshell.file.from_string(session.array_buffer.decode("utf-8"))
    session.is_file_loaded = True

    # Empty Previous Model Data from Session State
    session.isHealthDataLoaded = False
    session.HealthData = {}
    session.Graphs = {}
    session.SequenceData = {}
    session.CostScheduleData = {}

    # Empty Previous DataFrame from Session State
    session.DataFrame = None
    session.Classes = []
    session.IsDataFrameLoaded = False

def get_project_name():
    return session.ifc_file.by_type("IfcProject")[0].Name

def change_project_name():
    if session.project_name_input:
        session.ifc_file.by_type("IfcProject")[0].Name = session.project_name_input
        st.balloons()

def main():
    st.set_page_config(
        layout="wide",
        page_title="IFC Stream",
        page_icon="✍️",
    )
    st.title("Streamlit IFC")
    st.markdown(
        """ 
        ###  📁 Click on Browse File in the Side Bar to start
        """
    )

    # Add File uploader to Side Bar Navigation
    st.sidebar.header('Model Loader')
    st.sidebar.file_uploader("Choose a file", type=['ifc'], key="uploaded_file", on_change=callback_upload)

    # Add File Name and Success Message
    if "is_file_loaded" in session and session.is_file_loaded:
        st.sidebar.success(f'Project successfully loaded')
        st.sidebar.write("🔃 You can reload a new file  ")

        col1, col2 = st.columns([2, 1])
        col1.subheader(f'Start Exploring "{get_project_name()}"')
        col2.text_input("✏️ Change Project Name", key="project_name_input")
        col2.button("✔️ Apply", key="change_project_name", on_click=change_project_name)

    # Add the page navigation
    st.sidebar.subheader("Pages")

    # Get the list of .py files in the "pages" folder
    page_files = glob.glob("pages/*.py")
    page_links = []

    # Remove the "pages/" prefix and ".py" suffix and create the links
    for page_file in page_files:
        module_name = os.path.basename(page_file)[:-3]
        if module_name[0] != "_":  # Ignore files starting with an underscore
            link_text = module_name.replace("_", " ")
            page_links.append((link_text, module_name))

    # Display the page links and switch to the corresponding module when clicked
    for link_text, module_name in page_links:
        if st.sidebar.button(link_text):
            module = importlib.import_module(f'pages.{module_name}')
            module.execute()

    st.write("""
    --------------
    --------------
   
    """)
    st.write("")
    st.sidebar.write("")

if __name__ == "__main__":
    session = st.session_state
    main()

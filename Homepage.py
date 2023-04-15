import ifcopenshell
import streamlit as st
import os
import glob
import importlib


def callback_upload():
    st.session_state["file_name"] = st.session_state["uploaded_file"].name
    st.session_state["array_buffer"] = st.session_state["uploaded_file"].getvalue()
    st.session_state["ifc_file"] = ifcopenshell.file.from_string(st.session_state["array_buffer"].decode("utf-8"))
    st.session_state["is_file_loaded"] = True


def render_page(page_module):
    page_module.show()


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

    st.sidebar.header('Model Loader')
    uploaded_file = st.sidebar.file_uploader("Choose a file", type=['ifc'], key="uploaded_file",
                                             accept_multiple_files=False)

    if uploaded_file:
        callback_upload()

    if "is_file_loaded" in st.session_state and st.session_state["is_file_loaded"]:
        st.sidebar.success(f'Project successfuly loaded')
        st.sidebar.write("🔃 You can reload a new file  ")

        col1, col2 = st.columns([2, 1])
        col1.subheader(f'Start Exploring "{get_project_name()}"')
        col2.text_input("✏️ Change Project Name", key="project_name_input")
        col2.button("✔️ Apply", key="change_project_name", on_click=change_project_name())

    st.sidebar.write("""
    --------------
    --------------
    

    """)
    st.write("")
    st.sidebar.write("")

    # Get all .py files from the "pages" folder
    pages_folder = 'pages'
    py_files = glob.glob(os.path.join(pages_folder, "*.py"))

    # Get the module names and display names for the pages
    module_names = [os.path.splitext(os.path.basename(file))[0] for file in py_files]
    display_names = [name.replace('_', ' ').title() for name in module_names]

    # Create a dictionary to map display names to their corresponding modules
    page_modules = {}
    for module_name, display_name in zip(module_names, display_names):
        module = importlib.import_module(f'pages.{module_name}')
        page_modules[display_name] = module

    # Add the selectbox to the sidebar to choose between the pages
    selected_page = st.sidebar.selectbox('Choose a Page', display_names)

    # Render the selected page
    render_page(page_modules[selected_page])


if __name__ == "__main__":
    st.session_state
    main()

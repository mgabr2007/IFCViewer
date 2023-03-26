import ifcopenshell
import pandas as pd
import streamlit as st

def main():      
    st.set_page_config(
        layout= "wide",
        page_title="IFC Stream",
        page_icon="✍️",
    )
    st.title("Streamlit IFC")
    st.markdown(
        """ 
        ### 📁 Upload your IFC file
        """
    )

    uploaded_file = st.file_uploader("Choose a file", type=['ifc', 'IFC'])

    if uploaded_file is not None:
        # Load IFC file from uploaded file
        ifc_file = ifcopenshell.open(uploaded_file)

        # Extract available components from IFC file
        available_components = ["Pick Component"]
        for component in ["IfcWall", "IfcWindow", "IfcDoor"]:
            available_components.extend([c.Name for c in ifc_file.by_type(component)])

        # Store available components in session state
        session["available_components"] = available_components

        # Extract data from IFC file
        walls = ifc_file.by_type("IfcWall")
        windows = ifc_file.by_type("IfcWindow")
        doors = ifc_file.by_type("IfcDoor")

        # Store data in session state
        session["data"] = {
            "walls": pd.DataFrame(walls),
            "windows": pd.DataFrame(windows),
            "doors": pd.DataFrame(doors)
        }

        # Clear previous comparison results
        session["comparison"] = None
        
    # Add component selection dropdown
    if "available_components" in session:
        data_to_display = st.selectbox("Select component to display:", session["available_components"])

        # Check if data to display is present in session state
        if data_to_display not in session["data"]:
            st.warning("No data found for selected component.")
            return

        # Display selected component data
        st.write(session["data"][data_to_display])

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


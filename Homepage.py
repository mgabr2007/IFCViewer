import ifcopenshell
import pandas as pd
import streamlit as st



def callback_upload():
    session["file_name"] = session["uploaded_file"].name
    session["array_buffer"] = session["uploaded_file"].getvalue()
    session["ifc_file"] = ifcopenshell.file.from_string(session["array_buffer"].decode("utf-8"))
    session["is_file_loaded"] = True
    
    # Extract data from IFC file
    walls = session["ifc_file"].by_type("IfcWall")
    windows = session["ifc_file"].by_type("IfcWindow")
    doors = session["ifc_file"].by_type("IfcDoor")
    
    # Store data in session state
    session["data"] = {
        "walls": pd.DataFrame(walls),
        "windows": pd.DataFrame(windows),
        "doors": pd.DataFrame(doors)
    }

    # Clear previous comparison results
    session["comparison"] = None

def callback_upload():
    session["file_name"] = session["uploaded_file"].name
    session["array_buffer"] = session["uploaded_file"].getvalue()
    session["ifc_file"] = ifcopenshell.file.from_string(session["array_buffer"].decode("utf-8"))
    session["is_file_loaded"] = True

    # Extract available components from IFC file
    available_components = ["Pick Component"]
    for component in ["IfcWall", "IfcWindow", "IfcDoor"]:
        available_components.extend([c.Name for c in session["ifc_file"].by_type(component)])

    # Store available components in session state
    session["available_components"] = available_components

    # Empty Previous Model Data from Session State
    session["isHealthDataLoaded"] = False
    session["HealthData"] = {}
    session["Graphs"] = {}
    session["SequenceData"] = {}
    session["CostScheduleData"] = {}

    # Empty Previous DataFrame from Session State
    session["DataFrame"] = None
    session["Classes"] = []
    session["IsDataFrameLoaded"] = False

def compare_components():
    # Get user input for components to compare
    component_1 = st.selectbox("Select first component:", session["available_components"])
    component_2 = st.selectbox("Select second component:", session["available_components"])

    # Check if both components are the same
    if component_1 == component_2:
        st.warning("Please select two different components to compare.")
        return
    
    # Compare selected components
    data_1 = session["data"][component_1]
    data_2 = session["data"][component_2]

    # Convert all columns to a compatible data type
    for col in set(data_1.columns) & set(data_2.columns):
        data_1[col] = pd.to_numeric(data_1[col], errors="coerce")
        data_2[col] = pd.to_numeric(data_2[col], errors="coerce")
    
    # Concatenate selected components
    comparison = pd.concat([data_1.describe(), data_2.describe()], keys=[component_1, component_2], axis=1)
    
    # Store comparison results in session state
    session["comparison"] = comparison

def main():      
    st.set_page_config(
        layout= "wide",
        page_title="IFC Stream",
        page_icon="✍️",
    )
    st.title("Streamlit IFC")
    st.markdown(
        """ 
        ### 📁 Click on Browse File in the Side Bar to start
        """
    )

    # Add File uploader to Side Bar Navigation
    st.sidebar.header('Model Loader')
    st.sidebar.file_uploader("Choose a file", type=['ifc'], key="uploaded_file", on_change=callback_upload)

    # Add File Name and Success Message
    if "is_file_loaded" in session and session["is_file_loaded"]:
        st.sidebar.success(f'Project successfully loaded')
        st.sidebar.write("🔃 You can reload a new file")
        
        # Add component selection dropdown
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


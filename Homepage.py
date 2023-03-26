import ifcopenshell
import streamlit as st
import pandas as pd

def callback_upload():
    session["file_name"] = session["uploaded_file"].name
    session["array_buffer"] = session["uploaded_file"].getvalue()
    session["ifc_file"] = ifcopenshell.file.from_string(session["array_buffer"].decode("utf-8"))
    session["is_file_loaded"] = True
    
    ### Empty Previous Model Data from Session State
    session["isHealthDataLoaded"] = False
    session["HealthData"] = {}
    session["Graphs"] = {}
    session["SequenceData"] = {}
    session["CostScheduleData"] = {}

    ### Empty Previous DataFrame from Session State
    session["DataFrame"] = None
    session["Classes"] = []
    session["IsDataFrameLoaded"] = False

    # Extract available components from IFC file
    available_components = ["Pick Component"]
    for component in ["IfcWall", "IfcWindow", "IfcDoor"]:
        components_data = session["ifc_file"].by_type(component)
        if components_data:
            for c in components_data:
                data_frame = pd.DataFrame([c])
                if not data_frame.empty:
                    available_components.append(c.Name)
    # Store available components in session state
    session["available_components"] = available_components

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

    # Store a list of individual data frames
    session["data_frames"] = [pd.DataFrame(walls), pd.DataFrame(windows), pd.DataFrame(doors)]

##########################################################################
def get_project_name():
    return session.ifc_file.by_type("IfcProject")[0].Name

def change_project_name():
    if session.project_name_input:
        session.ifc_file.by_type("IfcProject")[0].Name = session.project_name_input
        st.sidebar.success("Project name changed successfully.")

def main():      
    if "is_file_loaded" not in session:
        session["is_file_loaded"] = False
    if "data" not in session:
        session["data"] = {}
    if "available_components" not in session:
        session["available_components"] = ["Pick Component"]
                                       
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

        if "available_components" in session:
            # Allow user to select a main component
            main_component = st.selectbox("Select main component:", ["Pick Component", "IfcWall", "IfcWindow", "IfcDoor"])

            if main_component != "Pick Component":
                # Filter available components based on the selected main component
                filtered_components = [comp for comp in session["available_components"] if comp.startswith(main_component)]

                # Add "Select All Components" option to the dropdown list
                options = ["Select All Components"] + filtered_components
                data_to_display = st.selectbox("Select specific component to display:", options, index=0)

                # Check if data to_display is present in session state and is not empty
                if data_to_display == "Select All Components":
                    all_data_frames = []
                    for key in session["data"]:
                        if key.startswith(main_component.lower()):  # Use lower() for case-insensitive comparison
                            data_frame = session["data"][key]
                            if not data_frame.empty:
                                all_data_frames.append(data_frame)

                    if all_data_frames:
                        combined_data_frame = pd.concat(all_data_frames)
                        st.write(combined_data_frame)
                    else:
                        st.warning("❌ No data found for selected component.")
                elif data_to_display in session["data"]:
                    data_frame = session["data"][data_to_display]
                    if not data_frame.empty:
                        st.write(data_frame)
                    else:
                        st.warning("❌ No data found for selected component.")
                else:
                    st.warning("❌  No data found for selected component.")
    st.sidebar.write("""
    --------------
    --------------
    
    
    """)
    st.write("")
    st.sidebar.write("")

if __name__ == "__main__":
    session = st.session_state
    main()

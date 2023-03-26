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

def compare_components():
    # Get user input for components to compare
    component_1 = st.selectbox("Select first component:", ["walls", "windows", "doors"])
    component_2 = st.selectbox("Select second component:", ["walls", "windows", "doors"])
    
    # Compare selected components
    data_1 = session["data"][component_1]
    data_2 = session["data"][component_2]
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
    ###  📁 Click on Browse File in the Side Bar to start
    """
    )

    ## Add File uploader to Side Bar Navigation
    st.sidebar.header('Model Loader')
    st.sidebar.file_uploader("Choose a file", type=['ifc'], key="uploaded_file", on_change=callback_upload)

    ## Add File Name and Success Message
    if "is_file_loaded" in session and session["is_file_loaded"]:
        st.sidebar.success(f'Project successfuly loaded')
        st.sidebar.write("🔃 You can reload a new file  ")
        
        # Add comparison section
        if "data" in session:
            st.sidebar.write("----")
            st.sidebar.header("Compare Components")
            compare_components()
            if session["comparison"] is not None:
                st.write(session["comparison"])
            
        # Add section to display data from IFC file
        st.sidebar.write("----")
        st.sidebar.header("IFC Data")
        data_to_display = st.sidebar.selectbox("Select component to display:", ["walls", "windows", "doors"])
        st.write(session["data"][data_to_display])
        
        # Add section to change project name
        col1, col2 = st.columns([2,1])
        col1.subheader(f'Start Exploring "{session["ifc_file"].by_type("IfcProject")[0].Name}"')
        col2.text_input("✏️ Change Project Name", key="project_name_input")
        col2.button("✔️ Apply", key="change_project_name", on_click=change_project_name())
        st.sidebar.write("""
--------------
### Credits:
#### Sigma Dimensions (TM)

Follow us [on Youtube](https://www.youtube.com/channel/UC9bPwuJZUD6ooKqzwdq9M9Q?sub_confirmation=1)

--------------
License: MIT

""")
st.write("")
st.sidebar.write("")
if name == "main":
    session = st.session_state
main()

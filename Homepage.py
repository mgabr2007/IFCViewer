import ifcopenshell
import streamlit as st

def callback_upload():
    st.session_state["file_name"] = st.session_state["uploaded_file"].name
    st.session_state["array_buffer"] = st.session_state["uploaded_file"].getvalue()
    st.session_state["ifc_file"] = ifcopenshell.file.from_string(st.session_state["array_buffer"].decode("utf-8"))
    st.session_state["is_file_loaded"] = True
    
    ### Empty Previous Model Data from Session State
    st.session_state["isHealthDataLoaded"] = False
    st.session_state["HealthData"] = {}
    st.session_state["Graphs"] = {}
    st.session_state["SequenceData"] = {}
    st.session_state["CostScheduleData"] = {}

    ### Empty Previous DataFrame from Session State
    st.session_state["DataFrame"] = None
    st.session_state["Classes"] = []
    st.session_state["IsDataFrameLoaded"] = False

def get_project_name():
    return st.session_state.ifc_file.by_type("IfcProject")[0].Name

def change_project_name():
    if st.session_state.project_name_input:
        st.session_state.ifc_file.by_type("IfcProject")[0].Name = st.session_state.project_name_input
        st.balloons()

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
    if "is_file_loaded" in st.session_state and st.session_state["is_file_loaded"]:
        st.sidebar.success(f'Project successfuly loaded')
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
    main()

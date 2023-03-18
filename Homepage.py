import ifcopenshell
import pyvista as pv
import streamlit as st

def visualize_geometry(file_path, lod_level):
    # Open the IFC file
    ifc_file = ifcopenshell.open(file_path)

    # Extract the geometry of all the building elements in the file
    building_elements = ifc_file.by_type("IfcBuildingElement")
    meshes = []
    for element in building_elements:
        geometry = ifcopenshell.geom.create_shape(settings=ifcopenshell.geom.settings(lod=lod_level), ifc_entity=element)
        if geometry:
            meshes.append(pv.PolyData(geometry.geometry))

    # Create a visualization and add the element meshes to it
    p = pv.Plotter()

    # Add the meshes to a LOD actor
    actor = pv.LODActor()
    for i, mesh in enumerate(meshes):
        actor.add_mesh(mesh, lod_resolution=i)

    p.add_actor(actor)
    return p

# Set up the Streamlit app
st.set_page_config(
    layout= "wide",
    page_title="IFC Stream",
    page_icon="✍️",
)
st.title("Streamlit IFC")

# Add File uploader to Side Bar Navigation
st.sidebar.header('Model Loader')
uploaded_file = st.sidebar.file_uploader("Choose a file", type=['ifc'], key="uploaded_file")

# Allow user to choose LOD level
if uploaded_file:
    lod_level = st.sidebar.slider("LOD Level", min_value=0, max_value=10, value=1, step=1)
    st.sidebar.success(f"LOD level set to {lod_level}")

# Load the IFC file and display the visualization
if uploaded_file:
    callback_upload()
    file_path = session["file_name"]
    p = visualize_geometry(file_path, lod_level)
    st.write(p.show())

def callback_upload():
    session["file_name"] = uploaded_file.name
    session["array_buffer"] = uploaded_file.getvalue()
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

def get_project_name():
    return session["ifc_file"].by_type("IfcProject")[0].Name

def change_project_name():
    if session["project_name_input"]:
        session["ifc_file"].by_type("IfcProject")[0].Name = session["project_name_input"]
        st.success('Project name successfully updated!')
        session["popup_shown"] = True

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

    ## Add File Name and Success Message
    if "is_file_loaded" in session and session["is_file_loaded"]:
        st.sidebar.success(f'Project successfuly loaded')
        st.sidebar.write("🔃 You can reload a new file  ")
            col1.subheader(f'Start Exploring "{get_project_name()}"')
            col2.text_input("✏️ Change Project Name", key="project_name_input")
            col2.button("✔️ Apply", key="change_project_name", on_click=change_project_name)

    if session["popup_shown"]:
        st.success('Project name successfully updated!')
        session["popup_shown"] = False

st.sidebar.write("""
--------------
""")
st.write("")
st.sidebar.write("")
if name == "main":
session = st.session_state
session["popup_shown"] = False
main()


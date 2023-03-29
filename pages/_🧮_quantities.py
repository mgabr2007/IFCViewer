import streamlit as st
from tools import graph_maker
from tools import ifchelper
from tools import pandashelper
import base64

session = st.session_state


def initialize_session_state():
    session["DataFrame"] = None
    session["Classes"] = []
    session["IsDataFrameLoaded"] = False


def load_data():
    if "ifc_file" in session:
        session["DataFrame"] = get_ifc_pandas()
        session.Classes = session.DataFrame["Class"].value_counts().keys().tolist()
        session["IsDataFrameLoaded"] = True


def get_ifc_pandas():
    data, pset_attributes = ifchelper.get_objects_data_by_class(
        session.ifc_file,
        "IfcBuildingElement"
    )
    frame = ifchelper.create_pandas_dataframe(data, pset_attributes)
    return frame


def download_csv():
    pandashelper.download_csv(session.file_name, session.DataFrame)


def download_excel():
    pandashelper.download_excel(session.file_name, session.DataFrame)


def download_filtered_csv():
    # Filter the DataFrame based on user input
    filtered_df = pandashelper.filter_dataframe_per_class(session.DataFrame, session.class_selector)
    filtered_df = pandashelper.get_quantities(filtered_df, session.qto_selector)

    # Generate a downloadable link for the CSV file
    csv_file = filtered_df.to_csv(index=False)
    b64 = base64.b64encode(csv_file.encode()).decode()
    button_label = f"Download {session.class_selector} - {session.qto_selector}.csv"
    href = f'<a href="data:file/csv;base64,{b64}" download="{session.class_selector} - {session.qto_selector}.csv"><button>{button_label}</button></a>'

    # Display the download button
    st.markdown(href, unsafe_allow_html=True)


def execute():
    st.set_page_config(
        page_title="Quantities",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.header(" 🧮 Model Quantities")
    if not "IsDataFrameLoaded" in session:
        initialize_session_state()
    if not session.IsDataFrameLoaded:
        load_data()
    if session.IsDataFrameLoaded:
        tab1, tab2 = st.tabs(["Dataframe Utilities", "Quantities Review"])
        with tab1:
            ## DATAFRAME REVIEW
            st.header("DataFrame Review")
            st.write(session.DataFrame)
            # from st_aggrid import AgGrid
            # AgGrid(session.DataFrame)
            st.button("Download CSV", key="download_csv", on_click=download_csv)
            st.button("Download Excel", key="download_excel", on_click=download_excel)
        with tab2:
            row2col1, row2col2 = st.columns(2)
            with row2col1:
                if session.IsDataFrameLoaded:
                    class_selector = st.selectbox("Select Class", session.Classes, key="class_selector")
                    session["filtered_frame"] = pandashelper.filter_dataframe_per_class(session.DataFrame,
                                                                                        session.class_selector)
                    session["qtos"] = pandashelper.get_qsets_columns(session["filtered_frame"])
                    if session["qtos"] is not None:
                        qto_selector = st.selectbox("Select Quantity Set", session.qtos, key='qto_selector')
                        quantities = pandashelper.get_quantities(session.filtered_frame, session.qto_selector)
                        st.selectbox("Select Quantity", quantities, key="quantity_selector")
                        st.radio('Split per', ['Level', 'Type'], key="split_options")
                        st.button("Download Filtered CSV", key="download_filtered_csv", on_click=download_filtered_csv)
                else:
                    st.warning("No Quantities to Look at !")
        ## DRAW FRAME
        with row2col2:
            if "quantity_selector" in session and session.quantity_selector == "Count":
                total = pandashelper.get_total(session.filtered_frame)
                st.write(f"The total number of {session.class_selector} is {total}")
            else:
                if session.qtos is not None:
                    st.subheader(f"{session.class_selector} {session.quantity_selector}")
                    graph = graph_maker.load_graph(
                        session.filtered_frame,
                        session.qto_selector,
                        session.quantity_selector,
                        session.split_options,
                    )
                    st.plotly_chart(graph)
else:
    st.header("Step 1: Load a file from the Home Page")

execute()

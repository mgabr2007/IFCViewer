# windows_info.py
import streamlit as st
import ifcopenshell

def get_windows_info(ifc_file):
    windows = ifc_file.by_type("IfcWindow")
    windows_info = []

    for window in windows:
        window_data = {
            "GlobalId": window.GlobalId,
            "Name": window.Name,
            "ObjectType": window.ObjectType,
            "OverallHeight": window.OverallHeight,
            "OverallWidth": window.OverallWidth
        }
        windows_info.append(window_data)

    return windows_info

def windows_info_page(ifc_file):
    st.title("Windows Information")

    if ifc_file:
        windows_info = get_windows_info(ifc_file)
        if windows_info:
            st.write("Windows found in the IFC file:")
            st.table(windows_info)
        else:
            st.warning("No windows found in the IFC file.")
    else:
        st.error("No IFC file loaded. Please load an IFC file to view windows information.")

# pages/windows_info.py
import streamlit as st
import pandas as pd

def get_windows_info(ifc_file):
    windows = ifc_file.by_type("IfcWindow")
    windows_info = []

    for window in windows:
        info = {
            "GlobalId": window.GlobalId,
            "Name": window.Name,
            "ObjectType": window.ObjectType,
            "OverallWidth": window.OverallWidth,
            "OverallHeight": window.OverallHeight,
        }
        windows_info.append(info)

    return windows_info

def windows_info_page(ifc_file):
    if ifc_file:
        windows_info = get_windows_info(ifc_file)
        if windows_info:
            st.write("Windows found in the IFC file:")
            df_windows_info = pd.DataFrame(windows_info)
            st.write(df_windows_info)
        else:
            st.warning("No windows found in the IFC file.")
    else:
        st.error("No IFC file loaded. Please load an IFC file to view windows information.")

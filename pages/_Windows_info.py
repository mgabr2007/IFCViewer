# pages/windows_info.py
import streamlit as st
import pandas as pd

# Define a function to extract window information from an IFC file
def get_windows_info(ifc_file):
    windows = ifc_file.by_type("IfcWindow")
    windows_info = []

    for window in windows:
        info = {
            "Name": window.Name,
            "OverallWidth": window.OverallWidth,
            "OverallHeight": window.OverallHeight,
            "Location": window.ObjectPlacement.RelativePlacement.Location.Coordinates if window.ObjectPlacement.RelativePlacement.Location else None,
            "Elevation": window.ObjectPlacement.RelativePlacement.RefDirection.DirectionRatios if window.ObjectPlacement.RelativePlacement.RefDirection else None,
            "Orientation": window.ObjectPlacement.RelativePlacement.PlacementRelTo.RelativePlacement.RefDirection.DirectionRatios if window.ObjectPlacement.RelativePlacement.PlacementRelTo and window.ObjectPlacement.RelativePlacement.PlacementRelTo.RelativePlacement.RefDirection else None,
            "Zone": window.ContainedInStructure.Name if window.ContainedInStructure else None,
            "Area": window.OverallHeight * window.OverallWidth if window.OverallHeight and window.OverallWidth else None
        }
        windows_info.append(info)

    return windows_info

def windows_info_page(ifc_file):
    if ifc_file:
        windows_info = get_windows_info(ifc_file)
        if windows_info:
            st.write("Windows found in the IFC file:")
            df_windows_props = pd.DataFrame(windows_info, columns=["GlobalId", "ConstructionType", "FrameDepth", "GlazingType", "OperationType", "SoundReductionIndex", "OverallWidth", "OverallHeight", "Area", "Location", "Elevation", "Orientation", "Zone"])
            st.write(df_windows_props)
        else:
            st.warning("No windows found in the IFC file.")
    else:
        st.error("No IFC file loaded. Please load an IFC file to view windows information.")

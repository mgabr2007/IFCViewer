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
            "ConstructionType": window.ConstructionType.Name if window.ConstructionType else None,
            "FrameDepth": window.FrameDepth,
            "GlazingType": window.GlazingType.Name if window.GlazingType else None,
            "OperationType": window.OperationType.Name if window.OperationType else None,
            "SoundReductionIndex": window.SoundReductionIndex,
            "OverallWidth": window.OverallWidth,
            "OverallHeight": window.OverallHeight,
            "Location": window.ObjectPlacement.RelativePlacement.Location.Coordinates if window.ObjectPlacement.RelativePlacement.Location else None,
            "Elevation": window.ObjectPlacement.RelativePlacement.RefDirection.DirectionRatios if window.ObjectPlacement.RelativePlacement.RefDirection else None,
            "Orientation": window.ObjectPlacement.RelativePlacement.PlacementRelTo.RelativePlacement.RefDirection.DirectionRatios if window.ObjectPlacement.RelativePlacement.PlacementRelTo and window.ObjectPlacement.RelativePlacement.PlacementRelTo.RelativePlacement.RefDirection else None,
            "Zone": window.ContainedInStructure.Name if window.ContainedInStructure else None
        }
        windows_info.append(info)

    return windows_info

def windows_info_page(ifc_file):
    if ifc_file:
        windows_info = get_windows_info(ifc_file)
        if windows_info:
            st.write("Windows found in the IFC file:")
            df_windows_props = pd.DataFrame(windows_info, columns=["GlobalId", "Name", "ObjectType", "ConstructionType", "FrameDepth", "GlazingType", "OperationType", "SoundReductionIndex", "OverallWidth", "OverallHeight", "Area", "UValue", "SHGC"])
            st.write(df_windows_props)
            df_windows_location = pd.DataFrame(windows_info, columns=["GlobalId", "Name", "Location", "Elevation", "Orientation", "Zone"])
            st.write(df_windows_location)
        else:
            st.warning("No windows found in the IFC file.")
    else:
        st.error("No IFC file loaded. Please load an IFC file to view windows information.")

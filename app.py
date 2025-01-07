import streamlit as st
import pandas as pd
from processed import processing
from agency_days import processing_agency_days_and_hours
# Title and description
st.title("FBCENC Data Processing")
st.write("""
Upload a CSV file, and it will be merged with a **pre-loaded reference file** for processing.
""")

# Load the static reference file
static_file_path = "FBCENC_Geo_2.csv"  # Replace with your file path
try:
    ref_df = pd.read_csv(static_file_path)
    st.write("### Reference File Preview:")
    st.write(ref_df.head())
except Exception as e:
    st.error(f"Error loading the static file: {e}")
    st.stop()

# File upload for the main dataset
uploaded_file = st.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file:
    # Read the uploaded file
    new_df = pd.read_csv(uploaded_file)

       

    out = processing(new_df)
    
    # Merge the uploaded file with the static file
    #merged_df = pd.merge(out, ref_df, on=key, how="inner")  # Default inner join
    final_df = out.merge(ref_df[['Latitude','Longitude','No.']], on="No.", how="left")
    # Example processing (modify this part as needed)
    #merged_df['Processed'] = merged_df.iloc[:, 1] * 2  # Example logic - replace with your own

    # Display the processed data
    st.write("### Merged and Processed Data Preview:")
    st.write(final_df.head())

    # Download button for the processed file
    st.download_button(
        label="Download Processed File For PowerBI",
        data=final_df.to_csv(index=False).encode('utf-8'),
        file_name="PowerBI_Input_file.csv",
        mime="text/csv"
    )

    # Second Processing Method
    st.write("### Processing Method 2")
    out2 = processing_agency_days_and_hours(new_df)
    #final_df2 = out2.merge(ref_df[['Latitude', 'Longitude', 'No.']], on="No.", how="inner")

    # Display the second processed output
    st.write("#### Processed Data (Method 2):")
    st.write(out2.head())

    # Download button for Method 2 output
    st.download_button(
        label="Download Processed File for Agency days and hours",
        data=out2.to_csv(index=False).encode('utf-8'),
        file_name="processed_file_agency_days.csv",
        mime="text/csv"
    )


else:
    st.info("Please upload a CSV file to continue.")

import streamlit as st
import pandas as pd
from processed import processing

# Title and description
st.title("File Processing and Merging App")
st.write("""
Upload a CSV file, and it will be merged with a **pre-loaded reference file** for processing.
""")

# Load the static reference file
static_file_path = static_file_path = "FBCENC_Geo_2.csv"

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
    final_df = out.merge(ref_df[['Latitude','Longitude','No.']], on="No.", how="inner")
    # Example processing (modify this part as needed)
    #merged_df['Processed'] = merged_df.iloc[:, 1] * 2  # Example logic - replace with your own

    # Display the processed data
    st.write("### Merged and Processed Data Preview:")
    st.write(final_df.head())

    # Download button for the processed file
    st.download_button(
        label="Download Processed File",
        data=final_df.to_csv(index=False).encode('utf-8'),
        file_name="processed_file.csv",
        mime="text/csv"
    )
else:
    st.info("Please upload a CSV file to continue.")

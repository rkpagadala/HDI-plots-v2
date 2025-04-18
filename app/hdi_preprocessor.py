# pyright: reportMissingModuleSource=false
import pandas as pd
import os

# Path constants
ROOT = "datasets/"
HDI_PATH = ROOT + "human-development-index.csv"
PROCESSED_HDI_PATH = ROOT + "processed_hdi.csv"

def preprocess_hdi_data():
    """
    Preprocess the HDI data to match the format of other datasets.
    
    This function:
    1. Reads the raw HDI data
    2. Renames columns to match the format of other datasets
    3. Pivots the data to have countries as rows and years as columns
    4. Saves the preprocessed data to a temporary file
    
    Returns:
        str: Path to the processed HDI data file
    """
    hdi_df = pd.read_csv(HDI_PATH)
    
    # Rename columns to match the format of other datasets
    hdi_df = hdi_df.rename(columns={"Entity": "Country", "Human Development Index": "HDI"})
    
    # Pivot the data to have countries as rows and years as columns
    pivoted_df = hdi_df.pivot(index="Country", columns="Year", values="HDI")
    
    # Reset index to make Country a column again
    pivoted_df.reset_index(inplace=True)
    
    # Save the preprocessed data to a temporary file
    pivoted_df.to_csv(PROCESSED_HDI_PATH, index=False)
    
    return PROCESSED_HDI_PATH

def get_hdi_data_for_country(country, years):
    """
    Get HDI data for a specific country within a year range.
    
    Args:
        country (str): The country name
        years (list): A list containing the start and end years [start_year, end_year]
        
    Returns:
        DataFrame: A DataFrame with 'x' (years) and 'y' (HDI values) columns, or None if data not available
    """
    # Check if processed HDI file exists, if not create it
    if not os.path.exists(PROCESSED_HDI_PATH):
        preprocess_hdi_data()
    
    df = pd.read_csv(PROCESSED_HDI_PATH)
    df = df[df["Country"] == country]
    
    if len(df) == 0:
        return None
        
    df = df.drop(["Country"], axis=1)
    # Convert column names to integers for filtering
    df.columns = df.columns.astype(int)
    
    # Filter columns by year range
    selected_columns = [year for year in range(years[0], years[1] + 1) if year in df.columns]
    if not selected_columns:  # If no columns match the year range
        return None
        
    df = df[selected_columns]
    df = df.dropna(axis=1)
    df = df.T
    df.reset_index(inplace=True)
    
    df.columns = ["x", "y"]
    df["x"] = df["x"].astype(int)
    
    if (df["y"].dtype == "object"):
        df["y"] = df["y"].astype(float)
    return df

def get_hdi_data_for_save_csv(selected_countries):
    """
    Get HDI data for multiple countries for saving to CSV.
    
    Args:
        selected_countries (list): List of country names
        
    Returns:
        DataFrame: A DataFrame with HDI data for the selected countries
    """
    # Check if processed HDI file exists, if not create it
    if not os.path.exists(PROCESSED_HDI_PATH):
        preprocess_hdi_data()
    
    df = pd.read_csv(PROCESSED_HDI_PATH)
    return df[df["Country"].isin(selected_countries)]


def get_hdi_data_for_state(state):
    """
    Handle HDI data requests for Indian states.
    Since HDI data for Indian states is not available, this function returns None
    to gracefully handle the case when HDI is selected for Indian states.
    
    Args:
        state (str): The state name
        
    Returns:
        None: Always returns None as HDI data for Indian states is not available
    """
    # HDI data for Indian states is not available
    return None

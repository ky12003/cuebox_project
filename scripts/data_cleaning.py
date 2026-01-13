########
# IMPORTS
########
from email_validator import validate_email, EmailNotValidError
import requests
import pandas as pd



############
# MAIN FUNCTIONS
############
"""
Overview:
Creates multiple dataframes based on a list of spreadsheet names

Parameters:
- spreadsheet_names (str[]): List of spreadsheet names (for extraction)

Returns:
- df_list (df[]): List of dataframes containing data from the specified spreadsheets
"""
def make_dfs(spreadsheet_names):
    print("IMPORTING DATAFRAMES....")
    df_list = []
    for sheet in spreadsheet_names:
        df = pd.read_csv(sheet)
        df_list.append(df)
    print("DATAFRAMES IMPORTED!")
    return df_list
    

"""
Overview:
Cleans the data from the "Constituents" subsheet

Parameters:
- const_df (df): Original "Constituents" dataframe

Returns:
- const_df (df): Cleaned dataframe
"""
def constituents_processing(const_df):
    ##########
    # Drop invalid rows from df
    ##########
    print("PROCESSING CONSTITUENTS....")
    
    # RULE 2: Drop rows w/out company OR first/last name
    const_df = const_df[const_df['First Name'].notna() & const_df['Company'].notna()]
    
    # RULE 3: Drop rows with empty "Date Entered" timestamp
    const_df = const_df.dropna(subset=['Date Entered'])
    const_df['Date Entered'] = const_df['Date Entered'].apply(format_date)
    
    # Clean and standardize data
    # Rule 2: Capitalize first letter of name
    const_df['First Name'] = const_df['First Name'].str.title()
    const_df['Last Name'] = const_df['Last Name'].str.title()
    const_df['Company'] = const_df['Company'].str.title()
    

    ##########
    # Add background info
    ##########
    # Rule 10: Add background info column (Job Title + Marital Status)
    marital_status = []
    for sal, mar in zip(const_df["Salutation"], const_df["Gender"]):
        if (sal == "Mrs" or sal == "Mr" or sal == "Mr. and Mrs.") or mar == "Married":
            marital_status.append("Married")
        else: 
            marital_status.append(mar)

    const_df["Marital Status"] = marital_status
    
    background_info = []
    for job, mar in zip(const_df["Title"], const_df["Marital Status"]):
        info = ""
        if pd.notna(job):
            info += job
        if pd.notna(mar):
            if info:
                info += " ; "
            info += mar
        background_info.append(info)

    const_df["Background Info"] = background_info
    
    print("CONSTITUENTS DATA CLEANED!")
    return const_df

"""
Overview:
Cleans/formats the data from the "" subsheet

Parameters:
- const_df (df): Original "Constituents" dataframe

Returns:
- const_df (df): Cleaned dataframe
"""

###########
# HELPER FUNCTIONS
###########
# Format datetime to "Month DD, YYYY" format
def format_date(date_val):
    if pd.isna(date_val):
        return None
    try:
        # Convert to datetime if it's not already
        if isinstance(date_val, str):
            date_obj = pd.to_datetime(date_val)
        else:
            date_obj = pd.to_datetime(date_val)
        
        # Format as "Month DD, YYYY"
        return date_obj.strftime("%B %d, %Y")
    except:
        return None
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
    const_df = const_df[const_df['First Name'].notna() | const_df['Company'].notna()]
    
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
    
    # Create Constituent Type column
    const_df['Constituent Type'] = const_df.apply(
        lambda row: 'Person' if pd.notna(row['First Name']) else 'Company' if pd.notna(row['Company']) else '', 
        axis=1
    )
    
    print("CONSTITUENTS DATA CLEANED!")
    return const_df

"""
Overview:
Cleans/formats the data from the "Donation History" subsheet

Parameters:
- donations_df (df): Original "Donation History" dataframe

Returns:
- donations_df (df): Cleaned dataframe
"""
def donation_history_processing(donations_df):
    print("PROCESSING DONATION HISTORY....")
    ##########
    # Removing Refunds -> Grouping
    ##########
    # Remove refunded donations
    donations_df = donations_df[donations_df['Status'] != 'Refund']

    # Group by "Patron ID" + get lifetime/most recent donation info
    donations_df = donations_df.groupby('Patron ID').agg({
        'Donation Amount': ['sum', 'max'],  # sum for total, max for most recent
        'Donation Date': 'max'
    }).reset_index()
    
    # Flatten the multi-level column names and rename appropriately
    donations_df.columns = ['Patron ID', 'Donation Amount Tot', 'Donation Amount Recent', 'Donation Date']

    

    ##########
    # Formatting
    ##########
    # Convert to numeric first, then format donation amounts to currency standard
    donations_df['Donation Amount Tot'] = pd.to_numeric(donations_df['Donation Amount Tot'], errors='coerce')
    donations_df['Donation Amount Tot'] = donations_df['Donation Amount Tot'].apply(lambda x: "${:.2f}".format(x) if pd.notna(x) else "")
    
    donations_df['Donation Amount Recent'] = pd.to_numeric(donations_df['Donation Amount Recent'], errors='coerce')
    donations_df['Donation Amount Recent'] = donations_df['Donation Amount Recent'].apply(lambda x: "${:.2f}".format(x) if pd.notna(x) else "")
    
    # Format "Donation Date" to "Month DD, YYYY"
    donations_df['Donation Date'] = donations_df['Donation Date'].apply(format_date)

    print("DONATION HISTORY DATA CLEANED!")
    return donations_df

"""
Overview:
Clean & group primary/secondary emails

Parameters:
- const_df_clean (df): Cleaned "Constituents" dataframe
- emails_df (df): Original "Emails" dataframe

Returns:
- const_df_clean (df): Updated "Constituents" dataframe with primary/secondary emails
"""
def emails_processing(const_df_clean, emails_df):
    print("PROCESSING EMAILS....")
    ##########
    # Validate Emails
    ##########
    primary_emails = []
    secondary_emails = []

    # Get all possible secondary emails
    grouped_emails = emails_df.groupby('Patron ID')['Email'].apply(list).reset_index()
    
    # Make map for id -> list of possible secondary emails
    email_map = dict(zip(grouped_emails['Patron ID'], grouped_emails['Email']))


    # Process each primary email + corresponding id + secondary email (if applicable)
    for idx, row in const_df_clean.iterrows():
        curr_main = ""
        curr_sec = ""
        
        # Validate primary email from constituents dataframe
        email_main = row['Primary Email']
        if email_main:
            try:
                valid = validate_email(str(email_main).strip())
                curr_main = valid.email
            except EmailNotValidError:
                curr_main = ""

        # Get potential secondary emails
        constituent_id = row['Patron ID']
        secondary_email_list = email_map.get(constituent_id, [])
        
        # Validate all secondary emails and filter valid ones
        valid_secondary_emails = []
        for sec_email in secondary_email_list:
            if sec_email:
                try:
                    valid = validate_email(str(sec_email).strip())
                    valid_email = valid.email
                    # Validity check (duplicates vs primary & existing secondaries)
                    if valid_email != curr_main and valid_email not in valid_secondary_emails:
                        valid_secondary_emails.append(valid_email)
                except EmailNotValidError:
                    continue
        
        # Pick the first valid secondary email (if any)
        if valid_secondary_emails:
            curr_sec = valid_secondary_emails[0]
        
        # Start assigning primary/secondary emails
        if curr_main:
            primary_emails.append(curr_main)
            secondary_emails.append(curr_sec)
        elif curr_sec:
            # If no valid primary but we have valid secondary, promote secondary to primary
            primary_emails.append(curr_sec)
            secondary_emails.append("")
        else:
            primary_emails.append("")
            secondary_emails.append("")

    const_df_clean['Primary Email'] = primary_emails
    const_df_clean['Secondary Email'] = secondary_emails

    print("EMAILS DATA CLEANED!")
    return const_df_clean

"""
Overview:
Cleans/maps the Tags column using the provided API

Parameters:
- const_df_clean (df): Cleaned "Constituents" dataframe with Tags column

Returns:
- const_df_clean (df): Updated "Constituents" dataframe with mapped tag names
"""
def tags_processing(const_df_clean):
    print("PROCESSING TAGS....")
    
    # Fetch tag mappings from API
    try:
        response = requests.get("https://6719768f7fc4c5ff8f4d84f1.mockapi.io/api/v1/tags")
        tag_data = response.json()
        
        # Create mapping dictionary: original name -> mapped name
        tag_mapping = {}
        for tag in tag_data:
            tag_mapping[tag['name']] = tag['mapped_name']
        
    except Exception as e:
        print(f"Error fetching tag mappings: {e}")
        print("Proceeding without tag mapping...")
        tag_mapping = {}
    
    
    # Apply tag mapping to the Tags column
    const_df_clean['Tags'] = const_df_clean['Tags'].apply(lambda x: map_tags(x, tag_mapping))
    
    print("TAGS DATA CLEANED!")
    return const_df_clean

"""
Overview:
Gets individual tags and counts from final_df for output sheet

Parameters:
- final_df (df): Cleaned "Constituents" dataframe with Tags column

Returns:
- tags_df (df): Dataframe with individual tags and their counts
"""
def extract_tags(final_df):
    print("EXTRACTING TAGS....")
    # Get all tags as individual rows
    tags = final_df.explode('Tags')
    tags_df = pd.DataFrame(tags).groupby('Tags').size().reset_index(name='Count')

    print("TAGS EXTRACTED!")
    return tags_df

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
    
# Function to map tags using the fetched tag_mapping
def map_tags(tag_list, tag_mapping= None):
    if pd.isna(tag_list) or not tag_list:
        return []
    
    # Handle both string and list inputs
    if isinstance(tag_list, str):
        # If it's a string, split by comma or other delimiter
        tags = [tag.strip() for tag in tag_list.split(',')]
    else:
        tags = tag_list
    
    # Map each tag to its mapped name or keep original if no mapping exists
    mapped_tags = []
    for tag in tags:
        if tag in tag_mapping:
            mapped_tags.append(tag_mapping[tag])
        else:
            mapped_tags.append(tag)  # Keep original if no mapping found
    
    return mapped_tags
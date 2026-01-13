import data_cleaning
import pandas as pd

# Step 1: import dataframes (layer 1)
spreadsheet_paths = ["data/constituents.csv", "data/emails.csv","data/donation_history.csv"]
df_list = data_cleaning.make_dfs(spreadsheet_paths)
constituents_df = df_list[0]
emails_df = df_list[1]
donations_df = df_list[2]


# Step 2: clean dataframes (layer 2)
constituents_df = data_cleaning.constituents_processing(constituents_df) # constituents cleaning
print("Length after constituents cleaning: ", len(constituents_df))
constituents_df = data_cleaning.emails_processing(constituents_df, emails_df) # email cleaning/merging
print("Length after emails cleaning: ", len(constituents_df))
donations_df = data_cleaning.donation_history_processing(donations_df) # donations cleaning/merging
print("Length after donations cleaning: ", len(donations_df))
constituents_df = data_cleaning.tags_processing(constituents_df) # clean tags using API

# Step 3: merge dataframes (layer 3)
final_df = pd.merge(constituents_df, donations_df, on="Patron ID", how="left")
print(final_df.head()[['Patron ID', 'First Name', 'Last Name', 'Primary Email', 'Secondary Email', 'Donation Amount Tot']])

# Step 4: export final dataframes (layer 4)
# Output 1 (constituents)
name_map = {
    "CB Constituent ID": "Patron ID",
    "CB Constituent Type": "Constituent Type",
    "CB First Name": "First Name",
    "CB Last Name": "Last Name",
    "CB Company Name": "Company Name",
    "CB Created At": "Date Entered",
    "CB Email 1 (Standardized)": "Primary Email",
    "CB Email 2 (Standardized)": "Secondary Email",
    "CB Title": "Title",
    "CB Tags": "Tags",
    "CB Background Information": "Background Information",
    "CB Lifetime Donation Amount": "Donation Amount Tot",
    "CB Most Recent Donation Date": "Donation Amount Date",
    "CB Most Recent Donation Amount": "Donation Amount Recent"
}

final_df_renamed = final_df.rename(columns=name_map)
final_df_renamed.to_csv("data/CB_Constituents.csv", index=False)


# Ouput 2 (tags)
tags_df = data_cleaning.extract_tags(final_df)
tags_map = {
    "CB Tag Name": "Tags",
    "CB Tag Count": "Count"
}
tags_df_renamed = tags_df.rename(columns=tags_map)
tags_df_renamed.to_csv("data/CB_Tags.csv", index=False)
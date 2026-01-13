import data_cleaning

# Step 1: import dataframes (layer 1)
spreadsheet_paths = ["data/constituents.csv", "data/emails.csv","data/donation_history.csv"]
df_list = data_cleaning.make_dfs(spreadsheet_paths)
constituents_df = df_list[0]
emails_df = df_list[1]
donations_df = df_list[2]


# Step 2: clean/combine dataframes (layer 2)
constituents_df = data_cleaning.constituents_processing(constituents_df)


# Step 3: export final dataframes (layer 3)
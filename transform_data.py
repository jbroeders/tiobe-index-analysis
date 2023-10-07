import os
import pandas as pd

def transform_data():
    # Define the path to the 'data' subfolder
    data_dir = os.path.join(os.getcwd(), 'data')

    # Initialize an empty list to store the dataframes
    all_dataframes = []

    # Iterate over the directories corresponding to the years
    year_dirs = ['2020', '2021', '2022', '2023']
    for year in year_dirs:
        year_dir_path = os.path.join(data_dir, year)
        for file in os.listdir(year_dir_path):
            if file.endswith(".csv"):
                file_path = os.path.join(year_dir_path, file)
                df = pd.read_csv(file_path)
                df['Year'] = int(year)  # Add the 'Year' column
                all_dataframes.append(df)

    # Concatenate all the dataframes
    combined_df = pd.concat(all_dataframes, ignore_index=True)

    # Melt the dataframe to a long format
    melted_df = combined_df.melt(id_vars=['Year', 'Programming Language'], 
                                 value_vars=[col for col in combined_df.columns if col not in ['Year', 'Programming Language']],
                                 var_name='Month', 
                                 value_name='Rating')

    # Pivot the dataframe to the desired wide format
    reshaped_df = melted_df.pivot_table(index=['Year', 'Month'], 
                                        columns='Programming Language', 
                                        values='Rating').reset_index()

    # Address inconsistencies in column names
    reshaped_df['Assembly Language'] = reshaped_df['Assembly Language'].combine_first(reshaped_df.get('Assembly Langauge', None))
    if 'Assembly Langauge' in reshaped_df.columns:
        reshaped_df.drop('Assembly Langauge', axis=1, inplace=True)

    # Save the cleaned and reshaped dataframe to a CSV file in the main project folder
    reshaped_csv_path = os.path.join(os.getcwd(), "tiobe_index_ratings_2020-2023.csv")
    reshaped_df.to_csv(reshaped_csv_path, index=False)
    print(f"Data reshaped and saved to {reshaped_csv_path}")

if __name__ == "__main__":
    transform_data()

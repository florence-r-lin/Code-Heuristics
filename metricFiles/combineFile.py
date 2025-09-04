import pandas as pd
import os

# combine csv files by year into one csv file

def combineFile(directory, output):

    years = range(2018, 2026)
    combined_df = pd.DataFrame()

    for year in years:
        filename = f'Metrics Score {year}.csv'
        filepath = os.path.join(directory, filename)

        if os.path.exists(filepath):
            df = pd.read_csv(filepath)
            combined_df = pd.concat([combined_df, df], ignore_index=True)
        else:
            print(f'File {filename} not found')

    combined_df.to_csv(output, index=False)

directory = '/Users/summer-2024/Desktop/code metrics 25/Code-Heuristics/'
output = '/Users/summer-2024/Desktop/code metrics 25/Code-Heuristics/metricFiles/Metrics Score 2018-2025.csv'

combineFile(directory, output)


# round data in csv file by column

def roundData(csvPath, columns, decimals):
    df = pd.read_csv(csvPath)

    for column in columns:
        if column in df.columns:
            df[column] = pd.to_numeric(df[column], errors='coerce').round(decimals)
        else:
            print(f'Column {column} not found in the CSV.')

    df.to_csv(csvPath, index=False)

columns = ['Comment Percentage', 'Execution Time']

roundData(output, columns, 3)
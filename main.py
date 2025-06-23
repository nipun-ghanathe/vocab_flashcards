import csv

import pandas as pd

# Converting the excel file to csv using pandas **(I should not do this and instead work with pandas)**
excel_file = "input_files/my-word-list.xlsx"
df = pd.read_excel(excel_file)  # noqa: PD901
df.to_csv("output_files/my-word-list.csv", index=False)


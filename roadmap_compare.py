import pandas as pd

df_1 = pd.read_csv("csv_outputs/dc_cards_2022-02-23.csv")
df_2 = pd.read_csv("csv_outputs/dc_cards_2021-12-16.csv")

# output the dataframe

print(df_1.head(5))
print(df_2.head(5))
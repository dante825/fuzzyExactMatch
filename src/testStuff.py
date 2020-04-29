from fuzzywuzzy import fuzz, process
import pandas as pd

# print(fuzz.partial_token_set_ratio('FOO GHE KOH', 'KOH FOO GHE'))
# print(fuzz.token_sort_ratio('FOO GHE KOH', 'KOH FOO GHE'))

dir_df = pd.read_csv("../input/exchgDirectorName-test.csv")
dir_sub_df = dir_df[dir_df["director_name"]=='KOH FOO GHE']

print(dir_sub_df)
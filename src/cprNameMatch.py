import logging
import os
import re
import time
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz, process

# logging.basicConfig(filename='../log/cpr.log',
#                     filemode='w', format='%(asctime)s, %(levelname)s, %(message)s',
#                     level=logging.INFO)

logging.basicConfig(level=logging.INFO)

input_file = '../input/cpr.csv'
output_file = '../output/cprMatched.csv'


def exact_match():
    """Exact match the name in the list

    Do the exact matching first.
    :return:
    """
    cpr_df = pd.read_csv(input_file)
    print('cpr df shape: {}'.format(cpr_df.shape))

    cpr_df["pp_fullname"] = cpr_df["pp_fullname"].apply(string_cleansing)
    distinct_id_df = cpr_df.drop_duplicates(subset=["cpr_person_id"])
    print('distinct_id_df shape: {}'.format(distinct_id_df.shape))

    distinct_names = cpr_df["pp_fullname"].unique()

    logging.info('Exact matching...')

    exact_df = pd.DataFrame()
    # exact_list = []
    for name in distinct_names:
        matched_df = distinct_id_df[distinct_id_df["pp_fullname"] == name]
        if matched_df.shape[0] > 1:
            exact_df = exact_df.append(matched_df)
    exact_df.to_csv(output_file, index=False)


# def fuzz_match():
#     del_files(output_file)
#     entity_list = read_entity(entity_file)
#     entity_df = pd.read_csv(input_csv)
#
#     entity_df[var_to_match] = entity_df[var_to_match].apply(string_cleansing)
#     entity_df = entity_df.sort_values(by=var_to_match)
#     entity_list = [string_cleansing(x) for x in entity_list]
#     logging.info('Fuzzy matching...')
#
#     fuzz_df = pd.DataFrame()
#     fuzz_list = []
#     for index, row in entity_df.iterrows():
#         if index % 10 == 0:
#             logging.info("Processing row %d" % index)
#         name_to_match = row[var_to_match]
#         for entity_str in entity_list:
#             if fuzz.ratio(name_to_match, entity_str) > fuzz_threshold:
#                 fuzz_df = fuzz_df.append(row)
#                 fuzz_list.append(entity_str)
#
#     fuzz_df['fuzz_entity'] = fuzz_list
#     fuzz_df.to_csv(output_file, index=False)


def string_cleansing(string):
    string = string.lower().strip()
    string = re.sub('[^A-Za-z0-9]+', ' ', string)
    string = re.sub('\\s+', ' ', string)
    return string


def main():
    start = time.time()
    exact_match()
    # fuzz_match()
    logging.info("Total time taken: %.2f seconds" % (time.time() - start))


if __name__ == "__main__":
    main()
"""
Name matching on the institutions profile to remove duplicates

SQL:
select wvb_institution_id, dbt_entity_id, external_id, institution_type,
regexp_replace(regexp_replace(regexp_replace(institution_name, ',', '', 'g'), ';', '', 'g'), '\t', '', 'g'),
regexp_replace(regexp_replace(regexp_replace(reported_institution_name, ',', '', 'g'), ';', '', 'g'), '\t', '', 'g'),
country_of_source, country_of_incorporation from dibots_v2.institution_profile;
"""
import logging
import os
import re
import time
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz, process

logging.basicConfig(format='%(asctime)s, %(levelname)s, %(message)s',
                    level=logging.INFO)

inst_file = '../input/inst.csv'
output_file = '../output/instExactMatched.csv'


def exact_match():
    inst_df = pd.read_csv(inst_file);
    logging.info('inst_df shape:{}'.format(inst_df.shape))

    inst_df = inst_df.dropna()
    logging.info('inst_df after dropna shape:{}'.format(inst_df.shape))

    inst_df['institution_name'] = inst_df['institution_name'].apply(string_cleansing)

    distinct_names = inst_df['institution_name'].unique()

    logging.info('Exact_matching...')

    exact_df = pd.DataFrame()
    count = 0
    for unq_name in distinct_names:
        if count % 100 == 0:
            logging.info('Processing row %d', count)
        count += 1
        matched_df = inst_df[inst_df['institution_name'] == unq_name]
        if matched_df.shape[0] > 1:
            exact_df = exact_df.append(matched_df)

    exact_df.to_csv(output_file, index=False);


def string_cleansing(string):
    string = string.lower().strip()
    string = re.sub('[^A-Za-z0-9]+', ' ', string)
    string = re.sub('\\s+', ' ', string)
    return string


def main():
    start = time.time()
    exact_match()
    logging.info("Total time taken: %.2f seconds" % (time.time() - start))


if __name__ == '__main__':
    main()

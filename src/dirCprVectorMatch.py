import logging
import os
import re
import time
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz, process

# LOG_FILE = "../logs/sancpersfuzzy.out"
#
# my_logger = logging.getLogger("fuzzyLogger")
# my_logger.setLevel(logging.INFO)
# handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=200000, backupCount=10)
# bf = logging.Formatter('{asctime} {name} {levelname:8s} {message}', style='{')
# handler.setFormatter(bf)
# my_logger.addHandler(handler)
#
# Usage: my_logger.info('<message> {}'.format(<something>))

logging.basicConfig(level=logging.INFO)

cpr_input_file = '../input/compPersRole.csv'
dir_input_file = '../input/exchgDirectorName.csv'
output_file = '../output/dirFuzzMatched2.csv'


def vectorized_fuzzy():
    cpr_df = pd.read_csv(cpr_input_file)
    dir_df = pd.read_csv(dir_input_file)
    cpr_df["fullname"] = cpr_df["fullname"].apply(string_cleansing)
    dir_df["director_name"] = dir_df["director_name"].apply(string_cleansing)

    logging.info("cpr_df input shape: {}".format(cpr_df.shape))
    # cpr_df[match_col].replace('', np.nan, inplace=True)
    # cpr_df = cpr_df.dropna()
    # my_logger.info("Pers_df input shape after empty names are dropped: {}".format(cpr_df.shape))

    logging.info("dir_df input shape: {}".format(dir_df.shape))
    # dir_df[match_col].replace('', np.nan, inplace=True)
    # dir_df = dir_df.dropna()
    # my_logger.info("Sanc_df input shape after empty names are dropped: {}".format(dir_df.shape))

    # dir_comp_id_list = dir_df.company_id.tolist()
    # dir_name_list = dir_df.director_name.tolist()

    v_fuzz_func = np.vectorize(fuzzy_partial_match)
    counter = 0
    fuzz_df = pd.DataFrame()
    for idx, row in cpr_df.iterrows():
        if counter % 100 == 0:
            logging.info("Processing row %d", counter)
        counter += 1

        cpr_pers_name = row["fullname"]
        cpr_comp_id = row['company_id']
        cpr_pers_id = row['person_id']

        dir_sub_df = dir_df[dir_df["company_id"] == cpr_comp_id]
        dir_sub_id_list = dir_sub_df.id.tolist()
        dir_sub_comp_list = dir_sub_df.company_id.tolist()
        dir_sub_name_list = dir_sub_df.director_name.tolist()

        if len(dir_sub_name_list) != 0 and len(cpr_pers_name) != 0:
            score_list = v_fuzz_func(dir_sub_name_list, cpr_pers_name)
            cpr_pers_id_list = [cpr_pers_id] * len(score_list)
            cpr_pers_name_list = [cpr_pers_name] * len(score_list)
            tmp_df = pd.DataFrame(list(zip(dir_sub_id_list, dir_sub_comp_list, dir_sub_name_list, cpr_pers_id_list, cpr_pers_name_list, score_list)),
                                  columns=['id', 'company_id', 'director_name','person_id', 'person_name', 'fuzzy_score'])
            tmp_df = tmp_df[tmp_df["fuzzy_score"] >= 90]
            fuzz_df = fuzz_df.append(tmp_df)

            # Partial output to file
            if fuzz_df.shape[0] > 100:
                if not os.path.isfile(output_file):
                    fuzz_df.to_csv(output_file, header=fuzz_df.columns, index=False)
                else:
                    fuzz_df.to_csv(output_file, mode='a', header=False, index=False)
                fuzz_df = pd.DataFrame()

    if not os.path.isfile(output_file):
        fuzz_df.to_csv(output_file, header=fuzz_df.columns, index=False)
    else:
        fuzz_df.to_csv(output_file, mode='a', header=False, index=False)

    # Output at the end of the process
    # output_filename = output_file + time.strftime("%Y%m%d%H%M%S") + ".csv"
    # fuzz_df.to_csv(output_filename, index=False)


def string_cleansing(string):
    string = string.lower().strip()
    string = re.sub('[^A-Za-z0-9]+', ' ', string)
    string = re.sub('\\s+', ' ', string)
    return string


def fuzzy_partial_match(x: str, y: str) -> int:
    simple_ratio = fuzz.ratio(x, y)
    token_ratio = fuzz.token_sort_ratio(x, y)

    if token_ratio >= simple_ratio:
        return token_ratio
    else:
        return simple_ratio


def main():
    start = time.time()
    # exact_match()
    vectorized_fuzzy()
    logging.info("Total time taken: %.2f seconds" % (time.time() - start))


if __name__ == "__main__":
    main()
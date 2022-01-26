# -*- coding:utf-8 -*-
import pprint
import json
import pandas as pd

pp = pprint.PrettyPrinter(indent=2)


def main():
    csv_path = 'D:/train/COMP3074-CW1-Dataset.csv'
    df = pd.read_csv(csv_path)          # read csv to pd.DataFrame
    target_list = []

    for index, info in df.iterrows():
        target_list = target_list+[{'label': info.Document,'question':[info.Question],'answer': [info.Answer]}]

    target_dict={'qandas':target_list}
    pp.pprint(target_dict)

    with open('./output.json', 'w') as fp:
        json.dump(target_dict, fp, indent=2)


if __name__ == "__main__":
    main()
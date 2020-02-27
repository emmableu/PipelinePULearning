import json
import os
import pandas as pd

import sys
sys.path.append('my_module')
from save_load_pickle import *
from sklearn.model_selection import train_test_split
from word2idx import *
word2idx = load_obj('word2idx', '.', 'Data')
print('word2idx')
print(word2idx)
idx2word = {idx+1: w for (idx, w) in enumerate(word2idx)}
print('idx2word')
print(idx2word)
def get_code_shape_count(project_vector): #returns one-hot count
    code_shape_count = []
    for idx in range(1, 170):
        try:
            code_shape_count.append(project_vector.count(idx2word[idx]))
        except:
            code_shape_count.append(0)

    return code_shape_count


def get_data_table(folder_name):
    root_path = os.getcwd()
    file_path = root_path + ("/Data/Unlabeled-SB3JsonFiles/" + folder_name)
    file_list = os.listdir(file_path)
    df_data = pd.DataFrame(columns = ['projectID', 'code'])
    for file_name in file_list:
        with open(file_path + '/' + file_name, 'r') as project:  ##  "with" is Python's crash resistant file open
            if file_name.split(".")[1] != "json":
                continue
            print("file_name: ", file_name)
            try:
                json_obj = json.load(project)
            except:
                continue
            project_vector = []
            try:
                project_vector = get_project_vector(json_obj, project_vector)
                code_shape_count = get_code_shape_count(project_vector)
            except:
                continue

            project_id = file_name.split(".")[0]
            code = code_shape_count
            new_record = {
                'projectID': project_id,
                'code': code
            }
            df_data.loc[len(df_data)] = new_record
    df_data = df_data.sort_values(by=['projectID']).reset_index(drop=True)
    save_obj(df_data, 'unlabeled_games_one_hot_count', 'Data', "UnLabeled-SB3JsonFiles/pre_process" + folder_name)




get_data_table('games')

# games = load_obj( 'unlabeled_games_one_hot_count', 'Data', "UnLabeled-SB3JsonFiles/pre_processgames")
# p_ID1000 = games['projectID'].unique()[:1000]
# def random_sample_1000(data):
#     return data[data['projectID'].isin(p_ID1000)]

# games = random_sample_1000(games)
# # metadata = random_sample_1000(metadata)
# save_obj(games, 'unlabeled_games_one_hot_count', 'Data', "UnLabeled-SB3JsonFiles/pre_process-games1000")

import json
import os
import pandas as pd
import sys
sys.path.append('my_module')
from save_load_pickle import *


def get_project_vector(json_obj, project_vector):
    target_obj_s = json_obj['targets']
    for target_obj in target_obj_s:
        if target_obj['isStage']:
            project_vector.append('Stage')
            block_s = target_obj['blocks']
            for block in block_s:
                project_vector.append(block_s[block]['opcode'])
        else:
            project_vector.append('Sprite')
            block_s = target_obj['blocks']
            for block in block_s:
                project_vector.append(block_s[block]['opcode'])

    return (project_vector)
def get_indexing_data():

    root_path = os.getcwd()
    file_path = root_path + ("/Data/UnLabeled-SB3JsonFiles/games")
    file_list = os.listdir(file_path)

    print("Starting tuning json files into project vector:")
    data = pd.DataFrame(columns = ['projectID', 'code'])
    #adapted from snapinator: https://github.com/djsrv/snapinator/blob/master/src/objects/Stage.tsx
    df_data = pd.DataFrame(columns=['projectID', 'code'])
    vocabulary = []

    i = 0
    for file_name in file_list:
        i = i + 1
        # if i == 1000:
        #     break
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
            except:
                continue

            project_id = file_name.split(".")[0]
            for token in project_vector:
                if token not in vocabulary:
                    vocabulary.append(token)
            new_record = {
                'projectID': project_id,
                'code': project_vector
            }
            df_data.loc[len(df_data)] = new_record

    save_obj(df_data, 'all_games_word', "Data/UnLabeled-SB3JsonFiles", 'all_games_word')
    word2idx = {w: idx+1 for (idx, w) in enumerate(vocabulary)}
    idx2word = {idx+1: w for (idx, w) in enumerate(vocabulary)}
    #
    save_obj(word2idx, 'word2idx', '.', 'Data')
    save_obj(idx2word, 'idx2word', '.', 'Data')

o = load_obj('all_games_word', "Data/UnLabeled-SB3JsonFiles", 'all_games_word')


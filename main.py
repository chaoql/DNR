from getData import download_extract, seeData
from pathlib import Path
import pickle
from dataProcessor import load_data, saveData

if __name__ == '__main__':

    # 下载数据
    dataPath = Path("./ml-1m")
    if not dataPath.exists():
        data_dir = './'
        download_extract('ml-1m', data_dir)

    # seeData()  # 查看数据
    # 数据与处理并保存
    if not Path("./processed_data/preprocess.pkl").exists():
        title_count, title_set, genres2int, features, targets_values, \
        ratings, users, movies, data, movies_orig, users_orig = load_data()
        saveData(title_count, title_set, genres2int, features, targets_values, ratings, users, movies, data,
                 movies_orig, users_orig)
    with open('./processed_data/preprocess.pkl', mode='rb') as f:
        title_count, title_set, genres2int, features, targets_values, ratings, users, movies, data, \
        movies_orig, users_orig = pickle.load(f)

    print(users.head())
    print('end')

from getRawData import download_extract
from helper import seeRawData, saveProcessedData, save_params, load_params
from pathlib import Path
from dataProcessor import load_data
from train import train


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
        saveProcessedData(title_count, title_set, genres2int, features, targets_values, ratings, users, movies, data,
                          movies_orig, users_orig)
    if not Path("./runs").exists():
        train()
    save_dir = './save'
    save_params(save_dir)
    load_dir = load_params()
    print('end')

from pathlib import Path
from common.libs.DLHelper.getRawData import download_extract
from common.libs.DLHelper.helper import seeRawData, saveProcessedData, save_params, load_params
from flask_script import Command
from common.libs.DLHelper.dataProcessor import load_data
from model.train import train
import var
from recommend import recommend_same_type_movie, recommend_your_favorite_movie, recommend_other_favorite_movie
from saveFeature import saveMovieFeature, saveUserFeature


class seeRawData_(Command):
    def run(self, *args, **kwargs):
        seeRawData()


class downloadData(Command):
    def run(self):
        flag = 0
        dataPath = Path("./ml-1m")
        if not dataPath.exists():
            data_dir = './'
            download_extract('ml-1m', data_dir)
            flag = 1
        if flag == 1:
            print("数据已保存...")
        else:
            print("数据已存在...")


class dataProcessSave(Command):
    def run(self):
        if not Path("./processed_data/preprocess.pkl").exists():
            title_count, title_set, genres2int, features, targets_values, ratings, users, movies, data, movies_orig, \
            users_orig = load_data()
            saveProcessedData(title_count, title_set, genres2int, features, targets_values, ratings, users, movies,
                              data,
                              movies_orig, users_orig)


class paramsSave(Command):
    def run(self):
        if not Path("./runs").exists():
            losses = train()
            save_params(var.save_dir)
            load_dir = load_params()


class saveFeature(Command):
    def run(self):
        if not Path("./save/movie_matrics.p").exists():
            saveMovieFeature()
        if not Path("./save/users_matrics.p").exists():
            saveUserFeature()
        print(recommend_same_type_movie(1401, 20))
        print(recommend_your_favorite_movie(234, 10))
        print(recommend_other_favorite_movie(1401, 20))
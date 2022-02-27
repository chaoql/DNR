import os
import pickle
import pandas as pd
import tensorflow.compat.v1 as tf
from config import *


def seeRawData():
    print("\n------------ users -------------")
    users_title = ['UserID', 'Gender', 'Age', 'OccupationID', 'Zip-code']
    users = pd.read_table('./ml-1m/users.dat', sep='::', header=None, names=users_title, engine='python')
    print(users.head())

    print("\n------------ movies -------------")
    movies_title = ['MovieID', 'Title', 'Genres']
    movies = pd.read_table('./ml-1m/movies.dat', sep='::', header=None, names=movies_title, engine='python',
                           encoding="ISO-8859-1")
    print(movies.head())

    print("\n------------ ratings -------------")
    ratings_title = ['UserID', 'MovieID', 'Rating', 'timestamps']
    ratings = pd.read_table('./ml-1m/ratings.dat', sep='::', header=None, names=ratings_title, engine='python')
    print(ratings.head())


def save_params(params):
    """
    Save parameters to file
    """
    with open('params.p', 'wb') as f:
        pickle.dump(params, f)


def load_params():
    """
    Load parameters from file
    """
    with open('params.p', mode='rb') as f:
        return pickle.load(f)


def saveProcessedData(title_count, title_set, genres2int, features, targets_values, ratings, users, movies, data,
                      movies_orig, users_orig):
    with open('./processed_data/preprocess.pkl', 'wb') as f:
        pickle.dump((title_count,
                     title_set,
                     genres2int,
                     features,
                     targets_values,
                     ratings,
                     users,
                     movies,
                     data,
                     movies_orig,
                     users_orig),
                    f)


def getProcessedData():
    with open('./processed_data/preprocess.pkl', mode='rb') as f:
        title_count, title_set, genres2int, features, targets_values, ratings, users, movies, data, \
        movies_orig, users_orig = pickle.load(f)
    return title_count, title_set, genres2int, features, targets_values, ratings, users, movies, data, \
           movies_orig, users_orig


def get_inputs():
    uid = tf.placeholder(tf.int32, [None, 1], name="uid")
    user_gender = tf.placeholder(tf.int32, [None, 1], name="user_gender")
    user_age = tf.placeholder(tf.int32, [None, 1], name="user_age")
    user_job = tf.placeholder(tf.int32, [None, 1], name="user_job")

    movie_id = tf.placeholder(tf.int32, [None, 1], name="movie_id")
    # 电影种类中要去除<PAD>，所以-1
    movie_categories = tf.placeholder(tf.int32, [None, movie_categories_max - 1], name="movie_categories")
    movie_titles = tf.placeholder(tf.int32, [None, 15], name="movie_titles")
    targets = tf.placeholder(tf.int32, [None, 1], name="targets")
    LearningRate = tf.placeholder(tf.float32, name="LearningRate")
    dropout_keep_prob = tf.placeholder(tf.float32, name="dropout_keep_prob")
    return uid, user_gender, user_age, user_job, movie_id, movie_categories, movie_titles, targets, LearningRate, dropout_keep_prob


def get_tensors(loaded_graph):
    uid = loaded_graph.get_tensor_by_name("uid:0")
    user_gender = loaded_graph.get_tensor_by_name("user_gender:0")
    user_age = loaded_graph.get_tensor_by_name("user_age:0")
    user_job = loaded_graph.get_tensor_by_name("user_job:0")
    movie_id = loaded_graph.get_tensor_by_name("movie_id:0")
    movie_categories = loaded_graph.get_tensor_by_name("movie_categories:0")
    movie_titles = loaded_graph.get_tensor_by_name("movie_titles:0")
    targets = loaded_graph.get_tensor_by_name("targets:0")
    dropout_keep_prob = loaded_graph.get_tensor_by_name("dropout_keep_prob:0")
    lr = loaded_graph.get_tensor_by_name("LearningRate:0")
    # 两种不同计算预测评分的方案使用不同的name获取tensor inference
    # inference = loaded_graph.get_tensor_by_name("inference/inference/BiasAdd:0")
    inference = loaded_graph.get_tensor_by_name(
        "inference/ExpandDims:0")  # 之前是MatMul:0 因为inference代码修改了 这里也要修改 感谢网友 @清歌 指出问题
    movie_combine_layer_flat = loaded_graph.get_tensor_by_name("movie_fc/Reshape:0")
    user_combine_layer_flat = loaded_graph.get_tensor_by_name("user_fc/Reshape:0")
    return uid, user_gender, user_age, user_job, movie_id, movie_categories, movie_titles, targets, lr, dropout_keep_prob, inference, movie_combine_layer_flat, user_combine_layer_flat

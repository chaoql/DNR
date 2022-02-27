import tensorflow.compat.v1 as tf
import numpy as np
from dataProcessor import load_data
import config as cg
from helper import get_tensors
from helper import load_params


def rating_movie(user_id_val, movie_id_val, load_dir=load_params()):
    title_count, title_set, genres2int, features, targets_values, \
    ratings, users, movies, data, movies_orig, users_orig = load_data()
    loaded_graph = tf.Graph()  #
    with tf.Session(graph=loaded_graph) as sess:  #
        # Load saved model
        loader = tf.train.import_meta_graph(load_dir + '.meta')
        loader.restore(sess, load_dir)

        # Get Tensors from loaded model
        uid, user_gender, user_age, user_job, movie_id, movie_categories, movie_titles, targets, lr, dropout_keep_prob, inference, _, __ = get_tensors(
            loaded_graph)  # loaded_graph

        categories = np.zeros([1, 18])
        categories[0] = movies.values[cg.movieid2idx[movie_id_val]][2]

        titles = np.zeros([1, cg.sentences_size])
        titles[0] = movies.values[cg.movieid2idx[movie_id_val]][1]

        feed = {
            uid: np.reshape(users.values[user_id_val - 1][0], [1, 1]),
            user_gender: np.reshape(users.values[user_id_val - 1][1], [1, 1]),
            user_age: np.reshape(users.values[user_id_val - 1][2], [1, 1]),
            user_job: np.reshape(users.values[user_id_val - 1][3], [1, 1]),
            movie_id: np.reshape(movies.values[cg.movieid2idx[movie_id_val]][0], [1, 1]),
            movie_categories: categories,  # x.take(6,1)
            movie_titles: titles,  # x.take(5,1)
            dropout_keep_prob: 1}

        # Get Prediction
        inference_val = sess.run([inference], feed)
        return (inference_val)

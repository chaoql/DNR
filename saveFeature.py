import pickle
import numpy as np
import tensorflow.compat.v1 as tf
from Helper.helper import load_params, get_tensors
import var


def saveMovieFeature():
    load_dir = load_params()
    loaded_graph = tf.Graph()  #
    movie_matrics = []
    with tf.Session(graph=loaded_graph) as sess:  #
        # Load saved model
        loader = tf.train.import_meta_graph(load_dir + '.meta')
        loader.restore(sess, load_dir)

        # Get Tensors from loaded model
        uid, user_gender, user_age, user_job, movie_id, movie_categories, movie_titles, targets, lr, dropout_keep_prob, _, movie_combine_layer_flat, __ = get_tensors(
            loaded_graph)  # loaded_graph

        for item in var.movies.values:
            categories = np.zeros([1, 18])
            categories[0] = item.take(2)

            titles = np.zeros([1, var.sentences_size])
            titles[0] = item.take(1)

            feed = {
                movie_id: np.reshape(item.take(0), [1, 1]),
                movie_categories: categories,  # x.take(6,1)
                movie_titles: titles,  # x.take(5,1)
                dropout_keep_prob: 1}

            movie_combine_layer_flat_val = sess.run([movie_combine_layer_flat], feed)
            movie_matrics.append(movie_combine_layer_flat_val)

    pickle.dump((np.array(movie_matrics).reshape(-1, 200)), open('./save/movie_matrics.p', 'wb'))


def saveUserFeature():
    load_dir = load_params()
    loaded_graph = tf.Graph()  #
    users_matrics = []
    with tf.Session(graph=loaded_graph) as sess:  #
        # Load saved model
        loader = tf.train.import_meta_graph(load_dir + '.meta')
        loader.restore(sess, load_dir)

        # Get Tensors from loaded model
        uid, user_gender, user_age, user_job, movie_id, movie_categories, movie_titles, targets, lr, dropout_keep_prob, _, __, user_combine_layer_flat = get_tensors(
            loaded_graph)  # loaded_graph

        for item in var.users.values:
            feed = {
                uid: np.reshape(item.take(0), [1, 1]),
                user_gender: np.reshape(item.take(1), [1, 1]),
                user_age: np.reshape(item.take(2), [1, 1]),
                user_job: np.reshape(item.take(3), [1, 1]),
                dropout_keep_prob: 1}

            user_combine_layer_flat_val = sess.run([user_combine_layer_flat], feed)
            users_matrics.append(user_combine_layer_flat_val)

    pickle.dump((np.array(users_matrics).reshape(-1, 200)), open('./save/users_matrics.p', 'wb'))
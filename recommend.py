import pickle
import random
import tensorflow.compat.v1 as tf
import numpy as np
from Helper.helper import load_params
import config as cg


def recommend_print(sim, top_k, str="以下是给您的推荐："):
    print(str)
    p = np.squeeze(sim)
    p[np.argsort(p)[:-top_k]] = 0
    p = p / np.sum(p)
    results = set()
    while len(results) != 5:
        c = np.random.choice(3883, 1, p=p)[0]
        results.add(c)
    for val in (results):
        print(val)
        print(cg.movies_orig[val])

    return results


def recommend_same_type_movie(movie_id_val, top_k=20):
    """
    思路是计算当前看的电影特征向量与整个电影特征矩阵的余弦相似度，取相似度
    最大的top_k个，这里加了些随机选择在里面，保证每次的推荐稍稍有些不同。
    :param movie_id_val:
    :param top_k:
    :return:
    """
    movie_matrics = pickle.load(open('./save/movie_matrics.p', mode='rb'))
    load_dir = load_params()
    loaded_graph = tf.Graph()  #
    with tf.Session(graph=loaded_graph) as sess:  #
        # Load saved model
        loader = tf.train.import_meta_graph(load_dir + '.meta')
        loader.restore(sess, load_dir)

        norm_movie_matrics = tf.sqrt(tf.reduce_sum(tf.square(movie_matrics), 1, keep_dims=True))
        normalized_movie_matrics = movie_matrics / norm_movie_matrics

        # 推荐同类型的电影
        probs_embeddings = (movie_matrics[cg.movieid2idx[movie_id_val]]).reshape([1, 200])
        probs_similarity = tf.matmul(probs_embeddings, tf.transpose(normalized_movie_matrics))
        sim = (probs_similarity.eval())
        #     results = (-sim[0]).argsort()[0:top_k]
        #     print(results)

        print("您看的电影是：{}".format(cg.movies_orig[cg.movieid2idx[movie_id_val]]))
        recommend_print(sim, top_k, "以下是给您的推荐：")


def recommend_your_favorite_movie(user_id_val, top_k=10):
    """
    思路是使用用户特征向量与电影特征矩阵计算所有电影的评分，取评分最高的top_k个，同样加了些随机选择部分。
    :param user_id_val:
    :param top_k:
    :return:
    """
    movie_matrics = pickle.load(open('./save/movie_matrics.p', mode='rb'))
    users_matrics = pickle.load(open('./save/users_matrics.p', mode='rb'))
    load_dir = load_params()
    loaded_graph = tf.Graph()  #
    with tf.Session(graph=loaded_graph) as sess:  #
        # Load saved model
        loader = tf.train.import_meta_graph(load_dir + '.meta')
        loader.restore(sess, load_dir)

        # 推荐您喜欢的电影
        probs_embeddings = (users_matrics[user_id_val - 1]).reshape([1, 200])

        probs_similarity = tf.matmul(probs_embeddings, tf.transpose(movie_matrics))
        sim = (probs_similarity.eval())
    recommend_print(sim, top_k, "以下是给您的推荐：")


def recommend_other_favorite_movie(movie_id_val, top_k=20):
    """
    1. 首先选出喜欢某个电影的top_k个人，得到这几个人的用户特征向量。
    2. 然后计算这几个人对所有电影的评分
    3. 选择每个人评分最高的电影作为推荐
    4. 同样加入了随机选择
    :param movie_id_val:
    :param top_k:
    :return:
    """
    movie_matrics = pickle.load(open('./save/movie_matrics.p', mode='rb'))
    users_matrics = pickle.load(open('./save/users_matrics.p', mode='rb'))
    load_dir = load_params()
    loaded_graph = tf.Graph()  #
    with tf.Session(graph=loaded_graph) as sess:  #
        # Load saved model
        loader = tf.train.import_meta_graph(load_dir + '.meta')
        loader.restore(sess, load_dir)

        probs_movie_embeddings = (movie_matrics[cg.movieid2idx[movie_id_val]]).reshape([1, 200])
        probs_user_favorite_similarity = tf.matmul(probs_movie_embeddings, tf.transpose(users_matrics))
        favorite_user_id = np.argsort(probs_user_favorite_similarity.eval())[0][-top_k:]
        #     print(normalized_users_matrics.eval().shape)
        #     print(probs_user_favorite_similarity.eval()[0][favorite_user_id])
        #     print(favorite_user_id.shape)

        print("您看的电影是：{}".format(cg.movies_orig[cg.movieid2idx[movie_id_val]]))
        print("喜欢看这个电影的人是：{}".format(cg.users_orig[favorite_user_id - 1]))
        probs_users_embeddings = (users_matrics[favorite_user_id - 1]).reshape([-1, 200])
        probs_similarity = tf.matmul(probs_users_embeddings, tf.transpose(movie_matrics))
        sim = (probs_similarity.eval())
        p = np.argmax(sim, 1)
        print("喜欢看这个电影的人还喜欢看：")
        results = set()
        while len(results) != 5:
            c = p[random.randrange(top_k)]
            results.add(c)
        for val in (results):
            print(val)
            print(cg.movies_orig[val])
        return results

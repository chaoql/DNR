import pickle
from sklearn.model_selection import train_test_split
from Helper.helper import get_inputs
from model.model import get_user_embedding, get_user_feature_layer, get_movie_feature_layer, get_movie_cnn_layer, \
    get_movie_id_embed_layer, get_movie_categories_layers
import numpy as np
import time
import datetime
import os
import tensorflow.compat.v1 as tf
import config as cg


tf.reset_default_graph()
tf.disable_v2_behavior()


def get_batches(Xs, ys, batch_size):
    """
    自定义获取 batch 的方法
    :param Xs:
    :param ys:
    :param batch_size:
    :return:
    """
    for start in range(0, len(Xs), batch_size):
        end = min(start + batch_size, len(Xs))
        yield Xs[start:end], ys[start:end]


def train():
    with open('../processed_data/preprocess.pkl', mode='rb') as f:
        title_count, title_set, genres2int, features, targets_values, ratings, users, movies, data, \
        movies_orig, users_orig = pickle.load(f)

    # reset_default_graph 操作应该在 tensorflow 的其他所有操作之前进行，否则将会出现不可知的问题
    # tensorflow 中的 graph 包含的是一系列的操作和使用到这些操作的 tensor
    train_graph = tf.Graph()
    # Graph 只是当前线程的属性，如果想要在其他的线程使用这个 Graph，那么就要像下面这样指定
    # 下面的 with 语句将 train_graph 设置为当前线程的默认 graph
    with train_graph.as_default():
        # 获取输入占位符
        uid, user_gender, user_age, user_job, \
        movie_id, movie_categories, movie_titles, \
        targets, lr, dropout_keep_prob = get_inputs()
        # 获取User的4个嵌入向量
        uid_embed_layer, gender_embed_layer, age_embed_layer, job_embed_layer = get_user_embedding(uid, user_gender,
                                                                                                   user_age, user_job)
        # 得到用户特征
        user_combine_layer, user_combine_layer_flat = get_user_feature_layer(uid_embed_layer, gender_embed_layer,
                                                                             age_embed_layer, job_embed_layer)
        # 获取电影ID的嵌入向量
        movie_id_embed_layer = get_movie_id_embed_layer(movie_id)
        # 获取电影类型的嵌入向量
        movie_categories_embed_layer = get_movie_categories_layers(movie_categories)
        # 获取电影名的特征向量
        pool_layer_flat, dropout_layer = get_movie_cnn_layer(movie_titles, dropout_keep_prob)
        # 得到电影特征
        movie_combine_layer, movie_combine_layer_flat = get_movie_feature_layer(movie_id_embed_layer,
                                                                                movie_categories_embed_layer,
                                                                                dropout_layer)
        # 计算出评分，要注意两个不同的方案，inference的名字（name值）是不一样的，后面做推荐时要根据name取得tensor
        # tensorflow 的 name_scope 指定了 tensor 范围，方便我们后面调用，通过指定 name_scope 来调用其中的 tensor
        with tf.name_scope("inference"):
            # 直接将用户特征矩阵和电影特征矩阵相乘得到得分，最后要做的就是对这个得分进行回归
            inference = tf.reduce_sum(user_combine_layer_flat * movie_combine_layer_flat, axis=1)
            inference = tf.expand_dims(inference, axis=1)

        with tf.name_scope("loss"):
            # MSE损失，将计算值回归到评分
            cost = tf.losses.mean_squared_error(targets, inference)
            # 将每个维度的 cost 相加，计算它们的平均值
            loss = tf.reduce_mean(cost)
        # 优化损失
        #     train_op = tf.train.AdamOptimizer(lr).minimize(loss)  #cost
        # 在为 tensorflow 设置 name 参数的时候，是为了能在 graph 中看到什么变量进行了什么操作
        global_step = tf.Variable(0, name="global_step", trainable=False)
        #     optimizer = tf.train.AdamOptimizer(lr)
        optimizer = tf.train.AdamOptimizer()
        gradients = optimizer.compute_gradients(loss)  # cost
        train_op = optimizer.apply_gradients(gradients, global_step=global_step)

    losses = {'train': [], 'test': []}
    with tf.Session(graph=train_graph) as sess:
        # 搜集数据给tensorBoard用
        # Keep track of gradient values and sparsity
        grad_summaries = []
        for g, v in gradients:
            if g is not None:
                grad_hist_summary = tf.summary.histogram("{}/grad/hist".format(v.name.replace(':', '_')), g)
                # tf.nn.zero_fraction 用于计算矩阵中 0 所占的比重，也就是计算矩阵的稀疏程度
                sparsity_summary = tf.summary.scalar("{}/grad/sparsity".format(v.name.replace(':', '_')),
                                                     tf.nn.zero_fraction(g))
                grad_summaries.append(grad_hist_summary)
                grad_summaries.append(sparsity_summary)
        grad_summaries_merged = tf.summary.merge(grad_summaries)

        # Output directory for models and summaries
        timestamp = str(int(time.time()))
        out_dir = os.path.abspath(os.path.join(os.path.curdir, "../runs", timestamp))
        print("Writing to {}\n".format(out_dir))

        # Summaries for loss and accuracy
        loss_summary = tf.summary.scalar("loss", loss)

        # Train Summaries
        train_summary_op = tf.summary.merge([loss_summary, grad_summaries_merged])
        train_summary_dir = os.path.join(out_dir, "summaries", "train")
        train_summary_writer = tf.summary.FileWriter(train_summary_dir, sess.graph)

        # Inference summaries
        inference_summary_op = tf.summary.merge([loss_summary])
        inference_summary_dir = os.path.join(out_dir, "summaries", "inference")
        inference_summary_writer = tf.summary.FileWriter(inference_summary_dir, sess.graph)

        sess.run(tf.global_variables_initializer())
        saver = tf.train.Saver()
        for epoch_i in range(cg.num_epochs):

            # 将数据集分成训练集和测试集，随机种子不固定
            train_X, test_X, train_y, test_y = train_test_split(features,
                                                                targets_values,
                                                                test_size=0.2,
                                                                random_state=0)

            train_batches = get_batches(train_X, train_y, cg.batch_size)
            test_batches = get_batches(test_X, test_y, cg.batch_size)

            # 训练的迭代，保存训练损失
            for batch_i in range(len(train_X) // cg.batch_size):
                x, y = next(train_batches)

                categories = np.zeros([cg.batch_size, 18])
                for i in range(cg.batch_size):
                    categories[i] = x.take(6, 1)[i]

                titles = np.zeros([cg.batch_size, cg.sentences_size])
                for i in range(cg.batch_size):
                    titles[i] = x.take(5, 1)[i]

                feed = {
                    uid: np.reshape(x.take(0, 1), [cg.batch_size, 1]),
                    user_gender: np.reshape(x.take(2, 1), [cg.batch_size, 1]),
                    user_age: np.reshape(x.take(3, 1), [cg.batch_size, 1]),
                    user_job: np.reshape(x.take(4, 1), [cg.batch_size, 1]),
                    movie_id: np.reshape(x.take(1, 1), [cg.batch_size, 1]),
                    movie_categories: categories,  # x.take(6,1)
                    movie_titles: titles,  # x.take(5,1)
                    targets: np.reshape(y, [cg.batch_size, 1]),
                    dropout_keep_prob: cg.dropout_keep,  # dropout_keep
                    lr: cg.learning_rate}

                step, train_loss, summaries, _ = sess.run([global_step, loss, train_summary_op, train_op], feed)  # cost
                losses['train'].append(train_loss)
                train_summary_writer.add_summary(summaries, step)  #

                # Show every <show_every_n_batches> batches
                if batch_i % cg.show_every_n_batches == 0:
                    time_str = datetime.datetime.now().isoformat()
                    print('{}: Epoch {:>3} Batch {:>4}/{}   train_loss = {:.3f}'.format(
                        time_str,
                        epoch_i,
                        batch_i,
                        (len(train_X) // cg.batch_size),
                        train_loss))

            # 使用测试数据的迭代
            for batch_i in range(len(test_X) // cg.batch_size):
                x, y = next(test_batches)

                categories = np.zeros([cg.batch_size, 18])
                for i in range(cg.batch_size):
                    categories[i] = x.take(6, 1)[i]

                titles = np.zeros([cg.batch_size, cg.sentences_size])
                for i in range(cg.batch_size):
                    titles[i] = x.take(5, 1)[i]

                feed = {
                    uid: np.reshape(x.take(0, 1), [cg.batch_size, 1]),
                    user_gender: np.reshape(x.take(2, 1), [cg.batch_size, 1]),
                    user_age: np.reshape(x.take(3, 1), [cg.batch_size, 1]),
                    user_job: np.reshape(x.take(4, 1), [cg.batch_size, 1]),
                    movie_id: np.reshape(x.take(1, 1), [cg.batch_size, 1]),
                    movie_categories: categories,  # x.take(6,1)
                    movie_titles: titles,  # x.take(5,1)
                    targets: np.reshape(y, [cg.batch_size, 1]),
                    dropout_keep_prob: 1,
                    lr: cg.learning_rate}

                step, test_loss, summaries = sess.run([global_step, loss, inference_summary_op], feed)  # cost

                # 保存测试损失
                losses['test'].append(test_loss)
                inference_summary_writer.add_summary(summaries, step)  #

                time_str = datetime.datetime.now().isoformat()
                if batch_i % cg.show_every_n_batches == 0:
                    print('{}: Epoch {:>3} Batch {:>4}/{}   test_loss = {:.3f}'.format(
                        time_str,
                        epoch_i,
                        batch_i,
                        (len(test_X) // cg.batch_size),
                        test_loss))

        # Save Model
        saver.save(sess, cg.save_dir)  # , global_step=epoch_i
        print('Model Trained and Saved')
        return losses

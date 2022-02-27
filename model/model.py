import tensorflow.compat.v1 as tf
from config import *


# 从上面的网络架构图中，我们可以看出，其实用户的特征总数量是 128
# 但是作者在下面的代码中并没有这样做，而是由的特征设置为了 16，这样可能是因为作者的电脑性能比较差
# 我们先尝试这样的设置，如果计算资源允许，我们在后面再次测试的时候全部设置为 32


def get_user_embedding(uid, user_gender, user_age, user_job):
    with tf.name_scope("user_embedding"):
        # 下面的操作和情感分析项目中的单词转换为词向量的操作本质上是一样的
        # 用户的特征维度设置为 32
        # 先初始化一个非常大的用户矩阵
        # tf.random_uniform 的第二个参数是初始化的最小值，这里是-1，第三个参数是初始化的最大值，这里是1
        uid_embed_matrix = tf.Variable(tf.random_uniform([uid_max, embed_dim], -1, 1),
                                       name="uid_embed_matrix")
        # 根据指定用户ID找到他对应的嵌入层
        uid_embed_layer = tf.nn.embedding_lookup(uid_embed_matrix, uid,
                                                 name="uid_embed_layer")

        # 性别的特征维度设置为 16
        #         gender_embed_matrix = tf.Variable(tf.random_uniform([gender_max, embed_dim // 2], -1, 1),
        #                                           name= "gender_embed_matrix")
        gender_embed_matrix = tf.Variable(tf.random_uniform([gender_max, embed_dim], -1, 1),
                                          name="gender_embed_matrix")
        gender_embed_layer = tf.nn.embedding_lookup(gender_embed_matrix, user_gender,
                                                    name="gender_embed_layer")

        # 年龄的特征维度设置为 16
        #         age_embed_matrix = tf.Variable(tf.random_uniform([age_max, embed_dim // 2], -1, 1),
        #                                        name="age_embed_matrix")
        age_embed_matrix = tf.Variable(tf.random_uniform([age_max, embed_dim], -1, 1),
                                       name="age_embed_matrix")
        age_embed_layer = tf.nn.embedding_lookup(age_embed_matrix, user_age,
                                                 name="age_embed_layer")

        # 职业的特征维度设置为 16
        #         job_embed_matrix = tf.Variable(tf.random_uniform([job_max, embed_dim // 2], -1, 1),
        #                                        name = "job_embed_matrix")
        job_embed_matrix = tf.Variable(tf.random_uniform([job_max, embed_dim], -1, 1),
                                       name="job_embed_matrix")
        job_embed_layer = tf.nn.embedding_lookup(job_embed_matrix, user_job,
                                                 name="job_embed_layer")
    # 返回产生的用户数据数据
    return uid_embed_layer, gender_embed_layer, age_embed_layer, job_embed_layer


def get_user_feature_layer(uid_embed_layer, gender_embed_layer, age_embed_layer, job_embed_layer):
    with tf.name_scope("user_fc"):
        # 第一层全连接
        # tf.layers.dense 的第一个参数是输入，第二个参数是层的单元的数量
        uid_fc_layer = tf.layers.dense(uid_embed_layer, embed_dim, name="uid_fc_layer", activation=tf.nn.relu)
        gender_fc_layer = tf.layers.dense(gender_embed_layer, embed_dim, name="gender_fc_layer", activation=tf.nn.relu)
        age_fc_layer = tf.layers.dense(age_embed_layer, embed_dim, name="age_fc_layer", activation=tf.nn.relu)
        job_fc_layer = tf.layers.dense(job_embed_layer, embed_dim, name="job_fc_layer", activation=tf.nn.relu)

        # 第二层全连接
        # 将上面的每个分段组成一个完整的全连接层
        user_combine_layer = tf.concat([uid_fc_layer, gender_fc_layer, age_fc_layer, job_fc_layer], 2)  # (?, 1, 128)
        # 验证上面产生的 tensorflow 是否是 128 维度的
        print(user_combine_layer.shape)
        # tf.contrib.layers.fully_connected 的第一个参数是输入，第二个参数是输出
        # 这里的输入是user_combine_layer，输出是200，是指每个用户有200个特征
        # # 相当于是一个200个分类的问题，每个分类的可能性都会输出，在这里指的就是每个特征的可能性
        # user_combine_layer = tf.contrib.layers.fully_connected(user_combine_layer, 200, tf.tanh)  # (?, 1, 200)
        user_combine_layer = tf.compat.v1.layers.dense(user_combine_layer, 200, tf.tanh)  # (?, 1, 200)

        user_combine_layer_flat = tf.reshape(user_combine_layer, [-1, 200])
    return user_combine_layer, user_combine_layer_flat


def get_movie_id_embed_layer(movie_id):
    with tf.name_scope("movie_embedding"):
        movie_id_embed_matrix = tf.Variable(tf.random_uniform([movie_id_max, embed_dim], -1, 1),
                                            name="movie_id_embed_matrix")
        movie_id_embed_layer = tf.nn.embedding_lookup(movie_id_embed_matrix, movie_id, name="movie_id_embed_layer")
    return movie_id_embed_layer


def get_movie_categories_layers(movie_categories):
    with tf.name_scope("movie_categories_layers"):
        movie_categories_embed_matrix = tf.Variable(tf.random_uniform([movie_categories_max, embed_dim], -1, 1),
                                                    name="movie_categories_embed_matrix")
        movie_categories_embed_layer = tf.nn.embedding_lookup(movie_categories_embed_matrix, movie_categories,
                                                              name="movie_categories_embed_layer")
        if combiner == "sum":
            movie_categories_embed_layer = tf.reduce_sum(movie_categories_embed_layer, axis=1, keep_dims=True)
    #     elif combiner == "mean":

    return movie_categories_embed_layer


def get_movie_cnn_layer(movie_titles, dropout_keep_prob):
    # 从嵌入矩阵中得到电影名对应的各个单词的嵌入向量
    with tf.name_scope("movie_embedding"):
        movie_title_embed_matrix = tf.Variable(tf.random_uniform([movie_title_max, embed_dim], -1, 1),
                                               name="movie_title_embed_matrix")
        movie_title_embed_layer = tf.nn.embedding_lookup(movie_title_embed_matrix, movie_titles,
                                                         name="movie_title_embed_layer")
        # 为 movie_title_embed_layer 增加一个维度
        # 在这里是添加到最后一个维度，最后一个维度是channel
        # 所以这里的channel数量是1个
        # 所以这里的处理方式和图片是一样的
        movie_title_embed_layer_expand = tf.expand_dims(movie_title_embed_layer, -1)

    # 对文本嵌入层使用不同尺寸的卷积核做卷积和最大池化
    pool_layer_lst = []
    for window_size in window_sizes:
        with tf.name_scope("movie_txt_conv_maxpool_{}".format(window_size)):
            # [window_size, embed_dim, 1, filter_num] 表示输入的 channel 的个数是1，输出的 channel 的个数是 filter_num
            filter_weights = tf.Variable(tf.truncated_normal([window_size, embed_dim, 1, filter_num], stddev=0.1),
                                         name="filter_weights")
            filter_bias = tf.Variable(tf.constant(0.1, shape=[filter_num]), name="filter_bias")

            # conv2d 是指用到的卷积核的大小是 [filter_height * filter_width * in_channels, output_channels]
            # 在这里卷积核会向两个维度的方向进行滑动
            # conv1d 是将卷积核向一个维度的方向进行滑动，这就是 conv1d 和 conv2d 的区别
            # strides 设置要求第一个和最后一个数字是1，四个数字的顺序要求默认是 NHWC，也就是 [batch, height, width, channels]
            # padding 设置为 VALID 其实就是不 PAD，设置为 SAME 就是让输入和输出的维度是一样的
            conv_layer = tf.nn.conv2d(movie_title_embed_layer_expand, filter_weights, [1, 1, 1, 1], padding="VALID",
                                      name="conv_layer")
            # tf.nn.bias_add 将偏差 filter_bias 加到 conv_layer 上
            # tf.nn.relu 将激活函数设置为 relu
            relu_layer = tf.nn.relu(tf.nn.bias_add(conv_layer, filter_bias), name="relu_layer")

            # tf.nn.max_pool 的第一个参数是输入
            # 第二个参数是 max_pool 窗口的大小，每个数值表示对每个维度的窗口设置
            # 第三个参数是 strides，和 conv2d 的设置是一样的
            # 这边的池化是将上面每个卷积核的卷积结果转换为一个元素
            # 由于这里的卷积核的数量是 8 个，所以下面生成的是一个具有 8 个元素的向量
            maxpool_layer = tf.nn.max_pool(relu_layer, [1, sentences_size - window_size + 1, 1, 1], [1, 1, 1, 1],
                                           padding="VALID", name="maxpool_layer")
            pool_layer_lst.append(maxpool_layer)

    # Dropout层
    with tf.name_scope("pool_dropout"):
        # 这里最终的结果是这样的，
        # 假设卷积核的窗口是 2，卷积核的数量是 8
        # 那么通过上面的池化操作之后，生成的池化的结果是一个具有 8 个元素的向量
        # 每种窗口大小的卷积核经过池化后都会生成这样一个具有 8 个元素的向量
        # 所以最终生成的是一个 8 维的二维矩阵，它的另一个维度就是不同的窗口的数量
        # 在这里就是 2,3,4,5，那么最终就是一个 8*4 的矩阵，
        pool_layer = tf.concat(pool_layer_lst, 3, name="pool_layer")
        max_num = len(window_sizes) * filter_num
        # 将这个 8*4 的二维矩阵平铺成一个具有 32 个元素的一维矩阵
        pool_layer_flat = tf.reshape(pool_layer, [-1, 1, max_num], name="pool_layer_flat")
        dropout_layer = tf.nn.dropout(pool_layer_flat, dropout_keep_prob, name="dropout_layer")
    return pool_layer_flat, dropout_layer


def get_movie_feature_layer(movie_id_embed_layer, movie_categories_embed_layer, dropout_layer):
    with tf.name_scope("movie_fc"):
        # 第一层全连接
        movie_id_fc_layer = tf.layers.dense(movie_id_embed_layer, embed_dim, name="movie_id_fc_layer",
                                            activation=tf.nn.relu)
        movie_categories_fc_layer = tf.layers.dense(movie_categories_embed_layer, embed_dim,
                                                    name="movie_categories_fc_layer", activation=tf.nn.relu)

        # 第二层全连接
        movie_combine_layer = tf.concat([movie_id_fc_layer, movie_categories_fc_layer, dropout_layer], 2)  # (?, 1, 96)
        # movie_combine_layer = tf.contrib.layers.fully_connected(movie_combine_layer, 200, tf.tanh)  # (?, 1, 200)
        movie_combine_layer = tf.compat.v1.layers.dense(movie_combine_layer, 200, tf.tanh)  # (?, 1, 200)

        movie_combine_layer_flat = tf.reshape(movie_combine_layer, [-1, 200])
    return movie_combine_layer, movie_combine_layer_flat

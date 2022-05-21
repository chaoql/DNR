import os
import gensim
import jieba
import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.layers import *
from keras.layers.embeddings import Embedding
from keras.models import Model
from keras.preprocessing.sequence import pad_sequences
from keras.preprocessing.text import Tokenizer
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sqlalchemy import create_engine
from keras.models import load_model
from keras.utils.np_utils import to_categorical
from tqdm import tqdm
np.random.seed(24)
tqdm.pandas()

def readData():
    engine = create_engine('mysql+pymysql://root:cql666@localhost:3306/news_recommendation_system')

    dfnews = pd.read_sql("select * from news;", engine)
    cnames = ["newsid", "genres", "title", "authors", "link", "date", "text", "photo", "hash", "view_count"]
    dfnews.columns = cnames

    dfusers = pd.read_sql("select * from user;", engine)
    cnames = ["userid", "gender", "age", "occupation", "nickname", "rootname", "pwd", "login_salt", "updatetime",
              "createtime", "status", "email", "power"]
    dfusers.columns = cnames

    dfview = pd.read_sql("select * from view;", engine)
    dfview.drop('id', axis=1, inplace=True)
    cnames = ["userid", "newsid", "viewcount"]
    dfview.columns = cnames

    dfnews1 = dfnews.merge(dfview, on="newsid", how="left")

    dfnews1 = dfnews1.dropna(subset=["userid", "viewcount"])

    dfnews2 = dfnews1.merge(dfusers, on="userid", how="left")
    return dfnews2

dfnews2=readData()


# 留下有用的列
userfulcol = ["genres", "userid", "title", "text", "view_count", "gender", "age", "occupation", "viewcount"]
# 因为userid和nickname都是一个人，所以用userid一个就好
dfnews2 = dfnews2[userfulcol]

# 处理非文本数据
othercol = ["genres", "userid", "gender", "age", "occupation", "view_count"]
dfnews3 = dfnews2[othercol]
catefea = ["genres", "userid", "gender", "occupation"]
for col in catefea:
    tmpd = dict(zip(dfnews3[col].unique(), range(len(dfnews3[col].unique()))))
    joblib.dump(tmpd, col + ".joblib")
    dfnews3[col] = dfnews3[col].map(tmpd)
floatfea = ["age", "view_count"]

# 将标签 one-hot
dffloat = dfnews3[floatfea]
for col in catefea:
    dffloat = pd.concat([dffloat, pd.DataFrame(to_categorical(dfnews3[col]))], axis=1)
dffloat = dffloat.astype(float)

# 处理文本输入
dfnews2["textall"] = dfnews2["title"] + dfnews2["text"]
# 分词
dfnews2["textall"] = dfnews2["textall"].progress_apply(lambda x: list(jieba.cut(x)))

# w2v
w2v_model = gensim.models.Word2Vec(list(dfnews2["textall"]), size=128, iter=10, min_count=0)
word_vectors = w2v_model.wv  # 训练之后的词向量
dfnews2["len"] = dfnews2["textall"].apply(lambda x: len(x))

# 文本转向量
x_train = list(dfnews2["textall"])
tokenizer = Tokenizer()  # 分词器
tokenizer.fit_on_texts(x_train)  # 统计每个词对应的数字，生成token词典，以便于将文本转化成向量
train_sequence = tokenizer.texts_to_sequences(x_train)  # 将所有的文本转化成向量
MAX_SEQUENCE_LENGTH = 512  # 最大长度
EMBEDDING_DIM = 128  # 向量维度
y_train = dfnews2["viewcount"]
y_train = y_train.astype(float)
word_index = tokenizer.word_index  # 一个dict，保存所有word对应的编号id，从1开始
print('Found %s unique tokens.' % len(word_index))
train_pad = pad_sequences(train_sequence, maxlen=MAX_SEQUENCE_LENGTH)  # 将每条文本按照最大长度补0

# 嵌入矩阵
embedding_matrix = np.zeros((len(word_index) + 1, EMBEDDING_DIM), dtype=np.float32)
not_in_model = 0
in_model = 0
not_words = []

for word, i in word_index.items():
    if word in w2v_model:
        in_model += 1
        embedding_matrix[i] = np.array(w2v_model[word])
    else:
        not_in_model += 1
        not_words.append(word)

# 切分数据集
index = np.random.permutation(range(train_pad.shape[0]))
train_pad = train_pad[index]
dffloat = dffloat.values
dffloat = dffloat[index]
y_train = y_train.values
y_train = y_train[index]
testsize = 0.2
train_data = train_pad[int(train_pad.shape[0] * testsize):]
val_data = train_pad[:int(train_pad.shape[0] * testsize)]
train_y = y_train[int(train_pad.shape[0] * testsize):]
val_y = y_train[:int(train_pad.shape[0] * testsize)]
train_float = dffloat[int(train_pad.shape[0] * testsize):]
val_float = dffloat[:int(train_pad.shape[0] * testsize)]


# 搭建模型
def get_cnnmodel(class_num=1):
    embed = Embedding(len(word_index) + 1, EMBEDDING_DIM, weights=[embedding_matrix], input_length=MAX_SEQUENCE_LENGTH,
                      trainable=True)  # 定义一个词嵌入层,将句子转化成对应的向量
    inputs_sentence = Input(shape=(MAX_SEQUENCE_LENGTH,))  # 设置输入向量维度
    inputs_float = Input(shape=(train_float.shape[1],))  # 设置输入向量维度
    denfloat = Dense(64, activation="relu")(inputs_float)
    sentence = (embed(inputs_sentence))  # 定义词嵌入层
    kernel_sizes = [3, 4, 5]
    convs = []
    max_poolings = []
    for kernel_size in kernel_sizes:
        convs.append(Conv1D(32, kernel_size, activation='relu'))
        max_poolings.append(GlobalMaxPooling1D())
    convs1 = []
    for i in range(len(kernel_sizes)):
        c = convs[i](sentence)
        c = max_poolings[i](c)
        convs1.append(c)
    x = Concatenate()(convs1 + [denfloat])
    dp = Dropout(0.1)(x)
    output = Dense(1, activation='relu')(dp)  # softmax层
    model = Model(inputs=[inputs_sentence, inputs_float], outputs=output)
    model.compile(loss='mse', optimizer='adam', metrics=['mse'])  # 定义损失函数，优化器，评分标准
    model.summary()
    return model

# os.environ["CUDA_VISIBLE_DEVICES"] = "1"
model = get_cnnmodel()
callbacks = [EarlyStopping(monitor='val_mean_squared_error', min_delta=0.001, patience=10),
             ModelCheckpoint("textcnn.hdf5", monitor='val_mean_squared_error',
                             mode='min', verbose=0, save_best_only=True)]
# 设置模型提前停止,停止的条件是验证集val_acc两轮已经不增加,保存验证集val_acc最大的那个模型,名称为textcnn.hdf5
history = model.fit([train_data, train_float], train_y, batch_size=4, epochs=40, callbacks=callbacks,
                    validation_data=([val_data, val_float], val_y))
# 每次训练批次大小为64,遍历整整10次训练集才完成


model = load_model("textcnn.hdf5")

val_loss = history.history['val_mean_squared_error']
loss = history.history['mean_squared_error']
epochs = range(1, len(loss) + 1)

plt.title('mse')
plt.plot(epochs, loss, 'red', label='Training mse')
plt.plot(epochs, val_loss, 'blue', label='Validation mse')
plt.legend()
plt.show()

trainpre = np.squeeze(model.predict([train_data, train_float]))
print("训练集mae:", mean_absolute_error(trainpre, train_y))
print("训练集mse:", mean_squared_error(trainpre, train_y))
print("训练集rmse:", np.sqrt(mean_squared_error(trainpre, train_y)))

testpre = np.squeeze(model.predict([val_data, val_float]))
print("测试集mae:", mean_absolute_error(testpre, val_y))
print("测试集mse:", mean_squared_error(testpre, val_y))
print("测试集rmse:", np.sqrt(mean_squared_error(testpre, val_y)))

joblib.dump(tokenizer, "tokenizer.joblib")

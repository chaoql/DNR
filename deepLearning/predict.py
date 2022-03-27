import glob
import joblib
import numpy as np
import pandas as pd
from keras.utils.np_utils import to_categorical
from tqdm import tqdm
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import jieba
tqdm.pandas()
model = load_model("textcnn.hdf5")
tokenizer = joblib.load("tokenizer.joblib")

d = {}
for i in glob.glob("*"):
    if "joblib" in i and "token" not in i:
        d[i[:-7]] = joblib.load(i)

age = 21
genres = "antip"
userid = 3
gender = "Female"
numcate = [len(d["genres"].keys()), len(d["userid"].keys()), len(d["gender"].keys()), len(d["occupation"].keys())]

def get_float_input(age, viewcount, genres="antip", userid=3, gender="Female", occupation="Student"):
    try:
        genres = d["genres"][genres]
    except:
        genres = -1
    try:
        userid = d["userid"][userid]
    except:
        userid = -1
    try:
        gender = d["gender"][gender]
    except:
        gender = -1
    try:
        occupation = d["occupation"][occupation]
    except:
        occupation = -1
    floatinput = pd.DataFrame([{"0": age, "1": viewcount}])

    dffloat = floatinput
    for ind, col in enumerate([genres, userid, gender, occupation]):
        tmpdf = pd.DataFrame(to_categorical([col], num_classes=numcate[ind]))
        if col == -1:
            tmpdf = pd.DataFrame(np.zeros_like(tmpdf.values))
        dffloat = pd.concat([dffloat, tmpdf], axis=1)

    dffloat = dffloat.astype(float)
    return dffloat


get_float_input(21, 6, "1", 3, "Female", "Student")


def fenci(text):
    return list(jieba.cut(str(text)))


def text_pre(text, age, viewcount, genres="antip", userid=3, gender="Female", occupation="Student"):
    dffloat = get_float_input(age, viewcount, genres, userid, gender, occupation)
    x = text.lower()
    x = x.replace("\r", "").replace("\n", "")
    x = fenci(x)
    tmp = tokenizer.texts_to_sequences([x])
    MAX_SEQUENCE_LENGTH = 512
    EMBEDDING_DIM = 128  # 向量维度
    train_pad = pad_sequences(tmp, maxlen=MAX_SEQUENCE_LENGTH)  # 将每条文本按照最大长度补0
    # print( model.predict(train_pad))
    return model.predict([train_pad, dffloat])[0][0]


print(text_pre("随变测试", 21, 99, "1122", 3, "Female", "Student"))

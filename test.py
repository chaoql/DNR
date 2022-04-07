import pickle


def save_obj(obj, name):
    with open('./' + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)


a = {"a": 10}
save_obj(a, "a")

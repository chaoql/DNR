import pickle

from common.libs.FLHelper.Helper import save_obj
from common.models.news import News
from common.models.user import User
from deepLearning.predict import text_pre


class JobTask:
    """
    python manager.py runjob -m rateNews
    """

    def __init__(self):
        pass

    def run(self, params):
        model_news = News.query.all()
        model_user = User.query.all()
        pred = {}
        for user in model_user:
            preView = {}
            for news in model_news:
                rate = text_pre(news.title + news.text, user.age, news.view_counter, news.genres, user.id, user.gender,
                                user.occupation)
                preView[news.id] = rate
            preView_order = sorted(preView.items(), key=lambda x: x[1], reverse=True)
            preView_100 = {}
            i = 0
            for item in preView_order:
                if i < 100:
                    preView_100[item[0]] = item[1]
                i += 1
            print(user.id)
            pred[user.id] = preView_100
        save_obj(pred, "preView")







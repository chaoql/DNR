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
            preView_order = dict(sorted(preView.items(), key=lambda x: x[1], reverse=True))
            print(user.id)
            pred[user.id] = preView_order
        save_obj(pred, "preView")







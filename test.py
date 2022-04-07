from common.libs.FLHelper.Helper import load_obj
from common.models.news import News

News_list = []
preView = load_obj("preView")
print(preView)
for item in preView:
    for newsID in preView[item]:
        model_news = News.query.filter_by(id=newsID).first()
        # print(model_news)
        News_list.append(model_news)
# print(News_list)
# print("-------------------------")
# News_list = News.query.order_by(News.view_counter.desc(), News.id.desc()).all()
# print(News_list)
print(len(News_list))
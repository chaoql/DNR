# import traceback
#
# from bs4 import BeautifulSoup
#
# from application import app
# import requests
#
# app.logger.info("正在从线上获取页面content...")
# try:
#     r = requests.get(url="https://new.qq.com/omn/20220303/20220303A03ZZP00.html")
#     soup = BeautifulSoup(str(r.content), "html.parser")
#     a = ""
#     tmp_text = soup.select("div.content-article p.one-p")
#     for text in tmp_text:
#         if text.select("img"):
#             app.logger.warning("continue")
#             continue
#         a += text.getText()
#     app.logger.warning(tmp_text)
#     app.logger.warning(len(tmp_text))
#     app.logger.warning(a)
# except Exception as e:
#     traceback.print_exc()
i = 1
for i in range(10):
    a = 2
print(a)

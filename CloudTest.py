import imageio as imageio
import jieba
from matplotlib import colors
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import pymongo

# connect to database
client = pymongo.MongoClient()
db = client['crawl_data']
comments_list = list(db['album_comment'].find({}))

# change list to string
comment = ''
for item in comments_list:
    comment = comment + item['cmmt_content']

# word cloud
text = ' '.join(jieba.cut(comment))
maskshape = imageio.imread("wordcloud.jpg")
colormaps = colors.ListedColormap(['#FF0000', '#FF7F50', '#FFE4C4'])
wordcloud = WordCloud(
                    background_color="#beb4d6",  # 设置背景颜色
                    mask=maskshape,  # 设置背景图片
                    max_words=200,  # 设置最大显示的字数
                    # stopwords = "", #设置停用词
                    font_path="C://Windows//Fonts//simhei.ttf",  # 设置中文字体，使得词云可以显示（词云默认字体是“DroidSansMono.ttf字体库”，不支持中文）
                    max_font_size=100,  # 设置字体最大值
                    # random_state = 50, #设置有多少种随机生成状态，即有多少种配色方案
                    scale=4,  # 指定分辨率
                    # colormap = colormaps,  # 指定颜色
                    # palette='tableau.BlueRed_6',
            ).generate(text)

wordcloud.to_file(r"C:\Users\lenovo\Desktop\毕业设计\code\app\static\img\wordcloud.png")
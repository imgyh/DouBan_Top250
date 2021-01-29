# 引入必要的库
import jieba        #分中文词
import numpy as np  #矩阵运算
import sqlite3      #数据库
from matplotlib import pyplot as plt    #绘图数据可视化
from wordcloud import WordCloud         #词云
from PIL import Image                   #图片处理

# 准备词云所需的词
con=sqlite3.connect("movies.db")
cur=con.cursor()
sql="select instroduction from movies250"
data =cur.execute(sql)
text=""
for item in data:
    text=text+item[0]
    # print(type(item))
    
cur.close()
con.close()

# 分词
cut =jieba.cut(text)
string =' '.join(cut)   # 此处' '双引号中间有空格
print(len(string))  #打印分词数量


img = Image.open(r"./static/assets/img/tree.jpg")   # 打开图片
img_array = np.array(img)   # 将图片转化成数组
wc=WordCloud(
    background_color='white',           # 设置背景颜色
    mask=img_array,                     # 设置背景图片
    font_path='/mnt/c/Windows/Fonts/msyhl.ttc')     #使用WSL子系统需要指定完整的字体路径
                                                    # 若是有中文的话，必须添加中文字体，不然会出现方框，不出现汉字

wc.generate_from_text(string)

# 绘制图片
fig=plt.figure(1)   #新建一个名叫 Figure1的画图窗口
plt.imshow(wc)      #显示图片，同时也显示其格式
plt.axis('off') #是否显示坐标轴

plt.savefig(r"./static/assets/img/word.jpg",dpi=400)    #保存合成图片，dpi是设定分辨率，默认为400


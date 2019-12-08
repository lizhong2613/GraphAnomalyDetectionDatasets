# GraphAnomalyDetectionDatasets
本库总结读过的图异常检测中使用的数据集 按照是否是图异常检测 分成两类 
1. 图异常检测数据集
2. 其他异常检测常用数据集
## 图异常检测数据集
### 网络类型为同质网络
1.

数据集名称 | 节点数目 | 边数目 | 下载地址 | 说明
---|--- |--- | --- | --- 
Twitter | 81306 |1768149 | http://proj.ise.bgu.ac.il/sns/datasets/twitter.csv.gz 标注文件：http://proj.ise.bgu.ac.il/sns/datasets/twitter_fake_ids.csv | Twitter数据集 使用接口查询如果用户账号被停用则为异常数据 执行代码见python文件
microblogPCU | 99413 |124642 | 见本项目文件 https://archive.ics.uci.edu/ml/machine-learning-databases/00323/ | 新浪微博数据集 可以使用微博地址+用户编号确定用户是否异常账户 账号被停用则为异常数据 执行代码见weibo_checker.py文件
Academia.edu | 85577 |137171 | http://proj.ise.bgu.ac.il/sns/datasets/academia.csv.gz | 论文作者之间的相互关系
ArXiv | 5242 |14484 | 见项目文件 | 论文作者之间的相互关系
Boys’ Friendship | 185 |360 | http://proj.ise.bgu.ac.il/sns/datasets/Relationship_patterns_in_the_19th_century.csv  标注文件：http://proj.ise.bgu.ac.il/sns/datasets/Relationship_patterns_labels.csv| 该数据集为一个德国学校班级的友谊网络（1880-81年）。
DBLP | 317,080	 |1,049,866 | http://snap.stanford.edu/data/com-DBLP.html | DBLP 是计算机领域内对研究的成果以作者为核心的一个计算机类英文文献的集成数据库系统




### 网络类型为异质网络
数据集名称 | 节点数目 | 边数目 | 下载地址 | 说明
---|--- |--- | --- | --- 
Flixster | 787,213	 |11,794,648 | librec公开 https://www.librec.net/download.html | librec是一个推荐系统，里面公开了很多可用于图异常检测的数据集.Flixster是一个社交电影网站，允许用户分享电影评论和发现新电影。
Yelp | - |5,200,000  | https://www.kaggle.com/yelp-dataset/yelp-dataset | Yelp是美国最大点评网站
douban | 129490 |1,692,952 | https://www.librec.net/datasets.html | 该数据集为异质网络 


##其他数据集
2. SNAP公开的数据集
 地址：http://snap.stanford.edu/data/index.html


3.BGU公开的数据集
http://proj.ise.bgu.ac.il/sns/datasets.html


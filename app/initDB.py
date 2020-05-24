# author    :   Meng Ding
# function  :   Initialize the tablespace and the schema of each table
import sqlite3

class initDB():
    def __init__(self):
        print('Invoked successfully.')


    def run(self):
        # self.buildNewsTable() # 初始化新闻存储表
        # self.buildUserTable() # 初始化用户注册信息表
        self.buildUserBehaviorTable() # 初始化用户行为记录表
        self.buildBoardInfoTable() # 初始化留言板信息记录表

    # 新闻存储表定义
    def buildNewsTable(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS news_table')
        c.execute(
            'CREATE TABLE IF NOT EXISTS news_table(news_id INTEGER PRIMARY KEY, author TEXT, title TEXT, description TEXT, url TEXT, url_to_image TEXT, publish_date TEXT, content TEXT)')
        # 该表字段包括：
        # news_id           :   新闻编号（可考虑automatic increment） - p.k.主键
        # author            :   作者名称
        # title             :   标题
        # description       :   描述
        # url               :   原文链接
        # url_to_image      :   图片地址
        # publish_date      :   发布日期
        # content           :   文章的内容

    # 用户注册信息表定义
    # def buildUserTable(self):
        # conn = sqlite3.connect('database.db')
        # c = conn.cursor()
        # c.execute('DROP TABLE IF EXISTS user_table')
        # c.execute(
        #     'CREATE TABLE IF NOT EXISTS user_table(user_id REAL, user_name TEXT, password TEXT)')
        # 该表字段包括：
        # user_id           :   用户编号（可考虑automatic increment） - p.k.
        # user_name         :   用户名
        # password          :   密码

    # 用户行为记录表定义
    def buildUserBehaviorTable(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS user_behavior_table')
        c.execute(
            'CREATE TABLE IF NOT EXISTS user_behavior_table(user_id REAL, news_id REAL, liked REAL, viewed REAL)')
        # 该表字段包括：
        # user_id           :   用户编号 - p.k.
        # news_id           :   新闻编号 - f.k.外键
        # liked             :   该新闻是否被该用户点赞（0为“否”，1为“是”）
        # viewed            :   该新闻是否被该用户转发（0为“否”，1为“是”）
        conn.commit()

    # 留言板信息记录表定义
    def buildBoardInfoTable(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute('DROP TABLE IF EXISTS board_info_table')
        c.execute(
            'CREATE TABLE IF NOT EXISTS board_info_table(post_id REAL, post_type_id REAL, user_id REAL, reply_sequence_id REAL, content TEXT)')
        # 该表字段包括：
        # post_id           :   帖子编号 - p.k.
        # post_type_id      :   帖子类型编号（0为“楼主贴”，1为“跟帖”）
        # user_id           :   留言者用户编号 - f.k.
        # reply_sequence_id :   如果类型为“跟帖”，跟帖的楼数编号（如为“楼主”帖则该项为0）
        # content TEXT      :   留言内容
        conn.commit()

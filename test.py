
# -----------------------------------------------------
# match文の練習
# -----------------------------------------------------

# def http_error(status):
#     match status:
#         case 400:
#             return "Bad request"
#         case 404:
#             return "Not found"
#         case 418:
#             return "I'm a teapot"
#         case _:
#             return "Something's wrong with the internet"
        
# print(http_error(400))


# y = 5
# point = (0, y)

# match point:
#     case (0, 0):
#         print("x, y が0")
#     case (0, y):
#         print(f"xが0, yが{y}です")
#     case (x, 0):
#         print(f"xが{x}, yが0")
#     case (x, y):
#         print("どちらも0ではありません")


# city = input("住んでいる市を入力してください")

# match city:
#     case "盛岡市" | "山形市" | "青森市" as c: # cに代入
#         your_city = f"{c}は東北地方です"
#     case "津市" | "伊勢市" | "和歌山市" as c:
#         your_city = f"{c}は近畿地方です。"
#     case _ as c:
#         your_city = f"{c}は日本にあります。"

# print(your_city)


# cat_dog = input("犬と猫、どっちが好きですか？: ")
# match cat_dog:
#     case "犬" | "dog" | "いぬ" as c:
#         choice = c
#     case "猫" | "cat" | "ネコ" as c:
#         choice = c
#     case _ as c:
#         choice = c

# print(f"あなたが好きなのは{choice}です")


# from enum import Enum

# # Enum定義
# class Animal(Enum):
#     DOG = "犬"
#     CAT = "猫"

# # ユーザー入力を Enum に変換
# try:
#     animal = Animal(input("犬と猫はどちらがすきですか?: "))
# except ValueError:
#     animal = None

# # match文で分岐
# match animal:
#     case Animal.DOG as c:
#         animal_choice = c
#     case Animal.CAT as c:
#         animal_choice = c
#     case _ as c:
#         animal_choice = c

# print(f"私が好きなのは{animal_choice.value}です！")




# from enum import Enum

# # Enum 定義
# class Color(Enum):
#     RED = "red"
#     GREEN = "green"
#     BLUE = "blue"

# # ユーザー入力を Enum に変換
# try:
#     color = Color(input("Enter red, green, or blue: "))
# except ValueError:
#     color = None

# # match 文で分岐
# match color:
#     case Color.RED:
#         print("I see red!")
#     case Color.GREEN:
#         print("Grass is green")
#     case Color.BLUE:
#         print("I'm feeling the blues :(")
#     case _:
#         print("Unknown color")

# from enum import Enum

# # Enum定義
# class Animal(Enum):
#     DOG = ("犬", "いぬ", "dog") 
#     CAT = ("猫", "ねこ", "cat")

# cat_dog = input("犬と猫、どっちが好きですか？: ")
# match cat_dog:
#     case "犬" | "dog" | "いぬ" as c:
#         choice = c
#     case "猫" | "cat" | "ネコ" as c:
#         choice = c
#     case _ as c:
#         choice = c

# print(f"あなたが好きなのは{choice}です")




# age = int(input("あなたは何歳ですか？: "))

# match age:
#     case a if 0 <= a < 18:
#         print("子ども料金です")
#     case a if 18 <= a < 60:
#         print("大人料金です")
#     case a if 60 <= a:
#         print("シニア割引です")
#     case _:
#         print("Invalid age")


# from enum import Enum

# class Group(Enum):
#     CHILD = "子ども"
#     ADULT = "大人"
#     SENIOR = "シニア"

# age = int(input("あなたの年齢は？： "))

# match age:
#     case a if 0 <= a < 18:
#         your_age = Group.CHILD
#     case a if 18 <= a < 60:
#         your_age = Group.ADULT
#     case a if 60 <= a < 110:
#         your_age = Group.SENIOR
#     case _:
#         your_age = None

# print(f"あなたは{your_age.value}料金です")




# -----------------------------------------------------
#  if文を使わない練習
# -----------------------------------------------------



# -----------------------------------------------------
#  SQLiteの練習
# -----------------------------------------------------

# import sqlite3

# # ファイルに保存する場合
# conn = sqlite3.connect('test.db')

# # カーソルを作る　## カーソルはSQLを実行するための窓口
# cur = conn.cursor()

# # テーブルを作成する
# cur.execute('''
# CREATE TABLE IF NOT EXISTS users (
#     id INTEGER PRIMARY KEY,
#     name TEXT,
#     age INTEGER
# )
# ''')

# # データを挿入する
# cur.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("yamada", 25))
# cur.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("hayasi", 30))

# # 変更を保存
# conn.commit()

# # データを取得
# cur.execute("SELECT * FROM users")
# rows = cur.fetchall()  # 全件取得

# for row in rows:
#     print(row)
    
# # データベースを閉じる
# conn.close()


# withを使った例

# import sqlite3

# # with文で接続すると自動でcommitとcloseがされる
# with sqlite3.connect('my_database.db') as conn:
#     cur = conn.cursor()

#     # テーブル作成
#     cur.execute('''
#     CREATE TABLE IF NOT EXISTS users (
#         id INTEGER PRIMARY KEY,
#         name TEXT,
#         age INTEGER
#     )
#     ''')

#     # データを挿入
#     cur.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("tanaka", 25))
#     cur.execute("INSERT INTO users (name, age) VALUES (?, ?)", ("hayasi", 30))

#     # データを取得して表示
#     cur.execute("SELECT * FROM users")
#     rows = cur.fetchall()
#     for row in rows:
#         print(row)

# ここで自動的にconn.commit()とconn.close()が行われる


# -----------------------------------------------------
#  SQLAlchemyの練習
# -----------------------------------------------------

# from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import declarative_base
# from sqlalchemy import create_engine   # ← ここを追加

# # ORM用の規定クラスの作成
# Base = declarative_base()

# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)
#     age = Column(Integer)

# # ------------------------------
# # ここからDB接続してテーブル作成
# engine = create_engine("sqlite:///example.db", echo=True)  # DB作成・接続
# Base.metadata.create_all(engine)  # 定義したテーブルをDBに作る


from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# データベース接続 (SQLiteを使用)
engine = create_engine('sqlite:///mydatabase.db', echo=True)

# テーブル定義用のベースクラス
Base = declarative_base()

# ユーザーテーブルを定義
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)   # 主キー
    name = Column(String, nullable=False)    # 名前
    age = Column(Integer)                     # 年齢

    def __repr__(self):
        return f"<User(name='{self.name}', age={self.age})>"

# テーブルを作成
Base.metadata.create_all(engine)







# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.orm import declarative_base, sessionmaker

# # 1. データベースに接続
# engine = create_engine('sqlite:///simple.db', echo=True)

# # 2. テーブルのベースを作る
# Base = declarative_base()

# # 3. テーブル定義
# class User(Base):
#     __tablename__ = 'users'
#     id = Column(Integer, primary_key=True)
#     name = Column(String)


# # 4. テーブルを作成
# Base.metadata.create_all(engine)

# # 5. セッション作成
# Session = sessionmaker(bind=engine)
# session = Session()

# # 6. データ追加
# session.add(User(name="Alice"))
# session.commit()

# # 7. データ取得
# user = session.query(User).first()
# print(user.name)

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



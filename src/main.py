from PIL import Image
import pyocr

import requests
import pprint
import re
import os


def get_chara_name(images):

    # 自身の順位：(X_left, Y_up) = (420, 0), (X_right, Y_up) = (580, 0), (X_left, Y_down) = (420, 160),(X_right, Y_down) = (580, 160)
    # 自身の使用キャラクター：(X_left, Y_up) = (170, 510), (X_right, Y_up) = (450, 510), (X_left, Y_down) = (170, 590),(X_right, Y_down) = (580, 590)
    # 相手の順位：(X_left, Y_up) = (950, 0), (X_right, Y_up) = (1080, 0), (X_left, Y_down) = (950, 160),(X_right, Y_down) = (1080, 160)
    # 相手の使用キャラクター：(X_left, Y_up) = (700, 510), (X_right, Y_up) = (9800, 510), (X_left, Y_down) = (700, 590),(X_right, Y_down) = (980, 590)

    # 切り取り箇所の設定
    my_rank = (420, 0, 580, 160)#自身の順位
    usedfighter = (170, 510, 450, 590)

    match_rank = (950, 0, 1080, 160)
    matchfighter = (700, 510, 980, 590)

    usedfighter_im = im.crop(usedfighter)
    usedfighter_im = usedfighter_im.rotate(352)

    matchfighter_im = im.crop(matchfighter)
    matchfighter_im = matchfighter_im.rotate(352)

    my_rank_im = im.crop(my_rank)
    my_rank_im = my_rank_im.rotate(355)

    match_rank_im = im.crop(match_rank)
    match_rank_im = match_rank_im.rotate(355)

    pyocr.tesseract.TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # OCRエンジンを取得
    engines = pyocr.get_available_tools()
    engine = engines[0]

    # 画像の文字を読み込む
    usedfighter = engine.image_to_string(usedfighter_im, lang="eng")
    matchfighter = engine.image_to_string(matchfighter_im, lang="eng")

    my_rank = engine.image_to_string(my_rank_im, lang="eng", builder=pyocr.builders.DigitBuilder(tesseract_layout=10))
    match_rank = engine.image_to_string(match_rank_im, lang="eng", builder=pyocr.builders.DigitBuilder(tesseract_layout=10))

    # print(my_rank)
    # print(match_rank)
    if my_rank == '2':
        match_rank = '1'
    elif match_rank == '2':
        my_rank = '1'

    # print(my_rank)
    # print(match_rank)

    if (my_rank == '1') or (my_rank == '4') or (my_rank == '7'):
        my_rank = '1'
        match_rank = '2'
    elif (match_rank == '1') or (match_rank == '4') or (match_rank == '7'):
        match_rank = '1'
        my_rank = '2'

    characters = ['MARIO', 'DONKEY KONG', 'LINK', 'SAMUS', 'DARK SAMUS', 'YOSHI', 'KIRBY', 'FOX', 'PIKACHU', 'LUIGI', 'NESS',
                'CAPTAIN FALCON', 'PURIN', 'PEACH', 'DAISY', 'KOOPA', 'ICE CLIMBERS', 'SHEIK', 'ZELDA', 'DR.MARIO', 'PICHU', 'FALCO',
                'MARTH', 'LUCINA', 'YOUNG LINK', 'GANONDORF', 'MEWTWO', 'ROY', 'CHROM', 'MR.GAME & WATCH', 'META KNIGHT', 'PIT', 'DARK PIT', 'ZERO SUIT SAMUS', 'WARIO',
                'SNAKE', 'IKE', 'POKEMON TRAINER', 'DIDDY KONG', 'LUCAS', 'SONIC', 'DEDEDE', 'OLIMAR', 'LUCARIO', 'ROBOT', 'TOON LINK', 'WOLF', 'MURABITO', 'ROCK MAN',
                'Wii Fit TRAINER', 'ROSETTA & CHIKO', 'LITTLE MAC', 'GEKKOUGA', 'Mii FIGHTER', 'Mii GUNNER', 'Mii SWORDSMAN'
    ]



    UsedFighter = str(characters.index(usedfighter) + 1)
    MatchFighter = str(characters.index(matchfighter) + 1)
    Result  = my_rank

    payload = {'UseFighter': UsedFighter, 'MatchFighter': MatchFighter, 'comment': '', 'Result': Result  , 'submit': '登録する'}

    return payload

#クマメイトのユーザ名とパスワード
USER = '****'
PASS = '****'

session = requests.Session()
url = {'top':'https://kumamate.net', 'login':'https://kumamate.net/wp-login.php', 'regit':'https://kumamate.net/submitfight'}
login={'log': USER, 'pwd':PASS, 'wp-submit': 'ログイン','redirect_to': url['top'], 'testcookie': '1'}

state = session.get(url['top'], timeout=(20, 20))

print(re.search(r'<title.*', state.text).group(0))
print(state.status_code)

# ログイン
state = session.post(url['login'], data=login, timeout=(20, 20))
print(re.search(r'<title.*', state.text).group(0))
print(state.status_code)

# fileの読みも気
### 画像ファイル数だけ繰り返す ###

data_dir_path = u"./images/"
file_list = os.listdir(r'./images/')

for file_name in file_list:
    root, ext = os.path.splitext(file_name)
    if ext == u'.png' or u'.jpeg' or u'.jpg':
        abs_name = data_dir_path + '/' + file_name
        print(abs_name)
        im = Image.open(abs_name)
        payload = get_chara_name(im)

        state = session.get(url['top'])
        state = session.post(url['regit'], data=payload, timeout=(20, 20))

from PIL import Image
from PIL import ImageDraw
import pyocr

import requests
import pprint
import re
import os


def get_chara_name(im):

    # 自身の順位：(X_left, Y_up) = (420, 0), (X_right, Y_up) = (580, 0), (X_left, Y_down) = (420, 160),(X_right, Y_down) = (580, 160)
    # 自身の使用キャラクター：(X_left, Y_up) = (170, 510), (X_right, Y_up) = (450, 510), (X_left, Y_down) = (170, 590),(X_right, Y_down) = (580, 590)
    # 相手の順位：(X_left, Y_up) = (950, 0), (X_right, Y_up) = (1080, 0), (X_left, Y_down) = (950, 160),(X_right, Y_down) = (1080, 160)
    # 相手の使用キャラクター：(X_left, Y_up) = (700, 510), (X_right, Y_up) = (9800, 510), (X_left, Y_down) = (700, 590),(X_right, Y_down) = (980, 590)

    # 切り取り箇所の設定
    my_rank = (450, 0, 570, 160)#自身の順位
    usedfighter = (170, 520, 410, 600)
    match_rank = (940, 0, 1070, 160)
    matchfighter = (700, 520, 940, 600)

    usedfighter_im = im.crop(usedfighter)
    
    draw = ImageDraw.Draw(usedfighter_im)
    draw.polygon(((0,0), (0, 20), (190, 0)), fill=(0, 0, 0), outline=(0, 0, 0))
    draw.polygon(((120, 80), (240, 80), (240, 65)), fill=(0, 0, 0), outline=(0, 0, 0))
    draw.line(((0,0), (0, 80)), fill=(0, 0, 0), width=8)
    draw.line(((0,80), (240,80)), fill=(0, 0, 0), width=8)
    
    pixelSizeTuple = usedfighter_im.size

    tmp = Image.new('RGB', usedfighter_im.size)

    for i in range(pixelSizeTuple[0]):
        for j in range(pixelSizeTuple[1]):
            r,g,b = usedfighter_im.getpixel((i, j))
            if ((r > 100) and (b < 50) and (g < 50))or ((b > 100) and (r < 50) and (g < 50)):
                tmp.putpixel((i, j), (0, 0, 0))
            else:
                tmp.putpixel((i, j), (r, g, b))
    usedfighter_im = tmp
    usedfighter_im = usedfighter_im.rotate(355)

    matchfighter_im = im.crop(matchfighter)

    draw = ImageDraw.Draw(matchfighter_im)
    draw.polygon(((0,0), (0, 20), (190, 0)), fill=(0, 0, 0), outline=(0, 0, 0))
    draw.polygon(((120, 80), (240, 80), (240, 65)), fill=(0, 0, 0), outline=(0, 0, 0))
    draw.line(((0,0), (0, 80)), fill=(0, 0, 0), width=8)
    draw.line(((0,80), (240,80)), fill=(0, 0, 0), width=8)

    pixelSizeTuple = matchfighter_im.size

    tmp = Image.new('RGB', matchfighter_im.size)

    for i in range(pixelSizeTuple[0]):
        for j in range(pixelSizeTuple[1]):
            r,g,b = matchfighter_im.getpixel((i, j))
            if ((r > 100) and (b < 50) and (g < 50))or ((b > 100) and (r < 100) and (g < 100)):
                tmp.putpixel((i, j), (0, 0, 0))
            else:
                tmp.putpixel((i, j), (r, g, b))
    matchfighter_im = tmp

    matchfighter_im = matchfighter_im.rotate(355)

    my_rank_im = im.crop(my_rank)

    match_rank_im = im.crop(match_rank)

    pyocr.tesseract.TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # OCRエンジンを取得
    engines = pyocr.get_available_tools()
    engine = engines[0]

    # 画像の文字を読み込む
    usedfighter = engine.image_to_string(usedfighter_im, lang="eng",  builder=pyocr.builders.DigitBuilder(tesseract_layout=6)).replace( '\n' , ' ' )
    matchfighter = engine.image_to_string(matchfighter_im, lang="eng").replace( '\n' , ' ' )

    my_rank = engine.image_to_string(my_rank_im, lang="eng", builder=pyocr.builders.DigitBuilder(tesseract_layout=10))
    match_rank = engine.image_to_string(match_rank_im, lang="eng", builder=pyocr.builders.DigitBuilder(tesseract_layout=10))

    # print(my_rank)
    # print(match_rank)
    if my_rank == '2':
        match_rank = '1'
    elif match_rank == '2':
        my_rank = '1'

    print(my_rank)
    print(match_rank)

    print(usedfighter)
    print(matchfighter)

    if (my_rank == '1') or (my_rank == '4') or (my_rank == '7'):
        my_rank = '1'
        match_rank = '2'
    elif (match_rank == '1') or (match_rank == '4') or (match_rank == '7'):
        match_rank = '1'
        my_rank = '2'

    characters = ['MARIO', 'DONKEY KONG', 'LINK', 'SAMUS', 'DARK SAMUS', 'YOSHI', 'KIRBY', 'FOX', 'PIKACHU', 'LUIGI', 'NESS',
                'CAPTAIN FALCON', 'PURIN', 'PEACH', 'DAISY', 'KOOPA', 'ICE CLIMBER', 'SHEIK', 'ZELDA', 'Dr. MARIO', 'PICHU',
                'FALCO','MARTH', 'LUCINA', 'YOUNG LINK', 'GANONDORF', 'MEWTWO', 'ROY', 'CHROM', 'Mr. GAME & WATCH', 'META KNIGHT', 
                'PIT', 'BLACK PIT', 'ZERO SUIT SAMUS', 'WARIO','SNAKE', 'IKE', 'POKEMON TRAINER', 'DIDDY KONG', 'LUCAS', 'SONIC',
                'DEDEDE', 'PIKMIN & OLIMAR', 'LUCARIO', 'ROBOT', 'TOON LINK', 'WOLF', 'MURABITO', 'ROCK MAN', 'Wii Fit TRAINER',
                'ROSETTA & CHIKO', 'LITTLE MAC', 'GEKKOUGA', 'Mii BRAWLER', 'Mii GUNNER', 'Mii SWORD FIGHTER', 'PALUTENA',
                'PAC-MAN', 'REFLET', 'SHULK', 'KOOPA Jr.', 'DUCK HUNT', 'RYU', 'KEN', 'CLOUD', 'KAMUI', 'BAYONETTA', 'INKLING',
                'RIDLEY', 'SIMON', 'RICHTER', 'KING K. ROOL', 'SHIZUE', 'GAOGAEN', 'PACKUN FLOWER', 'JOKER','HERO',
                'BANJO & KAZOOIE', 'TERRY', 'BYLETH', 'MINMIN', 'STEVE', 'SEPHIROTH', 'HOMURA', 'KAZUYA', 'SORA', 'HIKARI', 
                'ALEX', 'ZOMBIE', 'ENDERMAN'
    ]
    
    if str(characters.index(usedfighter) + 1) >= '88':
        UsedFighter = str(characters.index('STEVE') + 1)
    elif str(characters.index(usedfighter) + 1) == '87':
        UsedFighter = str(characters.index('HOMURA') + 1)
    else:
        UsedFighter = str(characters.index(usedfighter) + 1)

    if str(characters.index(matchfighter) + 1) >= '88':
        MatchFighter = str(characters.index('STEVE') + 1)
    elif str(characters.index(matchfighter) + 1) == '87':
        MatchFighter = str(characters.index('HOMURA') + 1)
    else:
        MatchFighter = str(characters.index(matchfighter) + 1)
    Result  = my_rank

    payload = {'UseFighter': UsedFighter, 'MatchFighter': MatchFighter, 'comment': '', 'Result': Result  , 'submit': '登録する'}

    return payload

#クマメイトのユーザ名とパスワード
USER = '******'
PASS = '******'

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
file_list = os.listdir(r'./images')

for file_name in file_list:
    root, ext = os.path.splitext(file_name)
    if ext == u'.png' or u'.jpeg' or u'.jpg':
        abs_name = data_dir_path + file_name
        print(abs_name)
        im = Image.open(abs_name)
        payload = get_chara_name(im)

        state = session.get(url['top'])
        state = session.post(url['regit'], data=payload, timeout=(20, 20))

# im = Image.open('./images/2.jpg')
# payload = get_chara_name(im)

# state = session.get(url['top'])
# state = session.post(url['regit'], data=payload, timeout=(20, 20))

from PIL import Image
import pyocr
im = Image.open('./images/result_example.jpg')

def get_chara_name(images):

    # 自身の順位：(X_left, Y_up) = (420, 0), (X_right, Y_up) = (580, 0), (X_left, Y_down) = (420, 160),(X_right, Y_down) = (580, 160)
    # 自身の使用キャラクター：(X_left, Y_up) = (170, 510), (X_right, Y_up) = (450, 510), (X_left, Y_down) = (170, 590),(X_right, Y_down) = (580, 590)
    # 相手の順位：(X_left, Y_up) = (950, 0), (X_right, Y_up) = (1080, 0), (X_left, Y_down) = (950, 160),(X_right, Y_down) = (1080, 160)
    # 相手の使用キャラクター：(X_left, Y_up) = (700, 510), (X_right, Y_up) = (9800, 510), (X_left, Y_down) = (700, 590),(X_right, Y_down) = (980, 590)

    # 切り取り箇所の設定
    my_rank = (420, 0, 580, 160)#自身の順位
    my_cha = (170, 510, 450, 590)

    your_rank = (950, 0, 1080, 160)
    your_cha = (700, 510, 980, 590)

    my_cha_im = im.crop(my_cha)
    my_cha_im = my_cha_im.rotate(352)

    your_cha_im = im.crop(your_cha)
    your_cha_im = your_cha_im.rotate(352)

    my_rank_im = im.crop(my_rank)
    my_rank_im = my_rank_im.rotate(355)

    your_rank_im = im.crop(your_rank)
    your_rank_im = your_rank_im.rotate(355)

    pyocr.tesseract.TESSERACT_CMD = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    # OCRエンジンを取得
    engines = pyocr.get_available_tools()
    engine = engines[0]

    # 画像の文字を読み込む
    my_cha = engine.image_to_string(my_cha_im, lang="eng")
    your_cha = engine.image_to_string(your_cha_im, lang="eng")

    my_rank = engine.image_to_string(my_rank_im, lang="eng", builder=pyocr.builders.DigitBuilder(tesseract_layout=10))
    your_rank = engine.image_to_string(your_rank_im, lang="eng", builder=pyocr.builders.DigitBuilder(tesseract_layout=10))

    print(my_rank)
    print(your_rank)
    if my_rank == '2':
        your_rank = '1'
    elif your_rank == '2':
        my_rank = '1'

    print(my_rank)
    print(your_rank)

    if (my_rank == '1') or (my_rank == '4') or (my_rank == '7'):
        my_rank = '1'
        your_rank = '2'
        print('nak')
    elif (your_rank == '1') or (your_rank == '4') or (your_rank == '7'):
        your_rank = '1'
        my_rank = '2'

    return {'my_rank':my_rank, 'my_cha':my_cha, 'your_rank':your_rank, 'your_cha':your_cha}

print(get_chara_name(im))

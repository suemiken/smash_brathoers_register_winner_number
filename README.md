# smash_brathoers_register_winner_number

大乱闘スマッシュブラザーズの対戦記録アプリである。Switchのアルバム機能からPCへ簡単にデータ転送が可能になったため、
作成しようと考えた。

リザルト画面を撮影し、自分と相手の使用キャラ、自身が勝率や苦手な相手を管理できる。既存の方法としてクマメイトがあるが、
一つ一つ登録しなければならないという問題がある。
このプログラムを使用すれば、リザルトの写真を撮影し、後日まとめてデータ転送するだけで、
対戦の記録と勝率の確認が可能である。

現在、勝敗の管理はクマメイトへリクエストすることで行うことを想定するが、自身でＤＢを作成することも可能である。

# feature

文字認識を使用して自分のファイターと相手のファイターを記録する。以下はオンラインで対戦した際にのリザルト画面の例である。
以下のように自身は1pと記録され、左側に表示され、対戦相手は2pとなり、右側に表示される。キャラ名が表示される箇所は固定であるため、
あるピクセルの範囲を切り取り、文字認識を行うことで、自身、相手の使用キャラを判別する。
自身の勝敗は右上の数字を認識することで判定する。１のとき、勝利、２の時敗北とし、記録を行う。


![result_example](https://user-images.githubusercontent.com/18396212/168417513-69198637-a6d6-4b02-9f62-af6f0eb9ac68.jpg)

# Requirement and Installation

OS:windows

conda env create -f requirement.yml

# Usage


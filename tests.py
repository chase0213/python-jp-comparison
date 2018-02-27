import re
import time

import logging

# 検証モジュール
import jaconv
import cnvk
import mojimoji
import zenhan
import rfZenHan
import nkf

# 10万回繰り返す
N = 100000

# ログレベル
logging.basicConfig(filename="test.log", level=logging.DEBUG)


def calc_time(func, *args):
    start = time.time()
    for _ in range(0, N):
        func(*args)
    end = time.time()
    logging.info("%5.2f[s]" % (end - start))


def get_test_cases():
    return [
      {
        "title": "単語（ひらがなのみ）",
        "body": "たんご",
      },
      {
        "title": "単語（カタカナのみ)",
        "body": "タンゴ",
      },
      {
        "title": "単語（漢字・ひらがなのみ）",
        "body": "単ご",
      },
      {
        "title": "短文（漢字・ひらがなのみ）",
        "body": "この文章には、片仮名は一文字も含まれていません",
      },
      {
        "title": "短文（カナカナのみ）",
        "body": "コノブンショウハカナカナノミデコウセイサレタタンブンデス",
      },
      {
        "title": "長文（漢字・ひらがなのみ）",
        "body": """雨にもまけず
          風にもまけず
          雪にも夏の暑さにもまけぬ
          丈夫なからだをもち
          欲はなく
          決して怒らず
          いつもしずかにわらっている
          一日に玄米四合と
          味噌と少しの野菜をたべ
          あらゆることを
          じぶんをかんじょうに入れずに
          よくみききしわかり
          そしてわすれず
          野原の松の林の蔭の
          小さな萓ぶきの小屋にいて
          東に病気のこどもあれば
          行って看病してやり
          西につかれた母あれば
          行ってその稲の束を負い
          南に死にそうな人あれば
          行ってこわがらなくてもいいといい
          北にけんかやそしょうがあれば
          つまらないからやめろといい
          ひでりのときはなみだをながし
          さむさのなつはオロオロあるき
          みんなにデクノボーとよばれ
          ほめられもせず
          くにもされず
          そういうものに
          わたしはなりたい""",
      },
      {
        "title": "長文（カタカナ中心）",
        "body": """雨ニモマケズ
          風ニモマケズ
          雪ニモ夏ノ暑サニモマケヌ
          丈夫ナカラダヲモチ
          慾ハナク
          決シテ瞋ラズ
          イツモシヅカニワラッテヰル
          一日ニ玄米四合ト
          味噌ト少シノ野菜ヲタベ
          アラユルコトヲ
          ジブンヲカンジョウニ入レズニ
          ヨクミキキシワカリ
          ソシテワスレズ
          野原ノ松ノ林ノ蔭ノ
          小サナ萓ブキノ小屋ニヰテ
          東ニ病気ノコドモアレバ
          行ッテ看病シテヤリ
          西ニツカレタ母アレバ
          行ッテソノ稲ノ朿ヲ負ヒ
          南ニ死ニサウナ人アレバ
          行ッテコハガラナクテモイヽトイヒ
          北ニケンクヮヤソショウガアレバ
          ツマラナイカラヤメロトイヒ
          ヒドリノトキハナミダヲナガシ
          サムサノナツハオロオロアルキ
          ミンナニデクノボートヨバレ
          ホメラレモセズ
          クニモサレズ
          サウイフモノニ
          ワタシハナリタイ""",
      },
    ]


def test_jaconv():
    logging.info("=========================================")
    logging.info("=               jaconv                  =")
    logging.info("=========================================")
    test_cases = get_test_cases()
    for tc in test_cases:
        title = tc['title']
        body = tc['body']

        logging.info("ひらがな（全角） to カタカナ（全角） for %s" % title)
        calc_time(jaconv.hira2kata, body)
        logging.debug("result: %s" % jaconv.hira2hkata(body))

        logging.info("カタカナ（全角） to ひらがな（全角） for %s" % title)
        calc_time(jaconv.kata2hira, body)
        logging.debug("result: %s" % jaconv.kata2hira(body))

        logging.info("ひらがな（全角） to カタカナ（半角） for %s" % title)
        calc_time(jaconv.hira2hkata, body)
        logging.debug("result: %s" % jaconv.hira2hkata(body))

        logging.info("半角 to 全角 for %s" % title)
        calc_time(jaconv.h2z, body)
        logging.debug("result: %s" % jaconv.h2z(body))

        logging.info("全角 to 半角 for %s" % title)
        calc_time(jaconv.z2h, body)
        logging.debug("result: %s" % jaconv.z2h(body))


def test_cnvk():
    logging.info("=========================================")
    logging.info("=                 cnvk                  =")
    logging.info("=========================================")
    test_cases = get_test_cases()
    for tc in test_cases:
        title = tc['title']
        body = tc['body']

        logging.info("ひらがな（全角） to カタカナ（全角） for %s" % title)
        calc_time(cnvk.convert, body, cnvk.HIRA2KATA)
        logging.debug("result: %s" % cnvk.convert(body, cnvk.HIRA2KATA))

        logging.info("カタカナ（全角） to ひらがな（全角） for %s" % title)
        calc_time(cnvk.convert, body, cnvk.Z_KATA, cnvk.KATA2HIRA)
        logging.debug("result: %s" % cnvk.convert(body, cnvk.Z_KATA, cnvk.KATA2HIRA))

        logging.info("ひらがな（全角） to カタカナ（半角） for %s" % title)
        calc_time(cnvk.convert, body, cnvk.HIRA2KATA, cnvk.H_KATA)
        logging.debug("result: %s" % cnvk.convert(body, cnvk.KATA2HIRA, cnvk.H_KATA))

        logging.info("半角 to 全角 for %s" % title)
        calc_time(cnvk.convert, body, cnvk.Z_ASCII)
        logging.debug("result: %s" % cnvk.convert(body, cnvk.Z_ASCII))

        logging.info("全角 to 半角 for %s" % title)
        calc_time(cnvk.convert, body, cnvk.H_ASCII)
        logging.debug("result: %s" % cnvk.convert(body, cnvk.H_ASCII))


def test_mojimoji():
    logging.info("=========================================")
    logging.info("=               mojimoji                =")
    logging.info("=========================================")
    test_cases = get_test_cases()
    for tc in test_cases:
        title = tc['title']
        body = tc['body']

        logging.info("ひらがな（全角） to カタカナ（全角） for %s" % title)
        logging.info("Not implemented")

        logging.info("カタカナ（全角） to ひらがな（全角） for %s" % title)
        logging.info("Not implemented")

        logging.info("ひらがな（全角） to カタカナ（半角） for %s" % title)
        logging.info("Not implemented")

        logging.info("半角 to 全角 for %s" % title)
        calc_time(mojimoji.han_to_zen, body)
        logging.debug("result: %s" % mojimoji.han_to_zen(body))

        logging.info("全角 to 半角 for %s" % title)
        calc_time(mojimoji.zen_to_han, body)
        logging.debug("result: %s" % mojimoji.zen_to_han(body))


def test_zenhan():
    logging.info("=========================================")
    logging.info("=               zenhan                  =")
    logging.info("=========================================")
    test_cases = get_test_cases()
    for tc in test_cases:
        title = tc['title']
        body = tc['body']

        logging.info("ひらがな（全角） to カタカナ（全角） for %s" % title)
        logging.info("Not implemented")

        logging.info("カタカナ（全角） to ひらがな（全角） for %s" % title)
        logging.info("Not implemented")

        logging.info("ひらがな（全角） to カタカナ（半角） for %s" % title)
        logging.info("Not implemented")

        logging.info("半角 to 全角 for %s" % title)
        calc_time(zenhan.h2z, body, zenhan.ASCII|zenhan.KANA|zenhan.DIGIT)
        logging.debug("result: %s" % zenhan.h2z(body, zenhan.ASCII|zenhan.KANA|zenhan.DIGIT))

        logging.info("全角 to 半角 for %s" % title)
        calc_time(zenhan.z2h, body, zenhan.ASCII|zenhan.KANA|zenhan.DIGIT)
        logging.debug("result: %s" % zenhan.z2h(body, zenhan.ASCII|zenhan.KANA|zenhan.DIGIT))


def test_rfzenhan():
    logging.info("=========================================")
    logging.info("=              rfZenHan                 =")
    logging.info("=========================================")
    test_cases = get_test_cases()
    for tc in test_cases:
        title = tc['title']
        body = tc['body']

        logging.info("ひらがな（全角） to カタカナ（全角） for %s" % title)
        logging.info("Not implemented")

        logging.info("カタカナ（全角） to ひらがな（全角） for %s" % title)
        logging.info("Not implemented")

        logging.info("ひらがな（全角） to カタカナ（半角） for %s" % title)
        logging.info("Not implemented")

        logging.info("半角 to 全角 for %s" % title)
        calc_time(rfZenHan.h2z, body)
        logging.debug("result: %s" % rfZenHan.h2z(body))

        logging.info("全角 to 半角 for %s" % title)
        calc_time(rfZenHan.z2h, body)
        logging.debug("result: %s" % rfZenHan.z2h(body))


def main():
    test_jaconv()
    test_cnvk()
    test_mojimoji()
    test_zenhan()
    test_rfzenhan()


if __name__ == '__main__':
    main()

# Python3 の日本語変換モジュール比較（第三者検証版）



##

https://qiita.com/yukinoi/items/42f8b5461dc1b62db7f9

## 比較対象

- [jaconv](https://github.com/ikegami-yukino/jaconv)
- [つまみ食う - 2010-12-13](http://d.hatena.ne.jp/mohayonao/20101213/1292237816)
- [cnvk](https://github.com/yuka2py/cnvk)
- [mojimoji](https://github.com/studio-ousia/mojimoji)
- [zenhan-py](https://github.com/MiCHiLU/zenhan-py/blob/master/zenhan.py)
- [rfZenHan](https://github.com/hATrayflood/rfZenHan)
- [python-nkf](https://github.com/fumiyas/python-nkf)


## 計測コード

### 基本コード（時間計測）

```python
import time

# 10万回繰り返す
N = 100000

def calc_time(func, **args):
    start = time.time()
    for i in range(0, N):
        func(**args)
    end = time.time()
    print("============\n%5.2f[s]============\n" % (func.__name__, end - start))
```

### テストケース

```python
def get_test_cases():
    return [
      {
        "title": "単語（漢字・平仮名のみ）",
        "body": "単語",
      },
      {
        "title": "単語（カタカナのみ)",
        "body": "タンゴ",
      },
      {
        "title": "単語（全角アルファベットのみ）",
        "body": "ｔａｎｇｏ",
      },
      {
        "title": "単語（半角アルファベットのみ）",
        "body": "tango",
      },
      {
        "title": "短文（漢字・平仮名のみ）",
        "body": "この文章には、片仮名は一文字も含まれていません",
      },
      {
        "title": "短文（カナカナのみ）",
        "body": "コノブンショウハカナカナノミデコウセイサレタタンブンデス",
      },
      {
        "title": "長文（漢字・平仮名のみ）",
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
```

### テスト関数

#### jaconv

```python
def test_jaconv():
    test_cases = get_test_cases()
    for tc in test_cases:
        title = tc['title']
        body = tc['body']

        print("平仮名（全角） to カタカナ（全角） with jaconv for %s" % title)
        calc_time(jaconv.hira2kata, body)

        print("カタカナ（全角） to 平仮名（全角） with jaconv for %s" % title)
        calc_time(jaconv.kata2hira, body)

        print("平仮名（全角） to 平仮名（半角） with jaconv for %s" % title)
        calc_time(jaconv.hira2hkata, body)

        print("半角 to 全角 with jaconv for %s" % title)
        calc_time(jaconv.h2z, body)

        print("全角 to 半角 with jaconv for %s" % title)
        calc_time(jaconv.z2h, body)
```

#### つまみ食う

```python
import re


def make_function_hiragana():
    re_katakana = re.compile(ur'[ァ-ヴ]')
    def hiragana(text):
        """ひらがな変換"""
        return re_katakana.sub(lambda x: unichr(ord(x.group(0)) - 0x60), text)
    return hiragana


def make_function_katakana():
    re_hiragana = re.compile(ur'[ぁ-&#12436;]')
    def katakana(text):
        """カタカナ変換"""
        return re_hiragana.sub(lambda x: unichr(ord(x.group(0)) + 0x60), text)
    return katakana


def test_tsumamiguu():
    test_cases = get_test_cases()
    hiragana = make_function_hiragana
    katakana = make_function_katakana

    for tc in test_cases:
        title = tc['title']
        body = tc['body']

        print("平仮名（全角） to カタカナ（全角） with jaconv for %s" % title)
        calc_time(hiragana, body)

        print("カタカナ（全角） to 平仮名（全角） with jaconv for %s" % title)
        calc_time(katakana, body)

        print("平仮名（全角） to 平仮名（半角） with jaconv for %s" % title)
        print("Not Implemented")

        print("半角 to 全角 with jaconv for %s" % title)
        print("Not Implemented")

        print("全角 to 半角 with jaconv for %s" % title)
        print("Not Implemented")
```

####
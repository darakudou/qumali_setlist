import csv
import json

import Levenshtein


def main():
    # csvを読む
    with open("data/qumaridepart_sounds.json", newline='') as f:
        sounds = json.load(f)


    with open("data/qumari_setlist.csv", newline='') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
            # ここで解析する
            res = analyze(row, sounds)
            print(row[0], res)

def analyze(row, sounds):
    """
    setlist情報を返す
    本当は日付とかその他の情報も返したいけど今はちょっと無理
    :param row:
    :param sounds:
    :return:
    """
    setlist = []
    for t in row[1].split("\\n"):
        now_distance = 99999
        now_sound = None
        # クマリで一番短いのはピアノなので短いモノは弾く
        # ピアノとメビウスが出安すぎる
        if len(t) < 2:
            continue
        for s in sounds:
            distance = Levenshtein.distance(t, s)
            jaro_distance = Levenshtein.jaro_winkler(t, s)
            if distance == 0:
                setlist.append(s)
                break
            elif distance < now_distance:
                now_distance = distance
                now_sound = s
        # 一旦距離があまりに遠いものはその他部分として入れない
        # 文字数が短いかつ距離が遠いものは外す
        if len(t) < 5 and now_distance > 4:
            continue
        if now_distance < 10:
            setlist.append(now_sound)
    return setlist


if __name__ == "__main__":
    main()
import csv
import json


def main():
    # csvを読む
    print("?")
    with open("data/qumaridepart_sounds.json", newline='') as f:
        sounds = json.load(f)


    with open("data/qumari_setlist.csv", newline='') as f:
        csvreader = csv.reader(f)
        for row in csvreader:
           # ここで解析する
           res = analyze(row, sounds)

def analyze(row, sounds):
    title = None
    date = None
    setlist = None
    other = None
    text = row[1]
    text.split("\n")
    for t in text:
        s = [s for s in sounds if s == t]





    return {"title": title, "date": date, "setlist":setlist, "other": other}


if __name__ == "__main__":
    main()
import os
from json import tool
from pprint import pprint

from PIL import Image, ImageEnhance
import pyocr


def main():
    # OCRエンジン取得
    tools = pyocr.get_available_tools()
    tool = tools[0]

    # OCRの設定 ※tesseract_layout=6が精度には重要。デフォルトは3
    builder = pyocr.builders.TextBuilder(tesseract_layout=6)

    # 解析画像読み込み
    img = Image.open('image/E5XxxzUVUAQJ0QN.jpeg')  # 他の拡張子でもOK

    # 適当に画像処理(何もしないと結構制度悪いです・・)
    # img_g = img.convert('L')  # Gray変換
    # enhancer = ImageEnhance.Contrast(img_g)  # コントラストを上げる
    # img_con = enhancer.enhance(2.0)  # コントラストを上げる

    # 画像からOCRで日本語を読んで、文字列として取り出す
    txt_pyocr = tool.image_to_string(img, lang='jpn', builder=builder)

    # 半角スペースを消す ※読みやすくするため
    txt_pyocr = txt_pyocr.replace(' ', '')
    pprint(txt_pyocr)


if __name__ == "__main__":
    main()
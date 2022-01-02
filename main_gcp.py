import csv
import glob
import io
import os
import pathlib

from PIL import Image, ImageEnhance, ImageDraw, ImageFont
from google.cloud import vision


def main():

    files = glob.glob("image/*")
    if not os.path.exists("data/qumari_setlist.csv"):
        _ = pathlib.Path("data/qumari_setlist.csv")
        _.touch()
    for file in files:
        # コントラストを上げる
        img = Image.open(file)
        enhancer = ImageEnhance.Contrast(img)
        img_enhanced = enhancer.enhance(2.0)
        # 変換した画像のbinary取得
        output = io.BytesIO()
        img_enhanced.save(output, format='JPEG')
        content = output.getvalue()

        image = vision.Image(content=content)

        client = vision.ImageAnnotatorClient()
        response = client.document_text_detection(
            image=image,
            image_context = {'language_hints': ['ja']}
        )
        text = get_text(response)
        # 読み取った文字だけの画像を貼る
        im2 = create_diff_image(img.width, img.height, response)
        # imageとim2を合体させた画像をつくる
        im3 = Image.new("RGB", (img.width * 2, img.height))
        im3.paste(img, box=(0,0))
        im3.paste(im2, (img.width, 0))
        im3.save(file.replace('image/', 'image_diff/'))

        out_csv(file+ "_enhance_0.5", text)


def out_csv(file, out_line):
    with open('data/qumari_setlist.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([file, repr(out_line)])


def create_diff_image(w, h, response):
    im = Image.new('RGB', (w, h), "white")
    draw = ImageDraw.Draw(im)
    # 二つ目の引数はfont size
    # これはMacの場合
    font = ImageFont.truetype('/System/Library/Fonts/ヒラギノ明朝 ProN.ttc', 40)
    # ページ→ブロック→段落→文?→char?
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for s in word.symbols:
                        x1 = s.bounding_box.vertices[0].x
                        y1 = s.bounding_box.vertices[0].y
                        x2 = s.bounding_box.vertices[2].x
                        y2 = s.bounding_box.vertices[2].y
                        y = y1 if y1 < y2 else y2
                        x = x1 if x1 < x2 else x2
                        # ここでfontを取り直してsizeを決めれたらいいかな...
                        draw.text(xy=(x, y), text=s.text, font=font, align="center", fill="black")
    return im

def get_text(response):
    output_text = ''
    # ページ→ブロック→段落→文?→char?
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for s in word.symbols:
                        output_text += s.text
                        if s.property.detected_break:
                            type = s.property.detected_break.type_
                            if type == vision.TextAnnotation.DetectedBreak.BreakType.EOL_SURE_SPACE:
                                output_text += "\n"
                            if type == vision.TextAnnotation.DetectedBreak.BreakType.LINE_BREAK:
                                output_text += "\n"
                            if type == vision.TextAnnotation.DetectedBreak.BreakType.SPACE:
                                output_text += " "
                            if type == vision.TextAnnotation.DetectedBreak.BreakType.SURE_SPACE:
                                output_text += " "
    return output_text


if __name__ == "__main__":
    main()
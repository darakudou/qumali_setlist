import csv
import glob
import os
import pathlib

from google.cloud import vision


def main():

    files = glob.glob("image/*")
    if not os.path.exists("data/qumari_setlist.csv"):
        _ = pathlib.Path("data/qumari_setlist.csv")
        _.touch()
    for file in files:
        client = vision.ImageAnnotatorClient()
        with open(file, 'rb') as image_file:
            content = image_file.read()
        image = vision.Image(content=content)
        response = client.document_text_detection(
            image=image,
            image_context = {'language_hints': ['ja']}
        )
        text = get_text(response)
        out_csv(file, text)


def out_csv(file, out_line):
    with open('data/qumari_setlist.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow([file, repr(out_line)])


def get_text(response):
    output_text = ''
    # ページ→ブロック→段落→語→記号
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
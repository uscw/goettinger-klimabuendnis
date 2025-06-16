from PIL import Image, ImageDraw, ImageFont
def text(input_image_path, output_path):
    image = Image.open(input_image_path)
    box = (0,0,500,500)
    region = image.crop(box)
    draw = ImageDraw.Draw(region)
    font = ImageFont.truetype("RobotoSlab-Bold.ttf", size=42)
    text = """
    Chihuly Exhibit
    Dallas, Texas"""
    draw.multiline_text((10, 25), text, font=font)
    # image.paste(region, box)
    region.save(output_path)
if __name__ == "__main__":
    text("/home/uschwar1/ownCloud/AC/html/hugo/goettinger-klimabuendnis/static/img/banner/2024-08-21-Zusammen-fuer-unsere-Zukunft.jpg", "out.jpg")


import random
from io import BytesIO

from PIL import ImageFilter, ImageDraw, Image, ImageFont


def check_code(width=120, height=30, char_length=5, font_file=r'C:\Users\ASUS\Desktop\厦门理工信息\字体\QingNiaoHuaGuangJianMeiHei\QingNiaoHuaGuangJianMeiHei\QingNiaoHuaGuangJianMeiHei-2.ttf', font_size=28):
    # 函数实现...
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    def rndChar():
        """
        生成随机字母
        :return:
        """
        return chr(random.randint(65, 90))

    def rndColor():
        """
        生成随机颜色
        :return:
        """
        return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255))

    # 写文字
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = rndChar()
        code.append(char)
        h = random.randint(0, 4)
        draw.text([i * width / char_length, h], char, font=font, fill=rndColor())

    # 写干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())

    # 写干扰圆圈
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())

    # 画干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)

        draw.line((x1, y1, x2, y2), fill=rndColor())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)


    # 使用 BytesIO 作为文件对象来保存图片
    buf = BytesIO()
    img.save(buf, 'PNG')  # 保存图片到 BytesIO 对象
    buf.close()

    # 返回图片的字节流和验证码字符串
    return img, ''.join(code)
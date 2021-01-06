import img2pdf
import os

dirname = "D:\\个人项目\\python_something\\anime_spider\\b\\"

with open("1.pdf", "wb") as f:
    imgs = []
    for chp in range(1, 54):
        page = 1
        while 1:
            fname = str(chp) + '_' + str(page) + '.jpg'
            if os.path.exists(dirname + fname):
                imgs.append(dirname + fname)
                page = page + 1
            else:
                break
    f.write(img2pdf.convert(imgs))
print("done")

import cv2
import numpy as np
import os
import matplotlib.pyplot as plt

def read_uploaded_file(file):
    try:
        contents = file.file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img
    except Exception as e:
        return None

def save_image(img, prefix):
    if not os.path.exists("static/images"):
        os.makedirs("static/images")
    filename = f"static/images/{prefix}_{np.random.randint(10000)}.png"
    cv2.imwrite(filename, img)
    return f"/{filename}"

def save_histogram(img, prefix, grayscale=True):
    if not os.path.exists("static/images"):
        os.makedirs("static/images")
    filename = f"static/images/{prefix}_{np.random.randint(10000)}.png"
    
    plt.figure(figsize=(6, 4))
    if grayscale:
        plt.hist(img.ravel(), 256, [0, 256], color='gray')
    else:
        colors = ('b', 'g', 'r')
        for i, col in enumerate(colors):
            hist = cv2.calcHist([img], [i], None, [256], [0, 256])
            plt.plot(hist, color=col)
    plt.savefig(filename)
    plt.close()
    return f"/{filename}"
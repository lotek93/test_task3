from pycocotools import coco
import numpy as np
import random
from tqdm import tqdm
import cv2
import os


DIR_DATA = './data/'
DIR_OUT = DIR_DATA + 'out/'
rgbAnnFile = DIR_DATA + 'aauRainSnow-rgb.json'
var_lapl_limit = 1.6  # threshold of laplacian variance


def get_var_laplacian(img):
    """ get laplacian variance for given image
    """
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img_resized = cv2.resize(img_gray, (140, 100), cv2.INTER_LANCZOS4)
    w, h = img_resized.shape[1], img_resized.shape[0]

    x, y = np.meshgrid(np.linspace(-1, 1, w), np.linspace(-1, 1, h))
    d = np.sqrt(x * x + y * y)
    sigma, mu = 1., 0.0
    gauss = np.exp(-((d - mu) ** 2 / (2.0 * sigma ** 2)))
    img2 = img_resized * gauss

    try:
        var_lapl = cv2.Laplacian(img2, cv2.CV_64F).var()
    except:
        var_lapl = 0

    return var_lapl, img2


def main():
    """ img_out: green bbox means vehicle is visible for optical cctv, 
        red bbox means vehicle is invisible for optical cctv
    """
    rainSnowRgbGt = coco.COCO(rgbAnnFile)

    if not os.path.exists(DIR_OUT):  # create output dir if it does not exist
        os.makedirs(DIR_OUT)

    print(f'saving labeled images into {DIR_OUT}')
    for i in tqdm(rainSnowRgbGt.imgs.keys()):
        annIds = rainSnowRgbGt.getAnnIds(imgIds=[i])
        anns = rainSnowRgbGt.loadAnns(annIds)

        rgbImg = rainSnowRgbGt.loadImgs([i])[0]
        img = cv2.cvtColor(cv2.imread(DIR_DATA + rgbImg['file_name']), cv2.COLOR_BGR2RGB)
    
        if len(anns) != 0:
            img_out = img.copy()
            for j in range(len(anns)):
                if anns[j]['area'] != 0:
                    x, y, w, h = anns[j]['bbox']
                    delta_x1, delta_x2, delta_y1, delta_y2 = -1, 1, -1, 1
                    if x == 0: delta_x1 = 0
                    if x + w == img.shape[1]: delta_x2 = 0
                    if y == 0: delta_y1 = 0
                    if y + h == img.shape[0]: delta_y2 = 0
                    img_bbox = img[y+delta_y1:y+h+delta_y2, x+delta_x1:x+w+delta_x2]

                    var_lapl, img_lapl = get_var_laplacian(img_bbox)
                
                    if var_lapl >= var_lapl_limit:
                        color = (0,255,0)  # green bbox
                    else:
                        color = (255,0,0)  # red bbox
                    img_out = cv2.rectangle(img_out, (x+delta_x1, y+delta_y1), (x+w+delta_x2, y+h+delta_y2), color)
                  
        cv2.imwrite(DIR_OUT + f'{i}.jpg', cv2.cvtColor(img_out, cv2.COLOR_RGB2BGR))


if __name__ == '__main__':
    main()

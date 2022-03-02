import cv2
import numpy as np
import matplotlib.pyplot as plt

def gammaCorrection(src, gamma):
    invGamma = 1 / gamma

    table = [((i / 255) ** invGamma) * 255 for i in range(256)]
    table = np.array(table, np.uint8)

    return cv2.LUT(src, table)
#

def show_img(img):
    # plt.figure(figsize=(15, 15))
    image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.imshow(image_rgb)
    plt.show()


def gaussian_noise(img, mean, sigma):
    # int -> float (標準化)
    img = img / 255.0
    # 隨機生成高斯 noise (float + float)
    noise = np.random.normal(mean, sigma, img.shape)
    # noise + 原圖
    gaussian_out = img + noise
    # 所有值必須介於 0~1 之間，超過1 = 1，小於0 = 0
    gaussian_out = np.clip(gaussian_out, 0, 1)

    # 原圖: float -> int (0~1 -> 0~255)
    gaussian_out = np.uint8(gaussian_out * 255)
    # noise: float -> int (0~1 -> 0~255)
    noise = np.uint8(noise * 255)

    return gaussian_out


origin_img = cv2.imread('nature.png')


gammaImg = gammaCorrection(origin_img, 2)  # 0.3可調

gaussian_img = gaussian_noise(origin_img, 0, 0.3)  # 0,0.3可調

gamma_gaussian_img = gaussian_noise(gammaImg, 0, 0.3)


show_img(origin_img)  # 原圖
show_img(gammaImg)  # gamma correction
show_img(gaussian_img)  # gaussian noise
show_img(gamma_gaussian_img)  # gamma + gaussian noise
# cv2.waitKey(0)
# cv2.imwrite('gammaImg.jpg', gammaImg)
# cv2.imwrite('guassian_img.jpg', guassian_img)
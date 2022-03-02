from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtWidgets import QFileDialog
import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt

# global filename, filetype
from transform_UI import Ui_MainWindow
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.selectpicture.clicked.connect(self.open_file)


    def open_file(self):
        gamma = self.ui.gummaSlider.value()
        gaussian = self.ui.gaussianSlider.value()
        #print(gamma)
        #print(gaussian)
        filename, filetype = QFileDialog.getOpenFileName(self,
                                                         "Open file",
                                                         "./")
        origin_img = cv2.imread(filename)

        def show_img(img):
            image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            plt.imshow(image_rgb)
            plt.show()

        if gamma != None and gaussian != None:
            #gamma
            gamma = gamma/100
            print("Gamma value(gamma):",gamma)

            invGamma = 1 / gamma
            table = [((i / 255) ** invGamma) * 255 for i in range(256)]
            table = np.array(table, np.uint8)
            gammaImg = cv2.LUT(origin_img, table)

            #gaussian
            gaussian = gaussian/100
            print("Gaussian value(sigma):",gaussian)
            # int -> float (標準化)
            img = gammaImg / 255.0
            # 隨機生成高斯 noise (float + float)
            noise = np.random.normal(0, gaussian, img.shape)
            # noise + 原圖
            gaussian_out = img + noise
            # 所有值必須介於 0~1 之間，超過1 = 1，小於0 = 0
            gaussian_out = np.clip(gaussian_out, 0, 1)
            # 原圖: float -> int (0~1 -> 0~255)
            gamma_gaussian_img = np.uint8(gaussian_out * 255)


            show_img(gamma_gaussian_img)
            cv2.imwrite('2.jpg', gamma_gaussian_img)
        else:
            show_img(origin_img)

    # def transform(self):
    #     origin_img = cv2.imread(filename)
    #     print(origin_img)
    #     gamma = self.ui.gummaSlider.value()
    #     print(gamma)
    #     gaussian = self.ui.gaussianSlider.value()
    #
    #     def show_img(img):
    #         # plt.figure(figsize=(15, 15))
    #         image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    #         plt.imshow(image_rgb)
    #         plt.show()
    #
    #     if gamma != 0:
    #         gamma = 1 / gamma
    #         invGamma = 1 / gamma
    #         table = [((i / 255) ** invGamma) * 255 for i in range(256)]
    #         table = np.array(table, np.uint8)
    #         gammaImg = cv2.LUT(origin_img, table)
    #         show_img(gammaImg)

















if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
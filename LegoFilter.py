from PIL import Image
import numpy as np
import sys
import os


class LegoFilter(object):
    """ 乐高滤镜对象 """
    def __init__(self):
        self.model_size = 40
        self.model_path = 'model.png'
        self.color_bit = 8

    def set_model_size(self, model_size):
        """
        设置乐高方块的大小
        """
        self.model_size = model_size
        return self

    def set_model_path(self, model_path):
        """ 设置乐高方块的路径 """
        self.model_path = model_path
        return self

    def set_color_bit(self, color_bit):
        """
        设置最终图像的颜色位数
        """
        self.color_bit = color_bit
        return self

    def handle(self, image_path):
        """
        处理图像
        """
        self.image = Image.open(image_path)
        num_x, num_y = self._crop()
        self._mean(num_x, num_y)

    def _crop(self):
        """
        切割图像，使其边长为乐高方块的整数倍
        """
        width, height = self.image.size
        num_x = width // self.model_size
        num_y = height // self.model_size
        width = num_x * self.model_size
        height = num_y * self.model_size
        self.image = self.image.crop((0, 0, width, height))
        return num_x, num_y

    def _mean(self, num_x, num_y):
        """
        对图像按照乐高方块尺寸进行平均化
        """
        # 从图像中载入颜色数组
        self.image_array = np.array(self.image).astype(np.int)
        # 为方块尺寸建立更短的别名
        l = self.model_size
        # 计算方块滤镜遮罩数组
        model_array = self._load_model()
        # 针对每个方块内的像素，分别对各个颜色通道取平均值
        for col in range(num_x):
            for row in range(num_y):
                block = self.image_array[row*l: (row+1)*l, col*l: (col+1)*l]
                mean = block.mean(0).mean(0).astype(np.int)
                # 色彩深度压缩
                color_sep_bit = 8 - self.color_bit + 1
                mean += 2 ** (color_sep_bit - 1)
                mean >>= color_sep_bit
                mean <<= color_sep_bit
                mean = np.where(mean, mean - 1, mean)
                self.image_array[row*l: (row+1)*l, col*l: (col+1)*l] = mean
                self.image_array[row*l: (row+1)*l, col*l: (col+1)*l] += model_array
        self.image_array = np.where(self.image_array < 0, 0, self.image_array)
        self.image_array = np.where(self.image_array > 255, 255, self.image_array)
        self.image_array = np.uint8(self.image_array)
        self.image = Image.fromarray(self.image_array)
        self.image.save('test.png')

    def _load_model(self):
        """
        载入并处理乐高方块
        """
        # 载入完整的乐高积木方块
        model_full = Image.open(self.model_path).convert('RGB')
        # 裁剪其中的四分之一
        self.model = model_full.crop((0, 0, model_full.size[0] // 2, model_full.size[1] // 2))
        # 缩放至标准大小
        self.model = self.model.resize((self.model_size, self.model_size), Image.ANTIALIAS)
        self.model_array = np.array(self.model).astype(np.int)
        mean = self.model_array.mean(2).astype(np.int)
        mean -= mean[-1, -1]
        # 处理边缘坡度光照效果
        mean[:2, :] += 10
        mean[-2:, :] -= 10
        mean[:, :2] -= 10
        mean[:, -2:] += 10
        # 光照放大因子
        mean *= 2
        # 重新扩展数组维度
        self.model_array = mean[:, :, np.newaxis]
        self.model_array = np.repeat(self.model_array, repeats=3, axis=2)

        return self.model_array


if __name__ == "__main__":
    legoFilter = LegoFilter()
    legoFilter.set_color_bit(8).set_model_size(40)
    legoFilter.handle('4.jpg')

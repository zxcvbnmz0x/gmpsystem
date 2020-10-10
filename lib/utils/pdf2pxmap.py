# -*- coding: utf-8 -*-

from PyQt5.QtGui import QImage, QPixmap

import fitz

# 把pdf内容转为pixmap
def render_pdf_page(page_data, zoom_width=0, zoom_height=0):
    # 图像缩放比例
    if zoom_width and zoom_height:
        zoom_matrix = fitz.Matrix(zoom_width, zoom_height)
    else:
        zoom_matrix = fitz.Matrix(3, 3)

    # 获取封面对应的 Pixmap 对象
    # alpha 设置背景为白色
    pagePixmap = page_data.getPixmap(
        matrix=zoom_matrix,
        alpha=False)
    # 获取 image 格式
    imageFormat = QImage.Format_RGB888
    # 生成 QImage 对象
    pageQImage = QImage(
        pagePixmap.samples,
        pagePixmap.width,
        pagePixmap.height,
        pagePixmap.stride,
        imageFormat)

    # 生成 pixmap 对象
    pixmap = QPixmap()
    pixmap.convertFromImage(pageQImage)
    return pixmap
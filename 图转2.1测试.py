# 导入相关的库
import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QPushButton, QComboBox, QFileDialog, QMessageBox)
from PyQt5.QtGui import QPixmap, QPainter, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PIL import Image

# ImageTransfer类继承自QWidget
class ImageTransfer(QWidget):
    def __init__(self):
        super().__init__()
        # 获取背景图片信息
        self.background_image = QPixmap("phototransfer.jpg")
        self.init_ui()

    def init_ui(self):
        # 垂直布局
        main_layout = QVBoxLayout()

        # 题头提示，本人GitHUb账号会持续更新本程序
        title_font = QFont()
        title_font.setPointSize(16)  # 设置字号大小
        title_label = QLabel('本程序是由个人开发用于期末作业，已同步上传至GitHub', self)
        title_label.setFont(title_font)  # 将设置好的字体应用到标签
        title_label.setStyleSheet("color: blue;")
        main_layout.addWidget(title_label)

        # 水平布局//使实现图片类型转换的功能放在一行排列
        # 后续如果加了新的功能（目前使准备加入裁剪图片的功能），会垂直布局到图片类型转换功能的下面一行
        h_layout = QHBoxLayout()

        # 给不懂图片类型区别的人介绍一下
        info_introduction = QPushButton('点击了解图片类型！', self)
        info_introduction.clicked.connect(self.introduction)
        h_layout.addWidget(info_introduction)

        # 初始化输出格式变量为"jpg"，表示默认的输出格式
        self.output_var = "jpg"
        # 创建列表来接受能转换的类型
        output_options = ['jpg', 'png', 'ico', 'bmp']

        # 创建一个下拉菜单，内容包括上面output_options里的元素
        self.output_menu = QComboBox(self)
        self.output_menu.addItems(output_options)
        h_layout.addWidget(self.output_menu)

        # 开始转换，按钮绑定函数transport
        transport_button = QPushButton('开始转换', self)
        transport_button.clicked.connect(self.transport)
        h_layout.addWidget(transport_button)

        # 将水平布局加入到窗口中
        main_layout.addLayout(h_layout)

        # 创建一个显示转换结果等相关信息的标签，初始内容为空
        self.result_label = QLabel("", self)
        main_layout.addWidget(self.result_label)

        # 将主布局设置给当前窗口，使得窗口按照该布局来显示各个控件
        self.setLayout(main_layout)

        # 设置窗口的标题为'图转'
        self.setWindowTitle('图转')
        # 设置窗口的初始位置（横坐标400，纵坐标400）和大小（宽479，高296）
        self.setGeometry(400, 400, 479, 296)

        # 设置窗口的图标，这里需要将"output.ico"替换为实际的图标文件路径
        self.setWindowIcon(QIcon("output.ico"))


    # 这个重写方法由ai完成
    def paintEvent(self, event):
        """
        重写paintEvent方法，用于绘制背景图片。
        这个方法在窗口需要重绘时（例如初次显示、窗口大小改变等情况）会被自动调用。
        """
        super().paintEvent(event)
        painter = QPainter(self)
        # 在窗口的整个矩形区域内绘制背景图片，使得背景图片覆盖整个窗口
        painter.drawPixmap(self.rect(), self.background_image)

    # 此方法也是由ai完成
    def resize_image(self, event):
        """
        当窗口大小改变时，更新背景图片的显示大小，保持图片的宽高比进行缩放，
        然后调用update方法触发窗口重绘，使得背景图片按照新的大小显示。
        """
        self.background_image = self.background_image.scaled(self.size(), Qt.KeepAspectRatioByExpanding)
        self.update()

    def introduction(self):
        # 定义一个包含图片类型介绍信息的字符串
        info_text = 'JPG 适合色彩丰富的照片，文件相对较小但有损压缩；\n' \
                    'PNG 支持透明背景，无损压缩；\n' \
                    'GIF 可用于简单动画，文件小；\n' \
                    'BMP 未压缩，文件较大但图像质量高。\n' \
                    'ICO 通常用于应用程序的图标。\n' \
                    '本程序暂不支持 GIF 相关的转换，敬请期待后续更新。\n'
        # 弹出一个信息框，显示图片类型介绍信息，标题为"图片类型介绍"
        QMessageBox.information(self, "图片类型介绍", info_text)

    def transport(self):
        # 弹出对话框，让用户选择需要转换类型的图片
        input_path, _ = QFileDialog.getOpenFileName(self, '请选择您要转换的图片', "", "All Files (*.*)")

        if not input_path:
            return

        try:
            # 使用PIL打开用户选择的图片文件
            image = Image.open(input_path)
            # 获取用户在下拉菜单中选择的输出格式
            output_type = self.output_menu.currentText()
            # 弹出目录选择对话框，让用户选择保存转换后图片的位置，返回选择的目录路径
            save_path = QFileDialog.getExistingDirectory(self, "选择保存位置")
            if not save_path:
                return

            # 根据用户选择的输出格式，执行相应的保存操作，并在结果标签中显示相应的转换成功提示信息
            if output_type == 'jpg':
                image.save(save_path + '/output.jpg')
                self.result_label.setText(f'已将您上传的图片转换为 jpg 格式，并保存到指定位置{save_path}。')

            elif output_type == 'png':
                image.save(save_path + '/output.png')
                self.result_label.setText(f'已将您上传的图片转换为 png 格式，并保存到指定位置{save_path}。')

            elif output_type == 'bmp':
                image.save(save_path + '/output.bmp')
                self.result_label.setText(f'已将您上传的图片转换为 bmp 格式，并保存到指定位置{save_path}。')

            elif output_type == 'ico':
                image.save(save_path + '/output.ico')
                self.result_label.setText(f'已将您上传的图片转换为 ico 格式，并保存到指定位置{save_path}。')

            else:
                self.result_label.setText('不支持的格式，请重新输入。')

        except Exception as e:
            # 如果在转换过程中出现异常，在结果标签中显示错误信息
            self.result_label.setText(f'发生错误：{e}')


# 启动窗口
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageTransfer()
    ex.show()
    sys.exit(app.exec_())
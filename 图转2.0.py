# 导入第三方库
import tkinter as tk
from tkinter import filedialog
from PIL import Image,ImageTk
# 创建
root = tk.Tk()
# 窗口命名
root.title('图转')
# 获取屏幕的高和宽
screen_height = root.winfo_screenheight()
screen_width = root.winfo_screenwidth()


# 加载背景图片
background_image = Image.open('phototransfer.jpg')
background_photo = ImageTk.PhotoImage(background_image)
background_label = tk.Label(root, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# 定义窗口的位置
root.geometry('479x296+{}+{}'.format(
    int(screen_width/2),
    int(screen_height/2),
    ))
root.iconbitmap('output.ico')
# 题头提醒
label_title = tk.Label(root,text='本程序仅供个人学习使用，不允许进行商业使用',
                       fg='blue',font=('宋体',10))
# 定位
label_title.grid()

# 自定义一个介绍函数1
def introduction():
    label_introduce = tk.Label(root,
                               text='JPG 适合色彩丰富的照片，文件相对较小但有损压缩；\n'
                                    'PNG 支持透明背景，无损压缩；\n'
                                    'GIF 可用于简单动画，文件小；\n'
                                    'BMP 未压缩，文件较大但图像质量高。\n'
                                    'ICO 通常用于应用程序的图标。\n'
                                    '本程序暂不支持 GIF 相关的转换，敬请期待后续更新。\n')
    label_introduce.grid()
    return label_introduce
#自定义转换函数
def transport():
    try:
        # filedialog.askopenfilename是一个用于弹出文件选择对话框的函数
        input_path = filedialog.askopenfilename(title='请选择您要转换的图片',
                                                filetypes=[('All Files', '*.*')])
        ''''filetypes=[("All Files", "*.*")]表示可以选择任何类型的文件
        通配符 “.” 表示所有文件'''
        if not input_path:
            return
        image = Image.open(input_path)
        output_type = output_var.get()
        # filedialog.askdirectory弹出一个目录选择对话框，让用户选择转换后的图片保存位置
        save_path = filedialog.askdirectory(title="选择保存位置")
        if not save_path:
            return
        # 开始转换
        if output_type == 'jpg':
            image.save(save_path + '/output.jpg')
            result_label.config(text='已将您上传的图片转换为 jpg 格式，并保存到指定位置。')
        elif output_type == 'png':
            image.save(save_path + '/output.png')
            result_label.config(text='已将您上传的图片转换为 png 格式，并保存到指定位置。')
        elif output_type == 'bmp':
            image.save(save_path + '/output.bmp')
            result_label.config(text='已将您上传的图片转换为 bmp 格式，并保存到指定位置。')
        elif output_type == 'ico':
            image.save(save_path + '/output.ico')
            result_label.config(text='已将您上传的图片转换为 ico 格式，并保存到指定位置。')
        else:
            result_label.config(text='不支持的格式，请重新输入。')
    except Exception as e:
        result_label.config(text=f'发生错误：{e}')

# 创建窗口内的第一个按钮，用来给用户科普图片的类型
info_introduction = tk.Button(root,text='了解图片类型',fg='red',command=introduction)
info_introduction.grid()

# 给转换阶段的函数里用到的变量进行定义
output_var = tk.StringVar()
# 创建一个列表
output_options = ['jpg','png','ico','bmp']
# 创建菜单
output_menu = tk.OptionMenu(root,output_var,*output_options)
# 定位到窗口上
output_menu.grid()
# 开始转换
transport_button = tk.Button(root,text='开始转换',command=transport)
# 定位到窗口上
transport_button.grid()

# 创建一个空文本标签
result_label = tk.Label(root, text="")
# 定位到窗口上
result_label.grid()
# 进入事件循环
root.mainloop()
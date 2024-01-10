"""
生信2101陈铠彬2021317210113
以下代码可实现在窗口程序中进行指定目录下特定文件类型的重命名、图片转PDF和搜索磁盘下含特定字符名称或特定类型的文件
"""




import os
import re
# 处理GUI
import tkinter as tk
from tkinter import filedialog
# 用于生成pdf
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
# 处理图像
from PIL import Image
# 获取时间
from time import strftime


class FileToolApp:
    def __init__(self, window):
        self.window = window
        self.window.title("文件工具")
        self.window.geometry("800x600")
        # 时钟部分
        self.update_clock()       

    def window_set(self):
        # 文件重命名部分组件设置
        rename_frame = tk.Frame(self.window)
        rename_frame.pack(pady=20)

        directory_label = tk.Label(rename_frame, text="选择目录:")
        directory_label.grid(row=0, column=0, padx=10, pady=8)

        directory_entry = tk.Entry(rename_frame, width=50)
        directory_entry.grid(row=0, column=1, padx=10, pady=8)

        browse_buttonA = tk.Button(rename_frame, text="浏览", command=lambda: self.browse_directory(directory_entry), width=15)
        browse_buttonA.grid(row=0, column=2, padx=10, pady=8)

        file_extension_label = tk.Label(rename_frame, text="文件类型:")
        file_extension_label.grid(row=1, column=0, padx=10, pady=8)

        file_extension_entry = tk.Entry(rename_frame, width=50)
        file_extension_entry.grid(row=1, column=1, padx=10, pady=8)

        new_name_label = tk.Label(rename_frame, text="输入新文件名")
        new_name_label.grid(row=2, column=0, padx=10, pady=8)

        new_name_entry = tk.Entry(rename_frame, width=50)
        new_name_entry.grid(row=2, column=1, padx=10, pady=8)

        rename_button = tk.Button(rename_frame, text="重命名", command=lambda: self.start_rename(directory_entry.get(), file_extension_entry.get(), new_name_entry.get()), width=15)
        rename_button.grid(row=2, column=2, padx=10, pady=5)

        # 图片转PDF部分组件设置
        pdf_frame = tk.Frame(self.window)
        pdf_frame.pack(pady=20)

        images_label = tk.Label(pdf_frame, text="图片列表:")
        images_label.grid(row=0, column=0, padx=10, pady=8)

        images_entry = tk.Entry(pdf_frame, width=50)
        images_entry.grid(row=0, column=1, padx=10, pady=8)

        browse_buttonB = tk.Button(pdf_frame, text="浏览", command=lambda: self.browse_photofiles(images_entry), width=15)
        browse_buttonB.grid(row=0, column=2, padx=10, pady=8)

        pdf_output_label = tk.Label(pdf_frame, text="PDF输出文件:")
        pdf_output_label.grid(row=1, column=0, padx=10, pady=8)

        pdf_output_entry = tk.Entry(pdf_frame, width=50)
        pdf_output_entry.grid(row=1, column=1, padx=10, pady=8)

        pdf_button = tk.Button(pdf_frame, text="转换为PDF", command=lambda: self.start_pdf_conversion(images_entry.get(), pdf_output_entry.get()), width=15)
        pdf_button.grid(row=1, column=2, padx=10, pady=8)

        # 文件搜索部分组件设置
        search_frame = tk.Frame(self.window)
        search_frame.pack(pady=20)

        search_directory_label = tk.Label(search_frame, text="搜索磁盘:")
        search_directory_label.grid(row=0, column=0, padx=10, pady=8)

        search_directory_entry = tk.Entry(search_frame, width=50)
        search_directory_entry.grid(row=0, column=1, padx=10, pady=8)

        search_name_label = tk.Label(search_frame, text="搜索文件:")
        search_name_label.grid(row=1, column=0, padx=10, pady=8)

        search_name_entry = tk.Entry(search_frame, width=50)
        search_name_entry.grid(row=1, column=1, padx=10, pady=8)

        search_button = tk.Button(search_frame, text="开始搜索文件", command=lambda: self.start_file_search(search_directory_entry.get(), search_name_entry.get()), width=20)
        search_button.grid(row=1, column=2, padx=10, pady=8)

        # 结果显示部分
        self.result_text = tk.Text(self.window, height=25, width=80)
        self.result_text.pack(pady=20)

    # 批量重命名特定类型文件
    def rename_files(self, directory, file_extension, new_name):
        try:
            n = 1
             # 检查文件类型是否存在
            matching_files = [filename for filename in os.listdir(directory) if filename.endswith(file_extension)]
            if not matching_files:
                self.result_text.config(state=tk.NORMAL)
                self.result_text.insert(tk.END, f"在指定目录中找不到类型为 {file_extension} 的文件\n")
                self.result_text.config(state=tk.DISABLED)
            else:
                # 遍历指定目录下文件列表
                for filename in matching_files:
                    # 统一命名与编号
                    new_filename = f"{new_name}_{n}.{file_extension}"
                    n += 1
                    # 构建原文件和新文件的完整路径
                    old_path = os.path.join(directory, filename)
                    new_path = os.path.join(directory, new_filename)
                    # 重命名文件
                    os.rename(old_path, new_path)
                # 输出结果开放编辑
                self.result_text.config(state=tk.NORMAL)
                self.result_text.insert(tk.END, "文件重命名完成！\n")
                # 输出结果不可编辑
                self.result_text.config(state=tk.DISABLED)

        # 处理异常信息，并输出显示
        except Exception as e:
            self.result_text.config(state=tk.NORMAL)
            self.result_text.insert(tk.END, f"无法更改文件名，出现以下错误：\n{e}\n")
            self.result_text.config(state=tk.DISABLED)

    # 图片转pdf
    def image_convert_pdf(self, myimages, output_pdf):
        # 创建ReportLab Canvas对象，用于生成PDF，指定输出pdf名和pdf大小
        c = canvas.Canvas(output_pdf, pagesize=letter)
        try:
            for myimage in myimages:
                # 打开图片文件
                img = Image.open(myimage)
                # 获取pdf页面宽度与高度
                pdf_width, pdf_height = letter
                # 获取图片宽度与高度
                img_width, img_height = img.size
                # 计算合适的缩放比例
                scale = min(pdf_width / img_width, pdf_height / img_height)
                # 设置图片在pdf中的水平和垂直位置
                in_x = (pdf_width - img_width * scale) / 2
                in_y = (pdf_height - img_height * scale) / 2
                # 在pdf上绘制图片
                c.drawInlineImage(img, in_x, in_y, width=img_width * scale, height=img_height * scale)
                # 在pdf上创建新页面
                c.showPage()
            # 保存生成的pdf文件
            c.save()

            self.result_text.config(state=tk.NORMAL)
            self.result_text.insert(tk.END, "图片转PDF完成！\n")
            self.result_text.config(state=tk.DISABLED)
        # 处理异常信息，并输出显示
        except Exception as e:
            self.result_text.config(state=tk.NORMAL)
            self.result_text.insert(tk.END, f"无法转换pdf，出现以下错误：\n{e}\n")
            self.result_text.config(state=tk.DISABLED)

    # 文件搜索
    def find_files(self, directory, target_name):
        result_files = []
        # 正则表达式进行文件名匹配
        refind = re.compile(target_name)

        try:
            # os.walk遍历指定目录及其子目录中所有文件
            for dirpath, dirnames, filenames in os.walk(directory, topdown=False):
                # 将匹配到的文件的绝对路径添加到result_files
                result_files.extend([os.path.abspath(os.path.join(dirpath, filename)) for filename in filenames if refind.search(filename)])

            # 如果找到匹配文件，显示前5个结果，少于5个则全部显示，并将匹配到文件的绝对路径结果写入txt文件中
            if result_files:
                self.result_text.config(state=tk.NORMAL)
                self.result_text.insert(tk.END, f"匹配文件如下：\n")
                for file in result_files[0:5]:
                    self.result_text.insert(tk.END, f"{file}\n")
                self.result_text.insert(tk.END, f"...\n共搜索到{len(result_files)}文件\n")
                # 写入txt文件
                with open("./find_files.txt","w") as f:
                    for file in result_files:
                        f.write(f"{file}\n")
                self.result_text.insert(tk.END, f"已将结果写入find_file.txt中\n")
                self.result_text.config(state=tk.DISABLED)
            # 如果未找到匹配文件，则输出提示
            else:
                self.result_text.config(state=tk.NORMAL)
                self.result_text.insert(tk.END, "未找到匹配文件\n")
                self.result_text.config(state=tk.DISABLED)
        # 处理异常信息，并输出显示
        except Exception as e:
            self.result_text.config(state=tk.NORMAL)
            self.result_text.insert(tk.END, f"发生错误：{e}\n")
            self.result_text.config(state=tk.DISABLED)
    # 选择目录
    def browse_directory(self, entry_widget):
        # 选择目录，并将其路径写入至文本输入框中
        directory = filedialog.askdirectory()
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, directory)

    # 执行文件重命名
    def start_rename(self, directory, file_extension, new_name):
        self.rename_files(directory, file_extension, new_name)

    # 选择一个或多个图片文件
    def browse_photofiles(self, entry_widget):
        # 选择文件
        photofiles = filedialog.askopenfilenames()

        # 获取当前已有的文件列表，并以;分隔
        current_files = entry_widget.get().split(";") if entry_widget.get() else []

        # 合并已有的文件列表和新选择的文件列表
        all_files = list(set(current_files + list(photofiles)))

        # 更新Entry中显示的文件列表
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, ";".join(all_files))

    # 执行图片转pdf
    def start_pdf_conversion(self, images_entry, output_pdf):
        # 用;分割文本输入框中的字符串，返回一个列表并将其做参数传给image_convert_pdf
        myimages = images_entry.split(";")
        self.image_convert_pdf(myimages, output_pdf)

    # 执行文件搜索
    def start_file_search(self, directory_entry, name_entry):
        # 将输入的磁盘名（如c，d等）转换成大写，方便构建路径
        search_directory = f"{directory_entry.upper()}:/"
        # 匹配含特定字符的文件和特定文件类型
        search_name = f".*{name_entry}.*"
        self.find_files(search_directory, search_name)

    # 更新时钟
    def update_clock(self):
        # 设置时间格式xx:xx:xx
        current_time = strftime('%H:%M:%S %p')
        # 将时间设置在窗口标题行
        self.window.title(f"工具  {current_time}")
        # 间隔1000毫秒(即1秒)调用一次时钟
        self.window.after(1000, self.update_clock)

    # 启动主事件循环，用于交互
    def execute(self):
        self.window.mainloop()


# 创建Tkinter窗口对象
window=tk.Tk()
# 传入window创建实例
mygui=FileToolApp(window)
# 设置窗口各种组件
mygui.window_set()
# 执行
mygui.execute()


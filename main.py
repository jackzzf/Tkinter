from tkinter import *
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pylab import mpl
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# 设置中文显示字体
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 中文显示
mpl.rcParams['axes.unicode_minus'] = False  # 负号显示


class Application(Frame):
    def __init__(self, master=None):
        """初始化方法"""
        super().__init__(master)  # 调用父类的初始化方法
        self.master_frame = master
        # self.pack(side=TOP, fill=BOTH, expand=1)  # 此处填充父窗体

        self.left_frame = None
        self.right_frame = None
        self.create_sub_frame(self.master_frame)

        self.canvas = None
        self.label = None
        self.list_box = None
        self.figure = None
        self.button_quit = None
        self.button_update = None

        # self.figure = self.create_matplotlib()
        self.figure = plt.figure()
        plt.text(0.2, 0.5, 'Modeling Analyzer', fontsize=40, color='green')
        plt.axis('off')  # 去掉坐标轴
        self.create_widget(self.figure)

    def create_sub_frame(self, father):
        self.left_frame = Frame(father, bd=1, relief="sunken")
        self.left_frame.pack(side=LEFT, fill=Y)
        self.right_frame = Frame(father, bd=1, relief="sunken")
        self.right_frame.pack(side=RIGHT, fill=BOTH, expand=1)

    def create_matplotlib(self):
        """创建绘图对象"""

        # 创建绘图对象fig, figsize的单位是英寸 像素 = 英寸*分辨率
        fig = plt.figure(num=1, figsize=(7, 4), dpi=80, facecolor="gold", edgecolor='green', frameon=True)
        ax = plt.subplot(1, 1, 1)  # 三个参数，依次是：行，列，当前索引
        x = np.arange(-2 * np.pi, 2 * np.pi, 0.1)
        y1 = np.sin(x)
        y2 = np.cos(x)

        line1 = ax.plot(x, y1, color='red', linewidth=2, label='y=sin(x)', linestyle='--')  # 画第一条线
        line2 = ax.plot(x, y2, color='green', label='y=cos(x)')
        plt.setp(line2, linewidth=1, linestyle='-', alpha=0.7)

        ax.set_title("曲线图", loc='center', pad=20, fontsize='xx-large', color='red')  # 设置标题
        # line1.set_label("正弦曲线")  # 确定图例
        # 定义legend 重新定义了一次label
        ax.legend(['正弦', '余弦'], loc='lower right', facecolor='orange', frameon=True, shadow=True, framealpha=0.7)
        ax.set_xlabel('(x)横坐标')  # 确定坐标轴标题
        ax.set_ylabel("(y)纵坐标")
        ax.set_yticks([-1, -1 / 2, 0, 1 / 2, 1])  # 设置y坐标轴刻度
        ax.grid(which='major', axis='x', color='gray', linestyle='-', linewidth=0.5, alpha=0.2)  # 设置网格

        return fig

    def update_plot(self):
        # 获取当前list box选择的item列表
        target_list = list(self.list_box.curselection())
        if len(target_list) == 0:
            return
        if target_list[0] == 0:
            # print(self.canvas.get_tk_widget().widgetName)
            self.canvas.get_tk_widget().destroy()

            x = np.linspace(-1, 1, 50)
            y1 = 2 * x
            y2 = x * x

            self.figure = plt.figure(facecolor="gold")
            ax1 = self.figure.add_subplot(1, 2, 1)
            ax1.plot(x, y1)
            ax2 = self.figure.add_subplot(1, 2, 2)
            ax2.plot(x, y2)

            self.canvas = FigureCanvasTkAgg(self.figure, master=self.right_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)
        elif target_list[0] == 1:
            # print(self.canvas.get_tk_widget().widgetName)
            self.canvas.get_tk_widget().destroy()

            x = np.linspace(-1, 1, 50)
            y1 = 2 * x

            self.figure = plt.figure(facecolor="gold")
            ax1 = self.figure.add_subplot(1, 1, 1)
            ax1.plot(x, y1)

            self.canvas = FigureCanvasTkAgg(self.figure, master=self.right_frame)
            self.canvas.draw()
            self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

    def create_widget(self, figure):
        """创建组件"""
        self.label = Label(master=self.right_frame, text='Modeling Analyzer Demo')
        self.label.pack()

        # 创建画布
        # print(self.children)
        self.canvas = FigureCanvasTkAgg(figure, master=self.right_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(side=TOP, fill=BOTH, expand=1)

        # 把matplotlib绘制图形的导航工具栏显示到tkinter窗口上
        toolbar = NavigationToolbar2Tk(self.canvas, self.right_frame)
        toolbar.update()
        self.canvas.get_tk_widget().pack(side=TOP, anchor="center", fill=BOTH, expand=1)

        # 创建 listBox
        target = ["1-IdVg_Vdthx", "2-IdVg_Vdd", "3-IdVd_Vb0", "4-IdVd_Vbb"]
        self.list_box = Listbox(master=self.left_frame, selectmode=EXTENDED, width=13, height=6)
        for i in target:
            self.list_box.insert(END, i)
        self.list_box.pack(side=TOP, anchor="center", padx=3, pady=(23, 3), fill=X)

        # 创建更新按钮
        self.button_update = Button(master=self.left_frame, text="更新", command=self.update_plot)
        self.button_update.pack(side=TOP, anchor="center", padx=3, pady=3, fill=X)

        # 创建退出按钮
        self.button_quit = Button(master=self.left_frame, text="退出", command=self.quit)
        self.button_quit.pack(padx=3, pady=3, side=BOTTOM, fill=X)

    def destroy(self):
        """重写destroy方法"""
        super().destroy()
        quit()

    def quit(self):
        """点击退出按钮时调用这个函数"""
        # for i in self.children.keys():
        #     print(i)  # 输出键
        #     print(self.children[i])  # 输出值
        #     print()
        root.quit()  # 结束主循环
        root.destroy()  # 销毁窗口


if __name__ == '__main__':
    root = Tk()
    root.title('Modeling Analyzer')
    # width * height + x + y
    root.geometry('1000x800+500+200')
    root.wm_attributes('-topmost', 1)

    app = Application(master=root)
    root.mainloop()

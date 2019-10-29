from tkinter import *
import main
import content_mysql
import os

class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        # self.pack()
        self.grid()     #使用grid布局
        self.createWidgets()    #每次创建实例就调用createWidgets函数

    def createWidgets(self):

        # 第一列，网站列表，选择网站，输入关键词
        # self.website_input.pack(fill = BOTH,side = 'left',padx = 0,pady = 0,ipadx = 100,ipady = 50)
        self.website_label01 = Label(self,text="可选择数据源的网站列表：").grid(row=0,column =0)
        self.website_Text = Label(self,bg='pink',wraplength = 150,justify = 'left',text ='网站列表...')
        self.website_Text.grid(row=1,column =0,ipadx =100,ipady =50)
        self.website_label02 = Label(self,text = "请输入网站编号，多个编号请用英文逗号','隔开，如需获取所有网站，请输入数字'0'：").grid(row=2 ,column=0)
        self.website_input = Entry(self)
        self.website_input.grid(row = 3,column = 0,ipadx = 100,ipady =10)
        self.keyword_label01 = Label(self, text="请输入关键词：").grid(row=4, column=0)
        self.keyword_input = Entry(self)
        self.keyword_input.grid(row = 5,column = 0,ipadx = 100,ipady =10)


        # 第二列，按钮列表
        self.website_button = Button(self, text='获取网站列表', command=self.get_website)
        self.website_button.grid(row=1, column=3)
        self.queren_button = Button(self, text='确认信息', command=self.queren)
        self.queren_button.grid(row=2, column=3)
        self.start_button = Button(self,text = '开始爬取',command=self.start)
        self.start_button.grid(row = 3,column = 3)
        self.topkey_button = Button(self, text='关键词分析', command=self.topkey)
        self.topkey_button.grid(row=4, column=3)
        self.emotion_button = Button(self, text='情感分析', command=self.emotion)
        self.emotion_button.grid(row=5, column=3)

        # 第三列
        # 确认窗口
        self.webs_label01 = Label(self,text="确认窗口").grid(row=0,column=5)
        self.webs_label02 = Label(self,bg = 'pink',text="aaa")
        self.webs_label02.grid(row = 1,column = 5,ipadx = 100,ipady =50)
        # 爬取结果窗口
        self.paqu_label01 = Label(self,text="爬取结果展示窗口").grid(row=2,column=5)
        self.paqu_label02 = Label(self,bg = 'pink',text="aaa")
        self.paqu_label02.grid(row = 3,column = 5, rowspan = 4,ipadx = 100,ipady =50)
        self.paqu_label03 = Label(self, bg='pink', text="aaa")
        self.paqu_label03.grid(row=5, column=5, rowspan=7, ipadx=100, ipady=50)

        # 退出
        self.quitButton = Button(self, text='Quit', command=self.quit)
        self.quitButton.grid(row = 10,column = 3)

        #空白布局
        self.nulla = Label(self).grid(row =0,column = 2,ipadx =5)
        self.nulla = Label(self).grid(row =0, column =4,ipadx =5)

    def get_website(self):
        # #要改的label、替换的图片，缺一不可都要global引用！，且grid()要独立出来
        global wensname
        websname = main.all_webname
        self.website_Text.config(text = websname)

    def queren(self):
        webs = self.website_input.get() or '网站'
        keyword = self.keyword_input.get() or '关键词'
        self.webs_label02.config(text = (webs,keyword))

    def start(self):
        input_list = self.website_input.get() or '0'
        keyword = self.keyword_input.get() or '关键词'
        main.gui_start(keyword,input_list)
        mkpath = os.getcwd() + '/' + keyword + '--爬取结果'
        count_path = mkpath + '/（统计）' + keyword + '.csv'
        all_path = mkpath + '/（总数据）' + keyword + '.csv'
        (id_list, name_list, nums_list, right_list) = content_mysql.open_count(keyword, count_path)
        (id_list, web_list, name_list, name2_list, time_list, url_list, data_list) = content_mysql.open_alldata(keyword, all_path)
        self.paqu_label02.config(text = (id_list, name_list, nums_list, right_list))
        self.paqu_label03.config(text=(id_list, web_list, name_list, name2_list, time_list, url_list, data_list))

    def topkey(self):
        pass

    def emotion(self):
        pass

app = Application()

# 设置窗口标题:
app.master.title('Hello World')
app.master.geometry('1000x500')                     # 设置窗口大小
# app.master["bg"] = "blue"
# 主消息循环:
app.mainloop()
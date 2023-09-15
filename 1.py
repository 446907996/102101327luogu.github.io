import requests
from bs4 import BeautifulSoup
import re
import urllib.parse
import os
from tkinter import Tk, Label, StringVar, ttk, Button, Entry, Text
import tkinter as tk
baseurl = "https://www.luogu.com.cn/problem/P"
savePath = "E:\软件工程\洛谷题库\\"
blogurl = "https://www.luogu.com.cn/blog/_post/"
listurl = "https://www.luogu.com.cn/problem/list"
solutionurl = "https://www.luogu.com.cn/problem/solution/P"
minn = 1000
maxn = 1049            #最大题号

def fun():
    print("计划爬取到P{}".format(maxn))
    t_list=[]
    get_titles(listurl, t_list)
    dif_list = get_dif(listurl)

    for i in range(minn, maxn+1):
        print("正在爬取P{}...".format(i), end="")
        text_output.insert(tk.END, "正在爬取P" + str(i) + "\n")
        key_list = []
        slice(t_list[i - 1000], key_list)
        dif = dif_turn(dif_list[i - 1000])
        phtml = get_baseHTML(baseurl + str(i))
        shtml = get_solutionHTML(solutionurl + str(i))
        if phtml == "error":
            print("爬取失败，可能是不存在该题或无权查看")
        else:
            problem = get_baseMD(phtml)
            solution = get_solutionMD(shtml)
            print("爬取成功！正在保存...", end="")
            text_output.insert(tk.END, "爬取成功！正在保存..."+"\n")
            if key_list:
                born_file(savePath + dif + "-" + key_list[0] + "-" + key_list[1])
                path = savePath + dif + "-" + key_list[0] + "-" + key_list[1] + "\\"
            else:
                born_file(savePath + dif)
                path = savePath + dif + "\\"
            born_file(path + "P" + str(i) + "--" + t_list[i - 1000])
            new_path = path + "P" + str(i) + "--" + t_list[i - 1000] + "\\"
            saveData(problem, new_path + "P" + str(i) + "--" + t_list[i - 1000] + ".md")
            saveData(solution, new_path + "P" + str(i) + "--" + t_list[i - 1000] + "题解" + ".md")
            print("保存成功!")
            text_output.insert(tk.END, "保存成功!" + "\n")
# 模拟用户访问浏览器
def get_html(url):

   headers = {
      "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 SLBrowser/8.0.1.4031 SLBChan/103",
      "cookie": "__client_id=af4215a6f73e4641a2ae5ed49f35ef0b93b0709b; login_referer=https%3A%2F%2Fwww.luogu.com.cn%2Fauth%2Flogin; _uid=664601; C3VK=a66952"
   }
   response = requests.get(url=url, headers=headers)
   return response.text

# 获取洛谷题库信息
def get_baseHTML(url):
   basehtml = get_html(url)
   return basehtml

#将题目信息转化为md格式
def get_baseMD(html):
   bs = BeautifulSoup(html, "html.parser")
   core = bs.select("article")[0]
   md = str(core)
   md = re.sub("<h1>", "# ", md)
   md = re.sub("<h2>", "## ", md)
   md = re.sub("<h3>", "#### ", md)
   md = re.sub("</?[a-zA-Z]+[^<>]*>", "", md)
   return md
# 获取题解信息
def get_solutionHTML(url):
   solutionhtml = get_html(url)
   key = get_postfix(solutionhtml)
   new_url = solutionurl + key
   new_solutionhtml = get_html(new_url)
   return new_solutionhtml
#获得博客后缀
def get_postfix(text):
   pattern = r"%22id%22%3A(\d+)"
   match = re.search(pattern, text)
   if match:
      return match.group(1)
   return None

#将题解网页转化为md格式
def get_solutionMD(html):
   core = BeautifulSoup(html, "html.parser")
   md = str(core)
   md = re.sub("<h1>", "# ", md)
   md = re.sub("<h2>", "## ", md)
   md = re.sub("<h3>", "#### ", md)
   md = re.sub("</p>", "<br>", md)
   return md
# 生成文件夹
def born_file(name):
   if not os.path.exists(name):
      os.mkdir(name)

#获取题目关键词
def slice(t_list, key_list):
   if t_list[0] == "[":
      key_list.append(t_list[1:5] + t_list[10:13])
      key_list.append(t_list[5:9])


#获取标题列表
def get_titles(url, t_list):
   thtml = get_html(url)
   soup = BeautifulSoup(thtml, "html.parser")
   all_titles = soup.findAll("li")
   for title in all_titles:
      name = title.find("a")
      t_list.append(name.string)



def dif_turn(dif):
   if dif == "1":
      d = "入门"
   elif dif == "2":
      d = "普及-"
   elif dif == "3":
      d = "普及&提高-"
   elif dif == "4":
      d = "普及+&提高"
   elif dif == "5":
      d = "提高+&省选-"
   elif dif == "6":
      d = "省选&NOI-"
   else:
      d = "NOI&NOI+&CTSC"
   return d
def get_dif(url):
   thtml = get_html(url)
   text = urllib.parse.unquote(thtml)
   pattern = r'"difficulty":(\d)'
   numbers = re.findall(pattern, text)
   return numbers
#存储md文件
def saveData(data, filename):
   file = open(filename, "w", encoding="utf-8")
   for d in data:
      file.writelines(d)
   file.close()



def on_select(event):
    selected_item = event.widget.get()
    print(f"Selected item: {selected_item}")

window = Tk()

# 设置窗口大小
window.geometry("600x400")

# 创建筛选框
selection_var1 = StringVar(window)
selection_combobox1 = ttk.Combobox(window, textvariable=selection_var1)

selection_var2 = StringVar(window)
selection_combobox2 = ttk.Combobox(window, textvariable=selection_var2)

selection_var3 = StringVar(window)
selection_combobox3 = ttk.Combobox(window, textvariable=selection_var3)

# 设置选项列表
selection_combobox1['values'] = ('2000', '2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023')
selection_combobox2['values'] = ('入门', '普及-', '普及/提高-','普及+/提高','提高+/省选-','省选/NOI-','NOI/NOI+/CTSC')
selection_combobox3['values'] = ('Option 1', 'Option 2', 'Option 3')

# 绑定选择事件
selection_combobox1.bind("<<ComboboxSelected>>", on_select)
selection_combobox2.bind("<<ComboboxSelected>>", on_select)
selection_combobox3.bind("<<ComboboxSelected>>", on_select)

# 显示筛选框
selection_combobox1.grid(row=0, column=1, padx=10, pady=10, sticky='w')
selection_combobox2.grid(row=1, column=1, padx=10, pady=10, sticky='w')
selection_combobox3.grid(row=2, column=1, padx=10, pady=10, sticky='w')

# 创建标签
label1 = Label(window, text="年份")
label2 = Label(window, text="难度")
label3 = Label(window, text="关键字")

# 显示标签
label1.grid(row=0, column=0, padx=10, pady=10, sticky='w')
label2.grid(row=1, column=0, padx=10, pady=10, sticky='w')
label3.grid(row=2, column=0, padx=10, pady=10, sticky='w')

# 创建文本框
text_output = Text(window, width=40, height=10)  # 设置初始宽度和高度
text_output.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky='w')




# 创建按钮
button = Button(window, text="启动", command=fun)

# 设置按钮的位置
button.grid(row=0, column=2, padx=10, pady=10, sticky='w')

window.mainloop()

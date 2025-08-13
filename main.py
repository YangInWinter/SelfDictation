import os
import json
from datetime import datetime
from os.path import getsize

# 类：单词列表
class WordList:
    def __init__(self):
        self.words = []
        self.trans = {}

    def add_word(self, word, meaning=""):
        """
        添加单词，及其对应的翻译。\n
        参数：\n
        word：需要增添的单词。\n
        meaning：单词对应的释义。
        """
        if not (word in self.words): # 如果单词表中存在该单词，则只更改单词的释义
            self.words.append(word)
        self.trans[word] = meaning

    def remove_word(self, item):
        """
        移除单词，及其对应的翻译。\n
        参数：\n
        item：可为索引（int）或单词（str）。
        """
        try:
            # 判断参数item类型再操作
            if is_convertible_to_int(item): # 如果item是数字
                item = int(item) - 1 # 转换item为索引
                del self.trans[self.words[item]]
                del self.words[item]
            else: # 如果item是字符串
                del self.trans[item]
                self.words.remove(item)
        except Exception as error:
            print(f"不存在该项目，详细错误信息如下：{str(error)}")

# 类：命令
class Commands():
    def __init__(self):
        self.cmd = {}
        self.wordlist = WordList()

    def parse(self, cmd):
        """
        解析命令，以字典的形式返回结果。\n
        解码后字典的结构：\n
        {"cmd":"命令", "-a":"参数a的输入（如果没有则为空）", "-b":"同理为参数b的输入"}
        """
        res = {} # 初始化返回列表
        parse_list = cmd.split() # 将输入以空格分割到列表
        # 遍历列表进行解析
        # 第一个单词为命令名称
        if not not parse_list:
            res["cmd"] = parse_list[0]
        option_name = "-param" # 默认将选项名称设为“-param”
        for content in parse_list[1:]: # 忽视已设为命令名称的第一项
            if content[0] == '-': # 参数以“-”开头
                option_name = content
            else:
                if not(option_name in res): # 判断是否存在该项
                    res[option_name] = str(content)
                else:
                    res[option_name] += ' ' + str(content)
        return res

    def add(self):
        """ 增添单词。 """
        # 遍历输入单词
        while True:
            content = input(f"{len(self.wordlist.words)+1}. ")
            if content == '':
                break
            # 判断是否输入了单词的释义，用“:”或“：”(全半角都行)分隔单词和释义
            if (':' in content) or ('：' in content): 
                try:
                    word = format(incise(content, ':' if (':' in content) else '：', 'b'))
                    meaning = format(incise(content, ':' if (':' in content) else '：', 'f'))
                    self.wordlist.add_word(word, meaning)
                except Exception as error:
                    print(f"错误：{str(error)}")
            else:
                self.wordlist.add_word(content)

    def remove(self, content:str):
        """
        通过输入单词或索引，移除单词表中的单词。\n
        参数：\n
        content：一系列需要移除的东西，以空格分开。
        """
        items = content.split()
        for item in items:
            self.wordlist.remove_word(item)

    def showlist(self):
        """ 逐一展示单词表。 """
        i = 1
        for word in self.wordlist.trans:
            print(f"{str(i)}. {word}: {self.wordlist.trans[word]}")
            i += 1

    def test(self, mode):
        """
        测试（默写），本程序最主要的内容。\n
        测试时，会给出单词/翻译，按enter直接下一个，按“?”给出一个字的提示，输入答案进行验证检测。\n
        参数：\n
        mode：可填“-s”，显示翻译，测试拼写。也可填“-t”，显示单词，测试翻译。
        """
        # 显示翻译
        if mode == "-s":
            i = 1
            for word in self.wordlist.trans:
                print(f"{i}. {self.wordlist.trans[word]}")
                hints = 1 # 提示的字母位置
                while True:
                    content = input()
                    if content == '': # 显示下一个
                        break
                    elif (content == "?") or (content == "？"): # 如果输入是“?”就给提示
                        print(f"前{hints}个字母是：{word[:hints]}") # 给出提示
                        hints += 1
                    elif format(content) == word: # 输入（可选）完全正确的情况
                        print("拼写正确！")
                        break
                    else:
                        print("拼写错误！")
                    if hints > len(word): # 提示完成时，退出测试
                        break
                print(f"这个单词是：{word}")
                i += 1
        # 显示单词
        elif mode == "-t":
            i = 1
            for word in self.wordlist.trans:
                trans = self.wordlist.trans[word]
                print(f"{i}. {word}")
                hints = 1 # 提示的字母位置
                while True:
                    content = input()
                    if content == '': # 显示下一个
                        break
                    elif (content == "?") or (content == "？"): # 如果输入是“?”就给提示
                        print(f"前{hints}个字是：{trans[:hints]}") # 给出提示
                        hints += 1
                    elif format(content) == trans: # 输入（可选）完全正确的情况
                        print("回答正确！")
                        break
                    else:
                        print("回答错误！")
                    if hints > len(word): # 提示完成时，退出测试
                        break
                print(f"这个单词的释义是：{trans}")
                i += 1

    def export(self, filepath=""):
        """
        导出为文件，包含路径和文件名。\n
        参数：\n
        filepath：（可选）文件保存的地址（包含文件名）。如果留空，则使用默认保存方式。
        """
        if filepath == "": # 默认保存方式
            # 判断默认路径是否存在
            if not os.path.exists("./data"):
                os.makedirs("./data")
            # 如果未给出命名方式，则以时间命名
            now = datetime.now()
            filename = now.strftime("%Y-%m-%d-%H-%M-%S")
            filepath = f"./data/{filename}.json"
        # 写入文件
        try:
            with open(filepath,'w', encoding="utf-8") as file:
                json.dump(self.wordlist.trans, file, ensure_ascii=False, indent=4)
            print(f"文件已保存在：{os.path.abspath(filepath)}")
        except Exception as error: # 出错情况
            if not os.path.exists(os.path.dirname(filepath)): # 判断最可能的原因：目录不存在
                print(f"目录不存在！错误：{error}")
                option = input("是否创建目录？（Y/n）") # 提醒是否创建父文件夹
                option = option.lower()
                if  (option == '') or ('y' in option) or (option == None):
                    os.makedirs(os.path.dirname(filepath), exist_ok=True)
                with open(filepath,'w', encoding="utf-8") as file:
                    json.dump(self.wordlist.trans, file, ensure_ascii=False, indent=4)
                print(f"文件已保存在：{os.path.abspath(filepath)}")
            else:
                print(f"错误：{error}")

    def import_data(self, filepath):
        """ 用于导入数据文件（json格式）。 """
        try:
            with open(filepath, 'r', encoding="utf-8") as file:
                # 询问是否保存当前单词表
                if not not self.wordlist.trans: # 判断单词表是否为空
                    option = input("是否保存当前单词表？（Y/n）")
                    option = option.lower()
                    if  (option == '') or ('y' in option) or (option == None):
                        self.export(input("保存目录（留空则选择默认目录）："))
                self.wordlist.trans = json.load(file) # 加载到trans字典
                self.wordlist.words = list(self.wordlist.trans) # 加载到words列表
                print("已加载文件。")
        except FileNotFoundError:
            print(f"错误：文件 '{filepath}' 不存在。")
        except json.JSONDecodeError:
            print(f"错误：文件 '{filepath}' 不是有效的JSON格式。")
        except Exception as error:
            print(f"处理文件时发生错误：{error}")

    def save_dict(self, dictpath='./data/dict/default.json'):
        """
        存储(self.wordlist.trans)至词典(.json文件)。\n
        参数：\n
        dictpath：可选，默认路径为“./data/dict/default.json”，需包含路径和文件名。
        """
        odict = {} # Output Dictionary
        try:
            if not os.path.exists(os.path.dirname(dictpath)): # 判断目录是否存在
                print("目录不存在！")
                option = input("是否创建目录？（Y/n）") # 提醒是否创建父文件夹
                option = option.lower()
                if  (option == '') or ('y' in option) or (option == None):
                    os.makedirs(os.path.dirname(dictpath), exist_ok=True)

            # 判断文件是否存在且不为空
            if os.path.exists(dictpath) and os.path.getsize(dictpath) > 0:
                with open(dictpath, 'r', encoding='utf-8') as dictfile:
                    odict = json.load(dictfile)
                with open(dictpath,'w', encoding="utf-8") as file:
                    odict.update(self.wordlist.trans)
                    json.dump(odict, file, ensure_ascii=False, indent=4)
                    print(f"文件已保存在：{os.path.abspath(dictpath)}")
            else:
                with open(dictpath,'w', encoding="utf-8") as file:
                    odict = self.wordlist.trans
                    json.dump(odict, file, ensure_ascii=False, indent=4)
                    print(f"文件已保存在：{os.path.abspath(dictpath)}")

        except Exception as error:
            raise RuntimeError(f"保存为词典时发生错误：{error}")

    def load_dict(self, dictpath='./data/dict/default.json'):
        """
        加载词典至:self.wordlist.trans\n
        参数：\n
        dictpath：可选，默认为“./data/dict/default.json”，需包含路径和文件名。
        """
        try:
            # 询问是否保存当前单词表
            if not not self.wordlist.trans: # 判断单词表是否为空
                option = input("是否保存当前单词表？（Y/n）")
                option = option.lower()
                if (option == '') or ('y' in option) or (option == None):
                    self.export(input("保存目录（留空则选择默认目录）："))

            with open(dictpath, 'r', encoding='utf-8') as dictfile:
                self.wordlist.trans = json.load(dictfile)
            print("已加载词典。")
        except FileNotFoundError as error:
            raise FileNotFoundError(f"文件不存在！详细信息：{error}")
        except Exception as error:
            raise RuntimeError(f"加载词典时发生错误：{error}")



    def run(self, typed):
        """
        输入命令的内容（原封不动），解析后执行。\n
        参数：\n
        typed：命令的内容（原封不动）。
        """

        # 必须考虑输入为空的情况，否则会报错退出
        if typed == '':
            return None

        # 解析typed（输入的内容）
        self.cmd = self.parse(typed)

        # 增添单词列表
        if self.cmd["cmd"] == "add":
            self.add()

        # 移除单词项
        elif self.cmd["cmd"] == "rm":
            self.remove(self.cmd["-param"])

        # 显示单词列表
        elif self.cmd["cmd"] == "ls":
            self.showlist()

        # 测试（显示释义）
        elif typed == "tst -s":
            self.test("-s")

        # 测试（显示单词）
        elif typed == "tst -t":
            self.test("-t")

        # 导出为文件，包含路径和文件名
        elif self.cmd["cmd"] == "exp":
            if "-param" in self.cmd:
                self.export(self.cmd["-param"])
            else:
                self.export()

        # 导入文件，包含路径和文件名
        elif self.cmd["cmd"] == "imp":
            self.import_data(self.cmd["-param"])

        # 保存词典。“-p”为可选项，用于指定路径；不选择“-p”，直接写参数的，以参数为文件名保存至“./data/dict/”；不写参数的，直接保存至“./data/dict/default.json”
        elif self.cmd["cmd"] == "save":
            try:
                if "-p" in self.cmd:
                    self.save_dict(self.cmd["-p"])
                elif "-param" in self.cmd:
                    self.save_dict(f"./data/dict/{self.cmd["-param"]}.json")
                else:
                    self.save_dict()
            except Exception as error:
                print(error)

        # 载入词典。“-p”为可选项，用于指定路径；不选择“-p”，直接写参数的，以参数为文件名从“./data/dict/”寻找；不写参数的，直接从“./data/dict/default.json”加载
        elif self.cmd["cmd"] == "load":
            try:
                if "-p" in self.cmd:
                    self.load_dict(self.cmd["-p"])
                elif "-param" in self.cmd:
                    self.load_dict(f"./data/dict/{self.cmd["-param"]}.json")
                else:
                    self.load_dict()
            except Exception as error:
                print(error)

        # 退出程序
        elif self.cmd["cmd"] == "exit":
            # 询问是否保存当前单词表
            if not not self.wordlist.trans: # 判断单词表是否为空
                option = input("是否保存当前单词表？（Y/n）")
                option = option.lower()
                if (option == '') or ('y' in option) or (option == None):
                    self.export(input("保存目录（留空则选择默认目录）："))
            os._exit(0)

        # 未知命令
        else:
            print(f"未知命令：{typed}")



# 通用函数
def format(text):
    """ 用于去除首尾及重复的空格。 """
    # 1. 去除首尾空格（使用 strip()）
    stripped = text.strip()
    # 2. 处理中间的重复空格（先按空格分割，再用单个空格拼接）
    cleaned = ' '.join(stripped.split()) # split() 无参数时，会自动将连续空格视为分隔符，返回非空元素列表
    return cleaned

def incise(text, separator, range):
    """
    返回字符串（text）分隔符（seperator）后的内容。\n
    参数：\n
    text：需要分割的字符串。\n
    seperator：分割符。\n
    range：范围，可以填“f”（forward，分隔符之后的内容）或“b”（backward，分隔符之前的内容）。
    """
    sep_index = text.find(separator)
    if sep_index != -1:
        if range == 'f':
            return text[sep_index+1:]
        elif range == 'b':
            return text[:sep_index]
    else:
        return ValueError(f"未找到符号“{separator}”！分隔符索引错误。")

def is_convertible_to_int(content):
    """ 判断字符串是否能转换为整型。 """
    try:
        int(content)
        return True
    except ValueError:
        return False



if __name__ == "__main__":
    # 创建实例
    cmd = Commands()

    # 主循环
    while True:
        # 输入命令
        typed = input("(Self Dictation)>>> ")

        # 使用cmd
        cmd.run(typed)


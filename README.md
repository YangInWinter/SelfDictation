# Self Dictation

这是一个用于自我听写的软件，以便**单人完成听写**。使用终端，通过**命令的形式**进行交互，完成单词表的编辑、双语言的测试、词典的导入/导出等。

## 目录

- [安装步骤](#安装步骤)
- [使用方法](#使用方法)
- [版权声明](#版权声明)


## 安装步骤

### (1) 安装Python 

该项目依赖于**Python3**及其内置库，所以安装Python即可。以下是Python下载方式：

- [Python官方下载页面](https://www.python.org/downloads/)：信任**官方**的用户可点击此链接，从官网下载，缺点是**速度慢**。
- [Python华为镜像](https://mirrors.huaweicloud.com/python/)：国内追求**下载速度**的用户可以从华为云下载。

### (2) 克隆仓库

- 通过**Git**克隆：

  在**命令行/终端**执行：
``` bash
git clone git@github.com:YangInWinter/SelfDictation.git
```

- 通过**ZIP**包下载：

  点击链接：[https://github.com/YangInWinter/SelfDictation/archive/refs/heads/main.zip](https://github.com/YangInWinter/SelfDictation/archive/refs/heads/main.zip)

### (3) 运行

进入项目根目录，在**终端/命令行**执行：

```bash
python3 main.py
```

## 使用方法

该程序通过**命令的形式**进行交互。在执行`main.py`后，你应该会看见以下界面：

```
(Self Dictation)>>> 
```

以下是受支持的命令：

### 1. add

格式：`add`

说明：执行（按下回车）后，终端会显示一个序号（序号为单词表的新一项），在序号之后，你可以输入单词（或词组、句子）。如果想输入释义，请紧随其后输入`:`冒号（全半角都行）并输入释义。在键入时，按下回车确认，并开始输入下一项；在新的一项（即该项为空时）按下回车，则结束添加行为。

示例：

```
(Self Dictation)>>> add
1. self: 自己
2. dictation: 听写
3. 
(Self Dictation)>>> 
```

### 2. ls

格式：`ls`

说明：按序号列出单词表。

示例：

```
(Self Dictation)>>> ls
1. self: 自己
2. dictation: 听写
```

### 3. rm

格式：`rm [项目1] [项目2] ...`

说明：项目可以为单词在单词表中的序号，也可以是单词本身（要求绝对匹配）。

示例：

```
(Self Dictation)>>> ls
1. self: 自己
2. dictation: 听写
3. other: 其他的
(Self Dictation)>>> rm 1 dictation
(Self Dictation)>>> ls
1. other: 其他的
```

### 4. tst

格式：`tst [选项]`

说明：这是本项目的主要功能，用于测试对单词的掌握（即听写），现支持两种选项。

**-s**	(spelling) 显示释义，默写单词（测试拼写）。

**-t**	(translation) 显示单词，默写释义。

听写时，有以下几个操作方式。

**?**	(全半角都行) 显示下一个字符的提示。

**enter**	(回车) 显示答案，听写下一个。 

**[单词/释义]**	输入你的答案，检测对不对。

示例：

```
(Self Dictation)>>> tst -t
1. self
自己
回答正确！
这个单词的释义是：自己
2. dictation
?
前1个字是：听
?
前2个字是：听写

这个单词的释义是：听写
3. other
其他
回答错误！
其他的
回答正确！
这个单词的释义是：其他的
```

```
(Self Dictation)>>> tst -s
1. 自己
self
拼写正确！
这个单词是：self
2. 听写
?
前1个字母是：d
?
前2个字母是：di
?
前3个字母是：dic

这个单词是：dictation
3. 其他的
others
拼写错误！

这个单词是：other
```

### 5. exp

用法：`exp [路径(选)]`

说明：导出单词表至json文件。“路径”选项选填，需包含文件路径与文件名；默认以时间命名(年份-月份-日期-小时-分钟-秒钟.json)。

示例：

```
(Self Dictation)>>> exp
文件已保存在：/home/user/SelfDictation/data/2025-06-01-12-00-00.json
(Self Dictation)>>> exp dict/example.json
目录不存在！错误：[Errno 2] No such file or directory: 'dict/example.json'
是否创建目录？（Y/n）y
文件已保存在：/home/user/SelfDictation/dict/example.json
```

### 6. imp

用法：`imp [路径]`

说明：从json文件导入单词表。“路径”选项必填，需包含文件路径与文件名。

示例：

```
(Self Dictation)>>> imp data/example.json
已加载文件。
```

### 7. exit

用法：`exit`

说明：正常的退出方式，会询问是否保存当前单词表。

## 版权声明

本项目使用MIT协议。

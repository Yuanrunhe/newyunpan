# python后端开发

## 前端

### 1.快速开发网站

```python
# -*- coding: utf-8 -*-
# File       : web.py.py
# Time       ：2023/2/2 21:03
# Author     ：袁润和
# version    ：python 3.5
# Description：

from flask import Flask

app = Flask(__name__)


@app.route("/show/info")
def index():
    return "中国联通"


if __name__ == '__main__':
    app.run()
```

返回文件结果的

```python
from flask import Flask,render_template

app = Flask(__name__)


@app.route("/show/info")
def index():
    # render_template他默认会在当前项目下的templates下查找
    return render_template("index.html")


if __name__ == '__main__':
    app.run()
```

### 2.HTML

笔记：https://blog.csdn.net/qq_43139145/article/details/128073474

#### 1.div和span

```html
<div>内容</div>
<span>内容</span>
```

div标签是块级标签，自己占一整行

span标签是行内标签，内容多大占多大位置

#### 2.超链接

```html
<a href="">内容</a>
```

#### 3.图片

```html
<img style="height: 100px;width: 100px" src="/static/111.jpg">
```

img标签属于行内标签

#### 4.列表

无序列表

```html
<ul>
	<li>内容1</li>
	<li>内容2</li>
</ul>
```

有序列表

```html
<ol>
	<li>内容1</li>
	<li>内容2</li>
</ol>
```

#### 5.表格

```html
    <table border="1">
        <thead>
            <tr> <th> 姓名 </th> <th> 年龄 </th> </tr>
        </thead>
        <tbody>
            <tr> <td> 袁润和 </td> <td> 18 </td> </tr>
        </tbody>
    </table>
```

#### 6.表单

##### 6.1.input系列

```html
<input type="text" />
<input type="password" />
<input type="file" />  上传文件

单选框，只要把name设置成一样就行了
<input type="radio" name="n1"/>男
<input type="radio" name="n1"/>女

多选框
<input type="checkbox" />篮球
<input type="checkbox" />排球
<input type="checkbox" />足球

按钮
<input type="button" value="提交" />  普通按钮
<input type="submit" value="提交" />  提交表单按钮
```

##### 6.2.下拉框

```html
单选
<select>
	<option>1</option>
	<option>2</option>
	<option>3</option>
</select>

多选
<select multiple>
	<option>1</option>
	<option>2</option>
	<option>3</option>
</select>
```

##### 6.3.多行文本

```html
<textarea row="3"></textarea>
```

row="3"是默认高度

##### 6.4.form表单和提交

form标签包裹要提交的数据标签。
提交方式：method="get"
提交地址：action="/xxx/xxx"
form标签中必须有submit标签

```html
    <form action="/aaa" method="get">
        账号: <input type="text" name="text">
        密码: <input type="password" name="pad">
        <input type="submit" value="提交">
    </form>
```

#### 7.小案例

html

```html
    <h1>用户注册</h1>
    <form action="/register" method="post">
        账号: <input type="text" name="user"> <br>
        密码: <input type="password" name="pwd"> <br>
        性别：
        <input type="radio" name="xb" value="1">男:
        <input type="radio" name="xb" value="2">女: <br>
        <div>
            爱好
            <input type="checkbox" name="ah" value="lq"/>篮球
            <input type="checkbox" name="ah" value="pq"/>排球
            <input type="checkbox" name="ah" value="zq"/>足球
        </div>
        <input type="submit" value="提交">
    </form>
```

后台

```python
from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/register", methods=["POST", "GET"])
def post_register():
    if request.method == "GET":
        return render_template("index.html")
    elif request.method == "POST":
        print(request.form)
        user = request.form.get("user")
        pwd = request.form.get("pwd")
        ah = request.form.getlist("ah")
        xb = request.form.get("xb")
        print("账号：", user)
        print("密码：", pwd)
        print("性别：", "男" if xb == "1" else "女")
        print("爱好：", ah)
        return '注册成功,<a href="/register">返回上一页面</a>......'


if __name__ == '__main__':
    app.run()

```

### 3.CSS

笔记：https://blog.csdn.net/qq_43139145/article/details/128073474

#### 1.高度宽度

```
.c4 {
        height: 300px;
        width: 500px;
    }
```

注意事项:

- 支持百分比
- 行内标签: 默认无效
- 块级标签: 默认有效(右边的剩余空白区域也会被占用)

#### 2.块级和行内标签

**行内标签对宽度高度边距都是无效的，必须加这个，比如要将一个图片外的a标签使图片水平居中就要加这个才能居中**

`display:inline-block` 使行内标签对 **height** 和 **width** 生效

```
.c4 {
        display: inline-block;  #这个是内块的
        height: 300px;
        width: 500px;
        border: 1px solid red;
    }
```

块级与行内标签的转换

```
	<div style="display: inline;">移动</div>
    <span style="display: block;">联通</span>
```

#### 3.字体和对齐方式

设置字体颜色/大小/粗细/字体样式

```css
<head>
    <meta charset="UTF-8">
    <title>Document</title>
    <style>
        .c1 {
            color: #00FF7F;                   /* 字体颜色 */
            font-size: 20px;                  /* 字体大小 */
            font-weight: 600;                 /* 字体粗细 */
            font-family: Microsoft Yahei;     /* 字体样式 */
            text-align: center;               /* 水平方向居中 */
            line-height: 50px;                /* 垂直方向居中 */
            border: 1px solid red;            /* 边框 */
        }
    </style>
</head>
```

#### 4.浮动

如果在块级标签中，加入了`float`属性，那么这个块级标签奖不会再占用一整行，而是自己有多大就占用多大。可以设置漂浮左右

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
    <style>
        .item {
            float: left;
            width: 280px;
            height: 170px;
            border: 1px solid red;
        }

    </style>
</head>
<body>
    <div>
        <div class="item"></div>
        <div class="item"></div>
        <div class="item"></div>
    </div>
</body>
</html>

```

如果你让标签浮动起来之后，就会脱离文档流。
例如下面的例子中，我们给div的父标签赋予了一个蓝色的背景，但是你不会看到蓝色背景。因为他被浮动的div字标签挡住了。

**内部盒子有设置宽度，外部盒子就不需要加宽度了，内部会撑起外部**

**解决办法:** 在同级子标签的最下面添加 `style="clear: both;"。加上这个就可以让浮动的标签不脱离文档流

```html
<body>
    <div style="background-color: blue;">
        <div class="item"></div>
        <div class="item"></div>
        <div class="item"></div>
        <div style="clear: both;"></div>
    </div>
</body>
```

#### 5.内边框

> padding-top | padding-left | padding-right | padding-botton

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title>
    <style>
        .outer {
            border: 1px solid red;
            height: 200px;
            width: 200px;

            padding-top: 20px;
            padding-left: 20px;
            padding-right: 20px;
            padding-bottom: 20px;
        }

    </style>
</head>
<body>
    <div class="outer">
        <div>hello</div>
        <div>world</div>
        
    </div>
</body>
</html>

```

其实上面的四个上下左右的padding可以简写为`padding: 20px 20px 20px 20px`,顺序为上右下左(顺时针方向)

#### 6.外边框

margin，`marin: 0 auto;`相当于上下 左右

```html
<body>
    <div style="height: 200px; background-color: aquamarine;"></div>
    <div style="height: 200px; background-color:blueviolet; margin-top: 20px;"></div>
</body>

```

#### 7.hover（伪类）

hover就是让鼠标放上去有效果

```css
<style>
        .c1 {
            color:brown;
        }
        .c1:hover {
            color: green;
            font-size: 20px;
        }

        .c2 {
            width: 300px;
            height: 300px;
            border: 3px solid red;
        }
        .c2:hover {
            border: 3px solid green;
        }
	
	# 鼠标放上去显示
        .download {
            display: none;  # 隐藏
        }

        .app:hover .download {
            display: block; #显示
        }

    </style>
```

#### 8.透明度

`opacity: 0.5;`

#### 9.after（伪类）

这个样式是在对应标签后面加上设置的内容

```
.c1:after {
            content: "大帅比"
        }
<div class="c1">袁润和</div>

显示
袁润和大帅比
```

这个一般是用在浮动的，因为要让他不脱离文档流，每次都必须在标签最后加上`<div style="clear: both;"></div>`，在开发中一般都是写下面的css来控制

```css
.clearfix:after{
	content: "";
	display: block;
	clear: both;
}
```



#### 10. position

- fixed
- relative
- absolute

##### 1.fixed

固定在窗口的某个位置。在这里他的位置放在body里面哪都行，因为是浮动起来的

```css
.back{
	position: fixed;
	width: 68px;
	height: 68px;
	border: 1px solid red;
	
	right: 10px;
	bottom: 20px;
}
```

##### 2.relative和absolute

这两个是联合用的，absolute是相对于relative来做改变、调整的。
比如说小米商城的下载APP，鼠标放下去就会显示二维码，而且二维码是相对于下载APP那个位置下面的，不会跑，页面怎么动也固定在那里。这就是用这个来弄的

```html
<a href="" style="position: relative">下载APP
	<div style="position: absolute">
        <img src="qcode.png" alt="">
    </div>
</a>
```

如上面案例，div就会相对于a标签的位置进行放置，调大小也会相对于于a标签进行设置，可以查看https://www.mi.com/shop的下载APP功能。这个也不会去撑起别的标签大小，不影响

#### 11.border

边框颜色

```css
    .c3 {
        height: 200px;
        width: 300px;
        margin: 50px;
        background-color: bisque;
        border-left: 2px solid transparent;  /* 透明色 ,可以设置鼠标放上去的效果*/
    }

    .c3:hover {
        border-left: 2px solid rgb(35, 211, 19);
    }
```
#### 12.背景色

`background-color: bisque;`

### 4.Bootstrap

https://www.bootcss.com/

使用方式:

- 下载Bootstrap，https://v3.bootcss.com/
- 使用:
  - 在页面上引入 Bootstrap
  - 编写HTML时,按照Bootstrap的规定来编写或者自定制

引入

```html
    <!--开发版本-->
    <link rel="stylesheet" href="static/plugins/bootstrap-3.4.1/css/bootstrap.css">
    <!--生产版本-->
<!--    <link rel="stylesheet" href="static/plugins/bootstrap-3.4.1/css/bootstrap.min.css">-->
```

开发中的目录会创建一个static来存放css、js、img、plugin(插件)，这些东西

### 5.Font Awesome

因为Bootstrap提供的图标不足，所以用图标可以用这个插件

https://fontawesome.com.cn/  直接下载旧版本4.7的，解压放到目录下

```
<link rel="stylesheet" href="static/plugins/font-awesome-4.7.0/css/font-awesome.css">
```

通过开发者模式找到图标的标签直接复制过来就行

### 6.插件引入js

jquery下载：https://jquery.com/download/

选中下载内容，见将内容复制出来后导入项目中，然后引入

```html
<script src="static/js/jquery-3.6.3.js"></script>
<script src="static/plugins/bootstrap-3.4.1/js/bootstrap.js"></script>
```

上面引入的是jQuery的包和bootstrap的js包，这样bootstrap的动态效果才实现

### 7.JavaScript

页面js编写位置。有两个位置；第一个：在head里面导入；第二个：在body内最后面，一般推荐放在第二个位置上，因为html的执行顺序是从前往下的，js放上面可能会影响效果

```html
<script type="text/javascript">
    
</script>

导入方式
<script src="static/js/jquery-3.6.3.js"></script>
```

##### 1.变量

字符串类型

```javascript
//声明
var name = "helloworld";
var name = String("helloworld");
```

常见功能

```javascript
var name = "中国联通"
var v1 = name.length;
var v2 = name[0];
var v3 = name.trim();			//去除空白
var v4 = name.substring(0,2)	//切片, 前取后不取
```

案例：

```html
<body>

    <div id="txt">欢迎中国联通领导poker莅临指导</div>

    <script type="text/javascript">

        function show() {
            //1.去HTML中找到某个标签并获取他的内容 (DOM)
            var tag = document.getElementById("txt");
            var dataString = tag.innerText;

            //2.动态起来,把文本中的第一个字符放在字符串的最后面
            var firstChar = dataString[0];
            var otherString = dataString.substring(1, dataString.length);
            var newText = otherString + firstChar;

            //3.在HTML标签中更新内容
            tag.innerText = newText;
        }

        //Javascript中的定时器
        //每秒钟执行这个show函数
        setInterval(show, 1000);    //毫秒
        //这样文字就会流动了
    </script>
</body>
```

##### 2.数组

```js
var v1 = [11,22,33,44];
var v2 = Array([11,22,33,44]);

//操作
var v1 = [11,22,33,44];

v1[1]
v1[0] = "poker"

//追加
v1.push("联通");			//尾部追加 [11,22,33,44,"联通"]
v1.unshift("联通");		//头部追加 ["联通",11,22,33,44]
v1.splice(索引,0,元素);
v1.splice(1,0,"中国");	//指定位置追加 [11,"中国",22,33,44]

//删除
v1.pop();				//尾部删除
v1.shift();				//头部删除
v1.splice(索引位置,1);
v1.splice(2,1);			//索引为 2 的元素删除 [11,22,44]



//循环
var v1 = [11,22,33,44];
//循环的是索引
for(var index in v1){
	//data=v1[index]
	...
}


for(var i=0; i<v1.length; i++){
	...
}

```

##### 3.案例: 动态数据

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Document</title> 
</head>
<body>
    
    <ul id="city">
        <!-- <li>北京</li>
        <li>天津</li>
        <li>上海</li> -->
    </ul>

    <script type="text/javascript">
        var cityList = ["北京","天津","上海"];
        for(var idx in cityList) {
            var text = cityList[idx];

            //创建 <li></li> 标签
            var tag = document.createElement("li");
            //在 li 标签中写入内容
            tag.innerText = text;

            //添加到 id=city 那个标签的里面 DOM
            var parentTag = document.getElementById("city");
            parentTag.appendChild(tag);
        }
    </script>
</body>
</html>

```

##### 4.对象(字典)

```js
info = {
	"name":"poker",
	"age":18,
}

info = {
	name:"poker",
	age:18
}

info.age;
info.name = "toker"

info["age"]
info["name"] = "toker";

//删除
delete info["age"]

//循环，这里for是取到字典的key，再通过key找到值
for(var key in info){
	//key值 data=info[key]
	...
}

```

案例：动态表格

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>

<body>
    <table border="1">
        <thead>
            <tr>
                <th>ID</th>
                <th>姓名</th>
                <th>年龄</th>
            </tr>
        </thead>
        <tbody id="body">
            <tr>
                <!-- <td>1</td>
                <td>poker</td>
                <td>25</td> -->
            </tr>
        </tbody>
    </table>

    <script type="text/javascript">

        var dataList = [
            { id: 1, name: "poker", age: 25 },
            { id: 1, name: "poker", age: 25 },
            { id: 1, name: "poker", age: 25 },
            { id: 1, name: "poker", age: 25 },
            { id: 1, name: "poker", age: 25 },
            { id: 1, name: "poker", age: 25 },
        ];

        for (var idx in dataList) {
            var info = dataList[idx]
            //1.创建 tr 标签
            var tr = document.createElement("tr")
            for (var key in info) {
                var text = info[key];
                //2.创建 td 标签
                var td = document.createElement("td");
                td.innerText = text;
                //再tr标签中加上td
                tr.appendChild(td);
            }
            //3. 追加数据
            var bodyTag = document.getElementById("body");
            bodyTag.appendChild(tr);
        }
    </script>
</body>
</html>

```

##### 5.条件语句

```js
if (条件) {
	...
}else{
	...
}

if (条件) {
	...
else if (条件){
	...
}else{
	...
}

```

##### 6.函数

```js
function func(){
	...
}

//执行
func()
```

##### 7.DOM

DOM 是一个模块,模块可以对HTML页面中的标签进行操作

```js
//根据 ID 获取标签
var tag = doucment.getElementById("xx");

//获取标签中的文本
tag.innerText

//修改标签中的文本
tag.innerText = "hhhhhhh";
```

还有很多的`DOM`操作没有介绍,我们后面会使用`JQuery`来实现`DOM`的功能,所以这里的内容了解即可

##### 8.事件的绑定

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Document</title>
</head>

<body>

    <input type="text" placeholder="请输入内容" id="content">
    <input type="button" value="点击添加" onclick="addCityInfo()">

    <ul id="city">
    </ul>

    <script type="text/javascript">
        function addCityInfo() {
            //1.找到标签
            var userContent = document.getElementById("content");
            //2.获取input中用户输入的内容
            var newString = userContent.value;
            //判断用户输入是否为空
            if (newString.length > 0) {
                //3.创建 li 标签,传入用户输入的内容
                var newTag = document.createElement("li");
                newTag.innerText = newString;
                //4.标签添加到 ul 中
                var parentTag = document.getElementById("city");
                parentTag.appendChild(newTag);
                //5.将 input text 内容清空
                userContent.value = "";
            }else{
                alert("输入不能为空!")
            }
        }
    </script>
</body>
</html>

```

### 8总结知识点

##### python数据类型

```
常见数据类型: int、bool、str、list、tuple、dict、set、float、None
- 哪些转化弄成布尔值为False: 空、None、0
- 可变和不可变划分，可变的有哪些: list、set、dict
- 可哈希和不可哈希，不可哈希的有哪些: list、set、dict
- 字典的键/集合的元素，必须是可哈希的类型 (list、set、dict不能做字典的键和集合元素)
主要数据类型:
- str
	- 独有功能: upper/lower/startswith/split/strip/join
	注意:str不可变，不会对原字符串进行修改，新的内容。
	- 公共功能: len/索引/切片/for循环/判断是否包含
- list
	- 独有功能: append、insert、remove、pop.··
	注意:list可变，功能很多都是对原数据操作。
	- 公共功能: len/索引/切片/for循环/判断是否包含
- dict
	- 独有功能: get/keys/items/values
	- 公共功能: len/索引for循环/判断是否包含(判断键效率很高)
```

### 9.jQuery

导入

```html
<script src="static/js/jquery-3.6.1.min.js"></script>
```

例子

```js
   <h1 id="txt">中国联通</h1>
	<script src="static/js/jquery-3.6.1.min.js"></script>
    <script type="text/javascript">
        //使用JQuery修改内容
        $("#txt").text("广西移动");
    </script>
```

#### 1.寻找标签

ID选择器

```
<h1 id="txt">中国联通</h1>

$("#txt")
```

样式选择器

```
<h1 class="c1">中国联通</h1>

$(".c1")
```

标签选择器

```
<h1 class="c1">中国联通</h1>

$("h1")
```

层级选择器

```
<div class="c1">
	<div class="c2">
		<h1>123</h1>
	</div>
</div>

$(".c1 .c2 h1")
```

多选择器

```
<div class="c1">
	<div class="c2">
		<h1>123</h1>
	</div>
</div>
<div class="c3">
	<div class="c4">
		<h1>123</h1>
		<li>456</li>
	</div>
</div>


$("#c1,#c2,li")
```

属性选择器

```
<input type="text" name="n1" />

$("input[name='n1']")
```

兄弟选择器

```
<div>
	<div>北京</div>
	<div id="c1">上海</div>
	<div>深圳</div>
	<div>广州</div>
</div>



$("#c1").prev()			//上一个
$("#c1")				
$("#c1").next()			//下一个
$("#c1").next().next()	//下一个的下一个
$("#c1").siblings()		//所有的
```

父子选择器

```
$("#c1").parent()			//父亲
$("#c1").parent().parent()	//父亲的父亲

$("#c1").children()			//所有的儿子
$("#c1").children(".p10")	//所有的儿子中寻找class=p10

$("#c1").find(".p10")		//所有的子孙中寻找class=p10
$("#c1").children("div")	//所有的儿子中寻找标签 div
```

#### 案例: 菜单的切换

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Document</title>

    <style>
        .menus {
            width: 200px;
            height: 1000px;
            border: 1px solid red;
        }

        .menus .header {
            background-color: royalblue;
            padding: 5px 5px;
            border-bottom: 1px dotted gray;
            cursor: pointer;
        }

        .menus .content a {
            display: block;
            padding: 5px 5px;
            border-bottom: 1px dotted gray;
        }

        .hide {
            display: none;
        }
    </style>
</head>

<body>

    <div class="menus">
        <div class="item">
            <div class="header" onclick="clickMe(this);">天津</div>
            <div class="content hide">
                <a>静海区</a>
                <a>东丽区</a>
                <a>西青区</a>
                <a>宝坻区</a>
                <a>滨海新区</a>
            </div>
        </div>
        <div class="item">
            <div class="header" onclick="clickMe(this);">上海</div>
            <div class="content hide">
                <a>静安区</a>
                <a>奉贤区</a>
                <a>浦东新区</a>
                <a>徐汇区</a>
                <a>青浦区</a>
            </div>
        </div>
    </div>

    <script src="static/js/jquery-3.6.1.min.js"></script>
    <script type="text/javascript">
        function clickMe(self) {
            //获取到我们当前的下一个标签，hasClass是看看是否有保护hide的样式
            //这样判断就可以实现打开时点击关闭，关闭时点击打开
            var hasHide = $(self).next().hasClass("hide");
            if (hasHide) {
                $(self).next().removeClass("hide");
            } else {
                $(self).next().addClass("hide");
            }
        }
    </script>
</body>
</html>

clickMe(this) 这里的this是代表我点击的这个标签，下面的self就是接受到我们点击的标签。

现在实现的还没完善，如果想要实现点击这个时关闭其它的标签，只显示当前点击的标签的话要这么写
先$(self).next().removeClass("hide");删除我们当前点击hide样式
然后获取到我们当前点击标签的所有父标签
$(self).parent().siblings().find(".content").addClass("hide");
siblings()是获取所有同胞标签，find(".content")是找到所有标签下的这样式标签，然后添加样式，这里不会重复添加的
```

#### 2.值得操作

```html
<div id="c1">内容</div>
<input type="text " id="c2"/>
```

```js
$("#c1").text()				//获取文本内容
$("#c1").text("abc")		//设置文本内容

$("#c2").val()				//获取用户输入的值
$("#c2").val("嘿嘿嘿")		//设置值
```

#### 3.事件

```html
<body>

    <ul>
        <li>百度</li>
        <li>谷歌</li>
        <li>搜狗</li>
    </ul>

    <script src="static/js/jquery-3.6.1.min.js"></script>
    <script>
        $("li").click(function(){
            // 点击li标签时,自动执行这和函数
            // $(this) 当前你点击的是哪个标签
        });
    </script>
</body>

```

在JQuery可以删除指定的标签

```js
<script src="static/js/jquery-3.6.1.min.js"></script>
<script>
    $("li").click(function(){
        // 点击li标签时,自动执行这和函数
        // $(this) 当前你点击的是哪个标签
        $(this).remove();
    });
</script>

```

### 10.前端总结

```html
    <style>
        /* 去除导航栏圆角 */
        .navbar {
            border-radius: 0;
        }
    </style>


$(this) 当前你点击的是哪个标签
```

jQuery在线手册：https://www.runoob.com/manual/jquery/

## Django

可以在老师的笔记中查找：https://www.cnblogs.com/wupeiqi/articles/4938499.html

### 1.创建项目

进入目录：执行Django-admin startproject 项目名

启动：进入项目执行启动命令：python manage.py runserver 127.0.0.1:8080

### 2.APP&模板

这个概念呢就是把一个项目下多个模块进行区分开，例如：

```
- 项目
	- app，用户管理  【表结构、函数、HTML模板...】
	- app，订单管理  【表结构、函数、HTML模板...】	
	- app，后台管理  【表结构、函数、HTML模板...】	
	- app，网站  【表结构、函数、HTML模板...】	
	- app，API  【表结构、函数、HTML模板...】	
	....
```

创建app命令：`python manage.py startapp app01`

目录：

```
创建完的目录介绍
1.migrations:	【固定的，不用动】数据库变更记录
2.admin.py:		【固定的，不用动】Django自带后台管理相关配置
3.apps.py:		【固定的，不用动】app启动类
4.models.py:	【重要】写类，根据类创建数据库表
5.tests.py:		【固定的，不用动】单元测试
6.views.py:		【重要】业务处理，函数
```

创建完要注册才能用，在setting.py中的INSTALLED_APPS中添加`app01.apps.App01Config`
这里的app01是创建的app名称，apps是固定的py文件，App01Config是里面的函数

路由设置要先引入app下面的views，然后根据views.py去引入对应的函数
`path('index/',views.index)`

```python
#urls.py
from django.contrib import admin
from django.urls import path
from app01 import views

urlpatterns = [
    path('index/', views.index)
]


#views
from django.shortcuts import render, HttpResponse
position

def index(request):
    return HttpResponse("你好")

#或者返回一个模板
def index(request):
    return render(request, "index.html")
```

##### 1.django的HTML模板

**参考上面的例子**

在这里呢app注册完后如果请求返回的是模板，那么他就会自动去templates目录下自动寻找对应的html文件，根据app的注册顺序，逐一去他们的templates目录中找

注意：如果在配置中的TEMPLATES中的DIRS中去配置`'DIRS': [os.path.join(BASE_DIR, 'templates')],`，那么他就会**优先**去根目录寻找对应的模板，找不到再去app注册顺序去templates寻找

所以要在app目录下创建templates

教程中说把DIRS给删了，为空

```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```

##### 2.django静态文件写法

**所有css、js、图片这些静态文件都要放在app目录下的static对应的css、img、js、plugins下**

引入直接写`<script src="/static/js/jquery-3.6.1.min.js"></script>`

在app下传教static目录

```html
{% load static %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>index</title>
    <link rel="stylesheet" href="{% static 'plugins/bootstrap-3.4.1/css/bootstrap.css' %}">
</head>
<body>
<img src="{% static 'img/1.png' %}" alt="">
</body>
</html>
```

这样方便以后在项目上线后如果静态文件有变化就直接改配置里面的路径就行了

### 3.Django模板写法

模板的意思是后台返回给前端的数据前端如何获取显示上去

**后台**

```python
def mb(request):
    name = "张三"
    age = 12
    agre = ["篮球", "排球"]
    zd = {"name": "zs", "age": 12}
    return render(request, "mb.html", {"name": name, "age": age, "agre": agre, "n1": zd})

```

**前端**

```html
<body>
    <h1>模板学习</h1>
    <!-- 单个数据 -->
    <div>{{ name }}</div>
    <!-- 列表 -->
    <div>{{ agre.0 }}</div>
    <div>{{ agre.1 }}</div>
    <hr/>
    <!-- for循环 -->
    {% for item in agre %}
        <span>{{ item }}</span>
    {% endfor %}
    <hr/>
    <!-- 获取字典 -->
    <span>{{ n1.name }}</span>
    <!-- 循环字典key -->
    {% for i in n1.keys %}
        <span>{{ i }}</span>
    {% endfor %}
    <!-- 循环字典value -->
    {% for i in n1.values %}
        <span>{{ i }}</span>
    {% endfor %}
    <!-- 循环字典键值 -->
    {% for k,v in n1.items %}
        <span>{{ k }} = {{ v }}</span>
    {% endfor %}
</body>


还有很多很多，都是通过.去获取后续的
例如：获取列表里面的字典
{{ n1.0.name }}

条件语句：
{% if n1 == "a1" %}
	<h1>11111</h1>
{% elif n1 == "a2" %}
	<h1>33333</h1>
{% else %}
	<h1>22222</h1>
{% endif %}
```

### 4.请求和响应

```
def someting(request):
    # request是一个对象，封装了用户发送过来的所有请求相关数据
    # 用request.method可以获取请求方式GET和POST
    # 获取请求内容可以通过request.POST/GET.get('user')
    # 【响应】放回字符串内容给请求者
    # return HttpResponse("返回内容")
    # 【响应】读取HTML的内容+渲染+字符串
    # return render(request, "class.html", {"class_list": class_list})
    # 【响应】让浏览器重定向到其它的页面
    # return return redirect("https://www.baidu.com")
    # 获取Cookies
    # request.COOKIES.get('ticket')	获取cookie
```

#### 1.解决csrf的问题

在django中有个csrf机制，我们必须在form表单里添加`{% csrf_token %}`

这个是验证机制，django会在form中默认加上这个校验机制，验证是否是通过网页正常请求来的，可以理解为反爬。我通过request.POST可以看到这个值

### 5.ORM

#### 1.ORM连接mysql

```
下载mysqlclient库，这个库相当与pymysql
pip install mysqlclient
```

#### 2.orm创建数据库

ORM可以帮忙我们做两件事：
1.创建、修改、删除数据库中的表（不需要写SQL语句）。【无法创建数据库】
2.操作表中的数据（不用写SQL语句）

```
create database yrhWebProject DEFAULT CHARSET utf8 COLLATE utf8_general_ci;
```

#### 3.ORM链接数据库

在setting.py进行配置和修改

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dbname',
        'USER': 'root',
        'PASSWORD': 'xxx',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}
```

#### 附件：redis配置

下载pip install django-redis

1

```
# redis配置
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOACTION': 'redis://127.0.0.1:6379/0',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}
```

#### 4.建表

在models.py文件中写对应的类型继承models.Model就可以以类名创建表名了

```python
class UserInfo(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    age = models.IntegerField()


# 参数
verbose_name = "标题"  # 列的中文别名
decimal_places = 2   # 小数个数


# 类型
# 小数的类型DecimalField(verbose_name="余额",max_digits=10,decimal_places=2)
# 时间类型DateTimeField(decimal_places="入职时间")


模型类如果未指明表名，Django默认以小写app应用名_小写模型类名为数据库表名。
可通过db_table指明数据库表名。
前提是要在对应的的表的model类内的class Meta:类下指定
例如：
    class Meta:
        db_table = 'department'  # 指明数据库表名
        verbose_name = '部门表'  # 在admin站点中显示的名称

```

##### Meta

1、**db_table**
个别如果咱们创立 model 的时候不指定表名，零碎在 makemigration 和 migrate 的时候会默认给咱们增加表名。
规定是：app_name + “_” + model_name 的小写。
比方一个 model 为 TestTableName，放在 blog 这个 application 下，那么在迁徙的时候，数据库表名则是：blog_testtablename。

而如果咱们在 Meta 里应用 db_table 参数，则能够间接指定表名，且忽视 application 名称前缀的规定。

```
class TestModel(models.Model):
    pass

    class Meta:
        db_table = 'test_table'
```

2、**get_latest_by**
指定 latest() 函数默认应用的字段。

先来介绍一下 latest() 函数，这个函数的应用办法前面会介绍，有一种用法：TestModel.objects.latest(‘field_name’)，这样通过指定字段名称，零碎会返回 TestModel 依照字段名为 field_name 排序的最新的一条数据。

而如果咱们在 Meta 里指定了这个参数，那么咱们就就能够在应用上述办法的时候不必指定字段名，依照咱们在 Meta 里指定的字段名来排序返回最新的一条，比方在 Blog model里咱们这样指定：

```
class Blog(models.Model):
    name = models.CharField(max_length=100)
    tagline = models.TextField()


    class Meta:
        get_latest_by = "name"
```

那么当咱们应用

```
Blog.objects.latest()
```

零碎就会获取依照 name 字段来排序，取最初一条数据，这个就等价于：

```
Blog.objects.order_by('name').last()
```

如果在 Meta 中不指定 get_latest_by 参数，那么就会依照 id 返回最初一条数据。

**留神：** 表里须要有数据，否则会报错。

3、**managed**

该参数不设置的时候，默认为 True。

如果为 True，那么对这个 model 的每次更改，都会在 makemigrations 的时候被检测到。

这个字段如果为 False，示意 Django 在 makemigrations 的时候会疏忽检测这张表，罕用在仅用于零碎查问的表。

用法如下：

```
class Blog(models.Model):
    pass

    class Meta:
        managed = True
```

4、**ordering**

返回数据的默认字段排序。

比方 Blog model，如果咱们没有在 Meta 里设置 ordering 的话，当咱们应用 Blog 筛选数据的时候，会默认依照 id 正序来返回数据，如果咱们在 Meta 里设置了 ordering 这个参数，那么当咱们在筛选的时候不应用 order_by() 参数，则会依照咱们在 ordering 里设置的字段来排序。

比方，当咱们设置：

```
class Blog(models.Model):
    pass
    
    class Meta:
        ordering = ["name"]
```

设置ordering 为 [“name”] 之后，Blog.objects.first() 返回的第一条数据，就是依照 name 进行正序排序之后的第一条。

如果想倒序排序，在字段名前加上 ‘-‘ 减号即可：ordering = [“-name”]

如果想依照多字段排序：ordering = [“name”, “tagline”]

以上就是本篇笔记的全部内容，接下来几篇笔记中将逐渐介绍 Django 的 model 在筛选中的一些用法，比方 filter，exclude，alias，values 等。

##### 执行操作

然后在终端执行命令后才能创建

```
python manage.py makemigrations
python manage.py migrate
```

执行的前提app需要先注册，没注册提交不了上去
执行后会生成很多表，其他那些表是Django自带的模块所依赖的表

如果有添加表的话，就再次执行命令就行了
删掉类再执行删掉就行，删掉列名直接注册就行

添加列：添加列有个问题就是原有数据的行需要给定默认值，可以在括号中加上default参数，设置默认值。也可以在执行命令是选择1选项确定默认值

```
# 设置默认值
age = models.IntegerField(default=2)

# 允许为空
age = models.IntegerField(null=True, blank=True)
```

##### 字段类型

| 类型             | 备注                                                         |
| ---------------- | ------------------------------------------------------------ |
| AutoField        | int自增列，必须填入参数 primary_key=True。当model中如果没有自增列，则自动会创建一个列名为id的列。 |
| Booleanfield     | 布尔字段，值为True或False                                    |
| NullBooleanField | 支持Null、True、False三种值                                  |
| CharField        | 字符类型，必须提供max_length参数， max_length表示字符长度。  |
| TextField        | 大文本字段，一般超过4000个字符时使用                         |
| IntegerField     | 一个整数类型,范围在 -2147483648 to 2147483647。              |
| Decimalfield     | 十进制浮点数 ， 参数maxdigits表示总位数， 参数decimalplaces表示小数位数 |
| FloatField       | 浮点数                                                       |
| DateField        | 日期字段，日期格式 YYYY-MM-DD，相当于Python中的datetime.date()实例。 |
| TimeField        | 时间，参数同date                                             |
| DateTimeField    | 日期时间字段，格式 YYYY-MM-DD HH:MM:ss[.uuuuuu]，相当于Python中的datetime.datetime()实例。 |
| FileField        | 上传文件字段                                                 |
| imageField       | 继承于FileField，对上传的 内容进⾏行行校验，确保是有效的图⽚片(必须要安装Pillow才可以使用（pip install Pillow） |

##### 选项

| 选项                         | 备注                                                         |
| ---------------------------- | ------------------------------------------------------------ |
| null                         | 如果为True，表示允许为空，默认值是False                      |
| blank                        | 如果为True，则该字段允许为空白，默认值是False                |
| db_column                    | 字段的名称，如果未指定，则使用属性的名称                     |
| db_index                     | 若值为True, 则在表中会为此字段创建索引，默认值是False        |
| default                      | 默认                                                         |
| primary_key                  | 若为True，则该字段会成为模型的主键字段，默认值是False，一般作为AutoField的选项使用，如果自己设定了那么django就不会给你创建id字段 |
| unique                       | 如果为True, 这个字段在表中必须有唯一值，默认值是False        |
| auto_now_add（时间字段独有） | 配置auto_now_add=True，创建数据记录的时候会把当前时间添加到数据库。 |
| auto_now（时间字段独有）     | 配置上auto_now=True，每次更新数据记录的时候会更新该字段。    |

##### 外键

在设置外键时，需要通过in_delete选项指明主表删除数据时，对于外键引用好数据如何处理，在django.db.models中包含了可选常量，on_delete：当删除关联表中的数据时，当前表与其关联的行的行为。

例如：

````blog = models.OneToOneField(xx, on_delete=models.CASCADE)````

| 外键               | 备注                                                         |
| ------------------ | ------------------------------------------------------------ |
| models.CASCADE     | 删除关联数据，与之关联也删除                                 |
| models.DO_NOTHING  | 删除关联数据，引发错误IntegrityError                         |
| models.PROTECT     | 删除关联数据，引发错误ProtectedError                         |
| models.SET_NULL    | 删除关联数据，与之关联的值设置为null（前提FK字段需要设置为可空） |
| models.SET_DEFAULT | 删除关联数据，与之关联的值设置为默认值（前提FK字段需要设置默认值） |
| models.SET         | 删除关联数据<br/>a. 与之关联的值设置为指定值，设置：models.SET(值)<br/>b. 与之关联的值设置为可执行对象的返回值，设置：models.SET(可执行对象) |
| db_constraint      | 是否在数据库中创建外键约束，默认为True。                     |

##### 创建FK表字段

在数据表中，比如用户的部门字段，如果写的是对应部门表的id的话，就需要创建字段的约束，创建方法如下：

```
depart = modeles.ForeignKey(to="Department", to_field='id')

to对应的是要关联的表
to_field对应的是字段名
注意：在这里给的字段名是depart，但是生成的字段名是depart_id

在这里虽然表名是有带id的，但是depart也是有作用的，就是当你需要查询数据时直接使用：obj.depart这样就可以直接获取关联表的对应数据了，这样会是一个对象，直接obj.depart.title就可以获取到具体字段信息了。
这里的obj是循环出来的整个对象中的单个对象

如果部门被删除了，那么对应的员工要怎么办
1.级联删除，在参数中添加on_delete=models.CASCADE
2.置空，前提是要允许字段可以为空：null=True, blank=True,on_delete=models.SET_NULL

如果给fk字段插入数据时必须是对应表的实例
```

##### 在django做约束

```
gender_choices = {
	(1, "男"),
	(2, "女")
}
gender = models.SmallIntegerField(verbose_name="性别", choices=gender_choices)


在前端中如果直接用字段名去渲染是显示不了中文的，要用.get_字段名_display去获取才能显示出中文
如：
<td>{{ item.get_ep_gender_display }}</td>
```

##### 主键id

django会为表创建自动增长的主键列，每个模型只能有一个主键列，如果使用选项设置某属性为主键列后django不会再创建自动增长的主键列。

##### 表关联查询

见https://www.cnblogs.com/cwj2019/p/11781108.html



#### 5.增删改查

##### 添加数据

```
#第一个是创建的类名，需要导入
from foreEnd.models import UserInfo
UserInfo.objects.create(name='袁润和',password='12333',age=17)
```

另一种快捷的添加数据方式：

```
from managepage.models import department
from datetime import datetime
def test(request):
    today = datetime.now().strftime('%Y-%m-%d')
    test1 = department(dp_name='人事部', dp_time=today)
    test1.save()
```

##### 删除数据

```
# 删除指定id=3的数据
UserInfo.objects.filter(id=3).delete()

# 删除表格里所有数据
UserInfo.objects.all().delete()
```

##### 查询数据

```
# 获取所有数据，他是一个QuerySet类型数据，data_list = [对象,对象]
data_list = UserInfo.objects

for obj in data_list:
	print(obj.id, obj.name, obj.password, obj.age)
	
	
# 获取指定数据,这里获取的也是对象data = [对象,]
data = UserInfo.objects.filter(id=3)
print(len(data))  这样可以获取行数
print(data[0].name)

# 如果知道获取出来的数据只有一行，那么可以直接
data = UserInfo.objects.filter(id=3).first()
print(data.name,data.password)


获取所有数据可以直接将整个对象传给前端，前端通过for循环去渲染
```

##### 更新数据

```
# 更新所有数据
UserInfo.objects.all().update(password=9999)

# 更新指定数据
UserInfo.objects.filter(id=3).update(password=9999)
```

### 6.正则URL

相对有一些get请求需要在url中添加一些参数传递到后台，这些并非是在url中？后面所传递的，而是通过根符号传递的，例如`127.0.0.1:8000/depart/1/edit`。在其中1就是传递的参数。前端、url路由器、后台需要怎么设置和获取呢：

```
# 前端
href='/depart/{{ data.id }}/edit'

# 路由。这种是django3有的，1的话需要自己写正则表达式
path('depart/<int:nid>/edit')

# 后台
def edit(request, nid):
	....
```

### 7.Django组件(Form组件、ModelForm组件)

首先举个例子，比如在页面中新建用户，在原始方式的思路中，就是通过前端填写具体的数据，然后给后台，后台在把数据添加到数据库中，但是这种方法缺少了很多东西并且还有很多麻烦的操作，例如：

```
- 用户提交数据没有校验
- 输入错误，页面上应该有错误的提示
- 页面上，每一个字段都需要我们重新写一遍
- 关联的数据，手动去获取并循环展示在页面上
```

#### 1Django组件

·Form组件(小简便)
·ModelForm组件(最简便)

#### 2.Form组件

form组件可以用来验证用户输入内容，并且在输错是可以给提示，设定规则。
form和ModelForm的区别就是一个需要自己设置字段设置规则，而另一个可以根据自己创建的model表的类来设定规则，有了原先model设置的规则外，还可以自己设置规则

##### 1.初识Form组件

**view.py**

```python
class MyForm(Form):
    user = form.CharField(widget=forms.Input)
    pwd = form.CharField(widget=forms.Input)
    email = form.CharField(widget=forms.Input)

def user_add(request):
    if request.method == "GET":
        form = MyForm()
        return reder(request, 'user_add.html', {"form":form})
```

**user_add.html**

```html
<form method="post">
    {{ form.user }}
    {{ form.pwd }}
    {{ form.email }}
</form>

也可以写成个for循环来取值
```

解释：在这里呢首先要定义一个类，继承Form，然后在里面定义几个字段，这几个字段可以设置规则，比如这里的`widget=forms.Input`就表示这个字段是一个input的输入框。然后我们的方法只需要去实例化这个类，并且将这个类传递给前端页面，前端页面只需要去获取这些字段，在前端就会自动渲染出对应的输入框。

在这里还可以设置其他规则

###### 网上复制的例子：

```python
from django import forms
from django.forms import widgets
class LoginForm(forms.Form):
	username = forms.CharField(min_length=8,label="用户名",initial="张三",error_messages={"required": "不能为空","invalid": "格式错误","min_length": "用户名最短8位"})
    pwd = forms.CharField(min_length=6,label="密码",widget=forms.widgets.PasswordInput(attrs={'class': 'c1'}, render_value=True)
        # 这个密码字段和其他字段不一样，默认在前端输入数据错误的时候，点击提交之后，默认是不保存的原来数据的，但是可以通过这个render_value=True让这个字段在前端保留用户输入的数据
    )
    gender = forms.ChoiceField(choices=((1, "男"), (2, "女"), (3, "保密")),label="性别",initial=3,
        widget=forms.widgets.RadioSelect())
    hobby = forms.ChoiceField(  # 注意，单选框用的是ChoiceField，并且里面的插件是Select，不然验证的时候会报错， Select a valid choice的错误。
        choices=((1, "篮球"), (2, "足球"), (3, "双色球"),),
        label="爱好",
        initial=3,
        widget=forms.widgets.Select()
    )
    hobby1 = forms.MultipleChoiceField(
        # 多选框的时候用MultipleChoiceField，并且里面的插件用的是SelectMultiple，不然验证的时候会报错。
        choices=((1, "篮球"), (2, "足球"), (3, "双色球"),),
        label="爱好1",
        initial=[1, 3],
        widget=forms.widgets.SelectMultiple()
    )
    keep = forms.ChoiceField(
        label="是否记住密码",
        initial="checked",
        widget=forms.widgets.CheckboxInput()
    )
    hobby3 = forms.MultipleChoiceField(
        choices=((1, "篮球"), (2, "足球"), (3, "双色球"),),
        label="爱好",
        initial=[1, 3],
        widget=forms.widgets.CheckboxSelectMultiple()
    )
    date = forms.DateField(widget=widgets.TextInput(attrs={'type': 'date'}))
EmailField(CharField)
参数label使用：
<lable for={{字段.id_for_label}}>{{字段.label}}</label>获取焦点=={{字段.label_tag}}


```

```python
常用的字段：
		forms.CharField文本框，用min_length和max_length设置文本长度
		forms.ChoiceField下拉框，参数choices以元组的形式表示
		forms.MultipleChoiceField下拉框但可以多选，继承ChoiceField
		forms.DateField：文本框但是具有验证日期格式的功能
		froms.FileFied:文件上传框，参数max_length设置上传文件名的最大长度，参数allow_empty_file是否允许文件内容为空
		ImageField：文件上传框可以验证是否为照片
		EmailField
FilePathField()     文件选项，目录下文件显示在页面中
FilePathField参数
    path,                      文件夹路径
    match=None,                正则匹配
    recursive=False,           递归下面的文件夹
    allow_files=True,          允许文件
    allow_folders=False,       允许文件夹
共同参数：
		label：用于生成label标签
在html中单独使用<lable for={{字段.id_for_label}}>{{字段.label}}</label>获取焦点=={{字段.label_tag}}
		initial：默认值
		error_messages：设置错误信息
		help_text=帮助信息
		show_hiiden_initial是否创建隐藏框
disable是否可以编辑
		require是否可以为空
		attrs设置属性
		widget：widget的值是forms.widgets对象，其类型必须与表单字段对应下面介绍表单字段对应的forms.widgets类型
		CharField 
				TextInput文本框内容设置为文本格式。
				PasswordInput密码框
				HiddenInput:隐藏文本框
		EmailField:：EmailInput验证输入值是否为邮箱格式
		ChoiceField：
Select设置下拉框
RadioSelect:将数据列表设置为单选按钮
		MultipleChoiceField
				CheckboxSelectMultiple
				selectMultipe
		FileField\ ImageField
FileInput
ClearableFieldInput与上面相比多了复选框

```

###### Form类的常用方法

```
error()获取异常信息。
is_valid()验证表单数据存在异常，若存在，则返回Flase
as_table()、as_ul()、as_p()以table\ul\pb标签的形式生成网页表单。
has_changed()：对比用于提交的数据与表单初始化数据是否发生变化。
```

###### Form类的参数

```
data:将数据绑定到对应的表单上，常见的值为request,POST
prefix:网页中使用多个相同表单时，用于区分
initial：以字典的形式表示，在表单的实例化过程中设置初始化值，往往和has_changed()连用
```

###### 自定义验证规则的使用

```python
import re
from django.forms import fields
from django.core.exceptions import ValidationError
# Create your views here.
def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')  #自定义验证规则的时候，如果不符合你的规则，需要自己发起错误
class LoginForm(forms.Form):
	phone = fields.CharField(validators=[mobile_validate, ],
		error_messages={'required': '手机不能为空'},
		widget=widgets.TextInput(attrs={'class': "form-control",
				'placeholder': '手机号码'}))
```

###### 特殊校验-数据清洗

需要在提供的校验的基础上满足某些校验规则【局部、全局钩子】，往往在调用is_valid()时，自动调用

```python
class LoginForm(forms.Form):
username = forms.CharField(min_length=8,label="用户名",
    initial="张三",error_messages={"required": "不能为空",
        "invalid": "格式错误","min_length": "用户名最短8位"})

# 定义局部钩子，用来校验username字段,之前的校验股则还在，给你提供了一个添加一些校验功能的钩子
  def clean_username(self):# 定义 clean_字段名() 方法，就能够实现对特定字段进行校验
    value = self.cleaned_data.get("username") #cleaned_data 就是读取表单返回的值，返回类型为字典dict型
    if "666" in value:
        raise ValidationError("光喊666是不行的")
    else:
        return value
```

**全局**

```python
class LoginForm(forms.Form):
    ...
    password = forms.CharField(
        min_length=6,
        label="密码",
        widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}, render_value=True)
    )
    re_password = forms.CharField(
        min_length=6,
        label="确认密码",
        widget=forms.widgets.PasswordInput(attrs={'class': 'form-control'}, render_value=True)
    )
    ...
    # 定义全局的钩子，用来校验密码和确认密码字段是否相同，执行全局钩子的时候，cleaned_data里面肯定是有了通过前面验证的所有数据
def clean(self):
    password_value = self.cleaned_data.get('password')
    re_password_value = self.cleaned_data.get('re_password')
    if password_value == re_password_value:
        return self.cleaned_data #全局钩子要返回所有的数据
    else:
        self.add_error('re_password', '两次密码不一致') #在re_password这个字段的错误列表中加上一个错误，并且clean_data里面会自动清除这个re_password的值，所以打印clean_data的时候会看不到它
```

###### 在视图中使用Form

```
obj=LoginForm(request.POST)
obj.is_valid()#验证是否全成功， True/False
obj.clean()#全成功后，获取成功的字段，以字典的方式返回
obj.errors#错误信息里包含的字段和form里的字段一样，错误是个列表，取值obj.errors['username'][0
```

关于choice的注意事项：在使用选择标签时，需要注意choices的选项可以从数据库中获取，但是由于是静态字段 获取的值无法实时更新，那么需要自定义构造方法从而达到此目的。

```python
from django.forms import Form
from django.forms import widgets
from django.forms import fields
class MyForm(Form):
    user = fields.ChoiceField(
        # choices=((1, '上海'), (2, '北京'),),
        initial=2,
        widget=widgets.Select
    )
    def __init__(self, *args, **kwargs):
        super(MyForm, self).__init__(*args, **kwargs)
        # self.fields['user'].choices = ((1, '上海'), (2, '北京'),)
        # 或
        self.fields['user'].choices = models.Classes.objects.all().values_list('id', 'caption')
```

**方式二**

```python
from django.forms import fields
from django.forms import models as form_model
class FInfo(forms.Form):
    authors = form_model.ModelMultipleChoiceField(queryset=models.NNewType.objects.all())  # 多选
    # authors = form_model.ModelChoiceField(queryset=models.NNewType.objects.all())  # 单选
```

**如果是从复杂的数据库中返回的话，无法设置str可以通过QuerySet对象去获取数据，具体如下**

```python
# QuerySet对象的所有方法
 <1> all():                  查询所有结果 
 <2> filter(**kwargs):       它包含了与所给筛选条件相匹配的对象。获取不到返回None
 <3> get(**kwargs):          返回与所给筛选条件相匹配的对象，返回结果有且只有一个。
                             如果符合筛选条件的对象超过一个或者没有都会抛出错误。
 <4> exclude(**kwargs):      它包含了与所给筛选条件不匹配的对象
 <5> order_by(*field):       对查询结果排序
 <6> reverse():              对查询结果反向排序 
 <8> count():                返回数据库中匹配查询(QuerySet)的对象数量。 
 <9> first():                返回第一条记录 
 <10> last():                返回最后一条记录 
 <11> exists():              如果QuerySet包含数据，就返回True，否则返回False
 <12> values(*field):        返回一个ValueQuerySet——一个特殊的QuerySet，运行后得到的
                             并不是一系 model的实例化对象，而是一个可迭代的字典序列
 <13> values_list(*field):   它与values()非常相似，它返回的是一个元组序列，values返回的是一个字典序列
 <14> distinct():            从返回结果中剔除重复纪录
 
 例子：
 class EpForm(forms.Form):
    ep_name = forms.CharField(min_length=2, max_length=32, widget=forms.TextInput)
    ep_brdata = forms.DateField(widget=forms.TextInput)
    ep_dpid = forms.ModelChoiceField(queryset=employee.objects.all().values()) # 返回一个对象，在前端是一个一个的字典
```



##### 2.初始ModelForm

通常在Django项目中，我们编写的大部分都是与Django 的模型紧密映射的表单。 举个例子，你也许会有个Book 模型，并且你还想创建一个form表单用来添加和编辑书籍信息到这个模型中。 在这种情况下，在form表单中定义字段将是冗余的，因为我们已经在模型中定义了那些字段。基于这个原因，Django 提供一个辅助类来让我们可以从Django 的模型创建Form，这就是ModelForm。

ModelForm相对于Form来说就更加简洁了，不需要我们每个字段去写，只需要我们去实例化models.py中我们创建表格的类就行了。例如

**models.py**

```python
class UserInfo(models.Model):
    name = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
    age = models.IntegerField()
```

**views.py**

```python
# 直接在这里定义一个类继承ModelForm，然后在里面重写Meta类，在里面实例化我们对于的表的类UserInfo,在这里我们就可以用我们建表时对字段设置的规则了，fields列表中就是我们要设置的字段名，这里传给前端也是拿这个名字去定义的
class MyForm(ModelForm):
    xx = form.CharField(widget=forms.Input)  # 也可以自己设置字段
    class Meta:
        model = UserInfo
        # 在这里需要哪几个字段写出就行了
        fields = ['name',"password","age","xx"]


def user_add(request):
    if request.method == "GET":
        form = MyForm()
        return reder(request, 'user_add.html', {"form":form})
```

**前端**

```
<form method="post">
    {% csrf_token %}
    {% for i in form %}
    	{{ i.label }}:{{ i }}
    {% endfor %}
</form>

这里的label指的是我们给字段设置的中文名，我们可以用中文名来给输入框设置标签
```

ModelForm是直接结合models进行定规则的，如果字段定义的是`choices=gender_choices`，那么在前端他是一个select下拉选项框，我们在后台设置什么前端就显示什么。
但是有一些字段是关联其他表格的，那么这个时候如果没设置其他操作时，他只会在前端的select下拉框中显示每一行数据的对象，这个时候需要在我们对应的**被关联**的表进行操作

```python
# 一般我们在输出一个对象时给出的值是这样的<......>
# 但是如果想要设置输出的值就必须在类里面设置`__str__`方法
如：
class DW(object):
	def __str__(self):
		return "哈哈哈"
a = DW()
print(a)
输出结果：哈哈哈



# 结合上面的面向对象知识，我们可以给被关联的表设置该方法
# 注意，这里是在model里面定义的
# 并且这里的表是另一个表关联过来的
class Department(models.Model):
	""" 部门表 """
	title = models.CharField(verbose_name='标题', max_length=32)
	
	def __str__(self):
	return self.title
	# 这样的话我们返回该类的对象的时候，就是返回下面方法的值
```

###### 网上的操作方法

当前端是get请求是，我们可以将整个ModelForm返回，然后前端去渲染

数据返回时，及post时，我们可以设置规则进行验证或者将数据保存

```python
from django import forms
from django.forms import ModelForm
class StudentList(ModelForm):
    #添加模型外的字段
    LEVEL=(
        ("L1",'初级'),
        ("L2","中级"),
        ('L3','高级')
    )
    level=forms.ChoiceField(choices=LEVEL,labels='级别')
    class Meta:
        model = Student  #对应的Model中的类
        fields = "__all__"      #字段，如果是__all__,就是表示列出所有的字段[字段1,字段2,]
        exclude = None          #排除的字段
        labels = None          #提示信息以 {字段名:label名}的形式
        help_texts = None       #帮助提示信息
        widgets = None          #自定义插件以
        error_messages = None   #自定义错误信息
#error_messages用法：
        error_messages = {
            '__all__':{'invalid':'请检查输入内容'},
            'name':{'required':"用户名不能为空",},
            'age':{'required':"年龄不能为空",},
        }
        #重新定义字段类型
        #一般情况下模型字段会自动转换为表单字段
        field_classes={
            'sex':forms.CharField
        }

#widgets用法,比如把输入用户名的input框给为Textarea
#首先得导入模块
        from django.forms import widgets as wid  #因为重名，所以起个别名
        widgets = {
            "name":wid.Textarea(attrs={"class":"c1"}) #还可以自定义属性
        },
#labels，自定义在前端显示的名字

　　　　labels= {
            "name":"用户名"
        }
使用：
====views
def student(request):
if request.method == 'GET':
        student_list = StudentList()
        return render(request,'student.html',{'student_list':student_list})
===html===
略
保存数据，不用挨个取数据了，只需要save一下
def student(request):
   if request.method == 'GET':
        student_list = StudentList()
        return render(request,'student.html',{'student_list':student_list})
    else:
        student_list = StudentList(request.POST)
        if student_list.is_valid():
            student_list.save()#如果说多对多.save_m2m()
        return redirect(request,'student_list.html',{'student_list':student_list})
编辑数据，只需要加一个instance=obj（obj是要修改的数据库的一条数据的对象）就可以得到同样的效果。保存的时候要注意，一定要注意有这个对象（instance=obj），否则不知道更新哪一个数据。
def student_edit(request,pk):  # 这里的pk可以看看路由设置正则的那个，是根据那个取的
    obj = models.Student.objects.filter(pk=pk).first()
    if not obj:
        return redirect('test')
    if request.method == "GET":
        student_list = StudentList(instance=obj)
        return render(request,'student_edit.html',{'student_list':student_list})

    else:
        student_list = StudentList(request.POST,instance=obj)
        if student_list.is_valid():
            student_list.save()
        return render(request,'student_edit.html',{'student_list':student_list})
```

```python
class UserInfoModelForm(forms.ModelForm):
    class Meta:
        model = models.UserInfo
        fields = '__all__'                              # __all__ 代表全部列
        # fields = ['username', 'email', 'user_type']   # 手动写所有的列
        # exclude = ['user_type']                       # 排除谁
```



##### 3.ModelForm传前端时给字段设置样式

当我们在前端直接获取后台传过来的标签显示上去，标签是没有样式的，但是在前端又加不了，所以只能在后端定义ModelForm的类里调用组件去设置，例如：

```python
class MyForm(ModelForm):
    xx = form.CharField(widget=forms.Input)  # 也可以自己设置字段
    class Meta:
        model = UserInfo
        # 在这里需要哪几个字段写出就行了
        fields = ['name',"password","age","xx"]
    widgets = {
        "name":forms.TextInput(attrs={"class":"form-control"})
        "password":forms.TextInput(attrs={"class":"form-control"})
    }
```

这样的话就可以给标签设置参数了
但是这样子太麻烦了，如果太多标签的话一个一个写很麻烦，可以参考下面写法

```python
class MyForm(ModelForm):
    xx = form.CharField(widget=forms.Input)  # 也可以自己设置字段
    class Meta:
        model = UserInfo
        # 在这里需要哪几个字段写出就行了
        fields = ['name',"password","age","xx"]
    def __init__(self, *args, **kwargs):
    	super().__init__(*args, **kwargs)
    	for name, field in self.fields.items()：
    		# 这里的name是上面我们获取字段的字段名。field是字段的对象
    		# 循环找到所有的插件，添加了对应的样式
    		field.widegt.attrs = {"class":"form-control","placeholder":field.label}
1
如果有哪个字段不加或者哪个字段有特殊形式的话可以判断name等于某个值时做出的操作，例如continue跳出
```

##### 4.ModelForm的错误验证

```python
def user_add(request):
    if request.method == "GET":
        form = MyForm()
        return reder(request, 'user_add.html', {"form":form})
    
    # 用户POST提交数据，数据校验
    form = MyForm(data=request.POST)
    # 判断提交数据是否合规
    if form.is_valid():
        # 获取数据
        print(form.cleaned_data)
        # 是的话就将数据报错到数据库
        form.save()
        retuen redirect('/add/')
    # 不合规时
    return render(request,'user_add.html', {"form":form})
	# 注意，这里返回的form对象数据已经不是前面get时返回的数据了，现在这里的数据是包含前端填写的内容和报错信息的，如果通过这样返回的话前端的输入框内容是不会被清洗掉的，而是一直显示在里面。在前端还有可以通过{{ field.errors }}去获取报错信息，但是这样获取的是一个列表，我们只需要获取第一个错误信息{{ field.errors.0 }},可以显示给前端用户
    
    
前端获取错误信息示范：
{% for i in data %}
        <div class="form-group">
        <label>{{ i.label }}</label>{{ i }}
        <span style="color: red;">{{ i.errors.0 }}</span>  错误信息是一个列表，我们只获取第一个就行
        </div>
{% endfor %}

可以先关闭页面的校验，如<form method="post" novalidate>
```

这样前端显示的全部都是英文的，除了可以自己去改动显示的内容也可以直接到配置文件中修改编码`LANGUAGE_CODE = 'zh-hans'`

##### 5.ModelForm修改数据

在前端页面中，如果需要去更改指定的数据的话，按照前面ModelForm的操作是实现不了需求的，必须按照以下的操作
首先当我们要对某个信息进行修改是，我们可以把这个信息的id传给后端，然后后端根据这个信息去获取这条数据，再将这条数据instance给对应的ModelForm函数，然后再返回给前端，前端可以将这条数据渲染到也去，实现修改时可以看到对应的数据

```python
# 这里的nid是前端传给url，url通过正则获取的值，在这里是指定数据的值
def user_edit(request,nid):
    if request.method == "GET":
    	# 先根据id去获取要编辑的那一行数据
    	row_object = models.UserInfo.objects.filter(id=nid).first()
    	# 这里的MyForm是前面设置的ModelForm类，instance是自动传入前面获取的数据显示在前端的修改页面上
    	# 这里解决的是前端修改时怎么显示我们要修改的那一行数据
    	form = MyForm(instance=row_object)
    	return reder(request, 'user_add.html', {"form":form})
   	
    # 提交校验的步骤，获取修改的数据
    # 在这里也要获取对应数据，传进去ModelForm对象中去，这样才是修改数据
    row_object = models.UserInfo.objects.filter(id=nid).first()
    form = MyForm(data=request.POST,instance=row_object)
    if form.is_valid():
        form.save()
        retuen redirect('/xiugai1/')
    return reder(request, 'user_add.html', {"form":form})
```

**除了用户输入的值保存到数据库中，我们也可以进行操作保存，例如`form.instance.字段=123`**,在保存之前设置

##### 6.ModelForm正则表达式

```python
from django.core.validators import RegexValidator
class MyForm(ModelForm):
    mobile = form.CharField(
    	label="手机号",
        validators=[RegexValidator(r'1\d{10}$', '手机号格式错误')]
    )
    class Meta:
        model = UserInfo
        fields = ['name',"password","age","xx"]
    def __init__(self, *args, **kwargs):
    	super().__init__(*args, **kwargs)
    	for name, field in self.fields.items()
    		field.widget.attrs = {"class":"form-control","placeholder":field.label}
```

**验证方式2**

自定义验证方式，定义**钩子**方法去验证。方法定义是clean开头加上对应的字段名。有全局写法和局部写法，在上面复制网上例子有写

```python
from django.core.validators import RegexValidator
class MyForm(ModelForm):
    class Meta:
        model = UserInfo
        fields = ['name',"password","age","xx","mobile"]
    def __init__(self, *args, **kwargs):
    	super().__init__(*args, **kwargs)
    	for name, field in self.fields.items()
    		field.widegt.attrs = {"class":"form-control","placeholder":field.label}
    def clean_mobile(self):
    	txt_mobile = self.cleaned_data["mobile"]  #读取cleaned_data字典的mobile数据，进行验证
    	if len(txt_mobile) != 11:
        	# 验证不通过
        	raise ValidationError("格式错误")
    	# 验证通过，用户输入的值返回
    	return txt_mobile
    
    """
    	钩子方法定义：(规定写法)
    	命名规则：clean_字段名
    	通过cleaned_data去获取用户输入的内容，他是一个字典，是用户输入后的所有数据
    	验证不通过返回错误信息
    	验证通过返回对应的值
    """
```

##### 7.ModelForm组件相关操作

```python
ModelForm
    a.  class Meta:
            model,                           # 对应Model的类
            fields=None,                     # 字段，表名
            exclude=None,                    # 排除字段，排除表名
            labels=None,                     # 提示信息，在html页面中显示的信息
            help_texts=None,                 # 帮助提示信息
            widgets=None,                    # 自定义插件
            error_messages=None,             # 自定义错误信息（整体错误信息from django.core.exceptions import NON_FIELD_ERRORS）
            field_classes=None               # 自定义字段类 （也可以自定义字段）
            localized_fields=('birth_date',) # 本地化，如：根据不同时区显示数据
            如：
                数据库中
                    2016-12-27 04:10:57
                setting中的配置
                    TIME_ZONE = 'Asia/Shanghai'
                    USE_TZ = True
                则显示：
                    2016-12-27 12:10:57
    b. 验证执行过程
        is_valid -> full_clean -> 钩子 -> 整体错误
 
    c. 字典字段验证，钩子方法
        def clean_字段名(self):
            # 可以抛出异常
            # from django.core.exceptions import ValidationError
            return "新值"
    d. 用于验证
        model_form_obj = XXOOModelForm()
        model_form_obj.is_valid()
        model_form_obj.errors.as_json()
        model_form_obj.clean()
        model_form_obj.cleaned_data
    e. 用于创建
        model_form_obj = XXOOModelForm(request.POST)
        #### 页面显示，并提交 #####
        # 默认保存多对多
            obj = form.save(commit=True)
        # 不做任何操作，内部定义 save_m2m（用于保存多对多）
            obj = form.save(commit=False)
            obj.save()      # 保存单表信息
            obj.save_m2m()  # 保存关联多对多信息
 
    f. 用于更新和初始化
        obj = model.tb.objects.get(id=1)
        model_form_obj = XXOOModelForm(request.POST,instance=obj)
        ...
 
        PS: 单纯初始化
            model_form_obj = XXOOModelForm(initial={...})

```

##### 8.ModelForm设置不可编辑

当输入框属于编辑功能是，有些字段比如用户名这些我们不想让用户去编辑，但是想让他显示的话可以参考下面写法：

```python
class MyForm(ModelForm):
    mobile = forms.CharField(disabled=True, label="手机号")  # 这里设置disabled=True表示不可编辑
    class Meta:
        model = UserInfo
        fields = ['name',"password","age","mobile"]
    def __init__(self, *args, **kwargs):
    	super().__init__(*args, **kwargs)
    	for name, field in self.fields.items()
    		field.widegt.attrs = {"class":"form-control","placeholder":field.label}
```

##### 9.ModelForm不允许输入重复值

例如：不允许手机号重复

```python
class MyForm(ModelForm):
    mobile = forms.CharField(disabled=True, label="手机号")  # 这里设置disabled=True表示不可编辑
    class Meta:
        model = UserInfo
        fields = ['name',"password","age","mobile"]
    def __init__(self, *args, **kwargs):
    	super().__init__(*args, **kwargs)
    	for name, field in self.fields.items()
    		field.widegt.attrs = {"class":"form-control","placeholder":field.label}
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        # 验证号码是否存在
        exists = models.UserInfo.objects.filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("号码已存在")
        return txt_mobile
```

当创建或者添加是的判断

```python
# 【obj,obj,obj...】
queryset = models.UserInfo.obdects.filter(mobile="188888")
# 返回第一个
obj = models.UserInfo.obdects.filter(mobile="188888").first()
# True/False
exists = models.UserInfo.obdects.filter(mobile="188888").exists()
```

当编辑时做判断。排除自己以外，其他的数据手机号是否重复

```python
获取号码等于某个值，id不等于2的
models.UserInfo.obdects.filter(mobile="188888").exclude(id=2)
```

在ModelForm中获取当前对应的id

```python
class MyForm(ModelForm):
    mobile = forms.CharField(disabled=True, label="手机号")  # 这里设置disabled=True表示不可编辑
    class Meta:
        model = UserInfo
        fields = ['name',"password","age","mobile"]
    def __init__(self, *args, **kwargs):
    	super().__init__(*args, **kwargs)
    	for name, field in self.fields.items()
    		field.widegt.attrs = {"class":"form-control","placeholder":field.label}
    def clean_mobile(self):
        txt_mobile = self.cleaned_data['mobile']
        # 验证号码是否存在。这里的pk就是前端传进来的id接收的
        exists = models.UserInfo.objects.exclude(id=instance.pk).filter(mobile=txt_mobile).exists()
        if exists:
            raise ValidationError("号码已存在")
        return txt_mobile
```

##### 10.ModelForm进行数据搜索

```python
ModelForm搜索数据的两种写法

直接传入值进行搜索
models.UserInfo.obdects.filter(mobile="188888", id=2)

传入字典写法方式进行数据搜索
data_dict = {"mobile":"18888888888", "id":123}
models.UserInfo.obdects.filter(**data_dict)
```

###### 数学条件

```python
models.UserInfo.obdects.filter(id=2)
models.UserInfo.obdects.filter(id__gt=2) # 大于
models.UserInfo.obdects.filter(id__gte=2) # 大于等于
models.UserInfo.obdects.filter(id__lt=2) # 小于
models.UserInfo.obdects.filter(id__lte=2) # 小于等于
```

```python
models.UserInfo.obdects.filter(mobile__startwith="188")  # 开头包含
models.UserInfo.obdects.filter(mobile__endwith="188")  # 结尾包含
models.UserInfo.obdects.filter(mobile__contains="188")  # 文本包含
```

##### 11.分页

```python
queryset = models.UserInfo.obdects.all()  # 获取所有
queryset = models.UserInfo.obdects.filter(id=2)[0:10]  # 获取对应id的前十条
queryset = models.UserInfo.obdects.all()[0:10]  # 获取所有数据的前十条
queryset = models.UserInfo.obdects.all()[10:20]  # 获取所有数据的第11条到20条
```

后端传给前端的标签能在前端显示必须标记为安全的mark_safe()。这里忽略了很多代码

```python
from django.utils.safestring import mark_safe

page_str_list = []
for i in range(1,21):
	ele = '<li><a href="?page={}">{}</a></li>'.format(i,i)
	page_str_list = []
page_string = mark_safe("".join(page_str_list))  # 标记为安全的，这样前端才会显示出来

return render(request, 'pretty_list.html', {"page_string":page_string})
```

获取数据库中的总条数

```python
# 获取总条数
count = models.UserInfo.obdects.all().count()
```

根据上面的写法，我们可以获取数据库的总条数，然后根据总条数去除以每页显示的数量去取整。可以用python的内置函数divmod()去相除，然后根据返回的第二个值去取整+1。再去生成页面选项。

但是，如果按照前面的思路的获取页面在前端去弄页面跳转的选项时，如果太多页码都会堆积在一起，很不美观。所以可以按照新思路只显示当前页面的前五页和后五页，中间交杂这当前页面。但是还有问题所在，如果我当前页面选择的是前五页的话，或者后五页的话，可能就不美观了，后台需要做判断，例如：

显示规则是当前页面的前五页和后五页的前提下：
如果当前页码小于等于5的话，开始页面必须等于1，结束页码为11
如果当前页码大于等于总页码-5的话，那么开始页面就为总页码-5+1，结束页面为总页码

这样就不会显示出小于1的页码和大于总页码的页码了

如果想在页码中将当前页面的位置显示高亮，就可以在生成页码出加上高亮的类标签就行了

**自己项目设置的分页**

```python
def user(request):
    page = int(request.GET.get("page")) if request.GET.get("page") else 1  # 当前页码
    # 定义每一页开始和结束的数据序号
    max_data = 10
    start_data = (page - 1) * max_data
    end_data = page * max_data
    employeeForm = employee.objects.all()[start_data:end_data]  # 获取当前数据
    data_count = employee.objects.all().count()  # 数据库总量
    total = divmod(data_count, max_data)[0]+1 if divmod(data_count, max_data)[1] else divmod(data_count, max_data)[0]  # 获取总页码
    # 设置当前页码前后显示的页数
    max_page = 3
    start_page = (page - max_page) if page > max_page else 1
    end_page = page + 4 if page < (total - max_page) else (total + 1)
    page_str_list = []
    # 设置上一页按钮
    if page == 1:
        page_str_list.append('<li class="disabled"><a href="#"><span aria-hidden="true">&laquo;</span></a></li>')
    else:
        page_str_list.append('<li><a href="/user/?page={}"><span aria-hidden="true">&laquo;</span></a></li>'.format(page - 1))
    # 设置页码按钮
    for i in range(start_page, end_page):
        if i == page:
            ele = '<li class="active"><a href="/user/?page={}">{}</a></li>'.format(i, i)
        else:
            ele = '<li><a href="/user/?page={}">{}</a></li>'.format(i, i)
        page_str_list.append(ele)
    # 设置下一页按钮
    if page == total:
        page_str_list.append('<li class="disabled"><a href="#"><span aria-hidden="true">&raquo;</span></a></li>')
    else:
        page_str_list.append('<li><a href="/user/?page={}"><span aria-hidden="true">&raquo;</span></a></li>'.format(page + 1))
    # 转换成字符串，并且设置为可信任的
    page_string = mark_safe("".join(page_str_list))
    print(page_string)

    return render(request, "employee.html", {'form': employeeForm, "page": page_string})
```

**前端**

```html
<nav aria-label="...">
  <ul class="pagination">
      {{ page }}
  </ul>
</nav>
```

##### 12.分页组件封装

app.utils下的组件

```python
#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# version: v1.0
# author : 袁润和
# Project : ythWhleProject
# File : pagep.py
# Software: PyCharm
# time: 2023/4/17 23:02
"""
import copy
from django.utils.safestring import mark_safe


class Paginstion(object):
    def __init__(self, requests, query_object, max_data=10, max_page=3, method="GET", paga_param="page",
                 dis_param=None):
        """
        获取分页组件的脚本
        get_html(self): 获取分页的html
        get_urlparam(self, page=None): 拼接分页标签的url参数
        get_data(self): 获取当前页面的数据对象

        :param requests: 请求的对象
        :param query_object: model对象
        :param max_data: 页面数据显示最大的函数
        :param max_page:  分页器当前页面前后的选项，默认3
        :param method: 请求类型，默认为get
        :param paga_param: url中当前页码的参数
        :param dis_param: url中需剔除的参数，列表形式出现
        """

        self.requests = requests
        self.query_object = query_object
        self.max_data = max_data
        self.max_page = max_page
        self.dis_param = dis_param
        self.paga_param = paga_param
        self.method = method
        self.total = self.query_object.objects.all().count()
        self.url_path = self.requests.path

        # 根据数据量获取总页码
        self.total_page = divmod(self.total, self.max_data)[0] + 1 if divmod(self.total, self.max_data)[1] else \
            divmod(self.total, self.max_data)[0]

        # 获取当前页码
        if method == "GET":
            self.page = requests.GET.get(self.paga_param, "1")
        else:
            self.page = requests.POST.get(self.paga_param, "1")
        if self.page.isdecimal():
            self.page = int(self.page)
        else:
            self.page = 1

        # 避免当前页面小于1或者大于总数
        if self.page > self.total_page:
            self.page = self.total_page
        elif self.page < 1:
            self.page = 1

        # # 取当前页码的前后个数
        if self.total_page <= self.max_page:
            self.start_page = 1
            self.end_page = self.total_page
        elif self.page < 1:
            self.start_page = 1
            self.end_page = (self.max_page * 2 + 1) if (self.max_page * 2 + 1) <= self.total_page else self.total_page
        elif self.page >= self.total_page:
            self.start_page = self.total_page - (self.max_page * 2) if (self.total_page - (
                    self.max_page * 2)) > 0 else 1
            self.end_page = self.total_page
        else:
            if self.page >= (self.total_page - self.max_page):
                if (self.total_page - (self.max_page * 2)) > 0:
                    self.start_page = self.total_page - (self.max_page * 2)
                else:
                    self.start_page = 1
                if (self.page + self.max_page) <= self.total_page:
                    self.end_page = self.page + self.max_page
                else:
                    self.end_page = self.total_page
            elif (self.page - self.max_page) <= 1:
                if self.total > (1 + (self.max_page * 2)):
                    self.start_page = 1
                    self.end_page = 1 + (self.max_page * 2)
                else:
                    self.start_page = 1
                    self.end_page = self.total_page
            else:
                self.start_page = self.page - self.max_page
                self.end_page = self.page + self.max_page

        self.page_str_list = []

    def get_html(self):
        """
        获取分页组件的html
        :return: html
        """

        # 设置首页按钮
        self.page_str_list.append(
            '<li class="disabled"><a href="{}?{}"><span aria-hidden="true">首页</span></a></li>'.format(
                self.url_path, self.get_urlparam(1)))
        # 获取上一页按钮
        if self.page == 1:
            self.page_str_list.append(
                '<li class="disabled"><a href="#"><span aria-hidden="true">&laquo;</span></a></li>')
        else:
            self.page_str_list.append(
                '<li><a href="{}?{}"><span aria-hidden="true">&laquo;</span></a></li>'.format(
                    self.url_path, self.get_urlparam(self.page - 1)))

        # 中间数据的按钮
        for page in range(self.start_page, self.end_page + 1):
            if page == self.page:
                self.page_str_list.append(
                    '<li class="active"><a href="{}?{}">{}</a></li>'.format(self.url_path, self.get_urlparam(page),
                                                                            page)
                )
            else:
                self.page_str_list.append(
                    '<li><a href="{}?{}">{}</a></li>'.format(self.url_path, self.get_urlparam(page), page)
                )

        # 获取下一页按钮
        if self.page == self.total:
            self.page_str_list.append(
                '<li class="disabled"><a href="#"><span aria-hidden="true">&raquo;</span></a></li>')
        else:
            self.page_str_list.append(
                '<li><a href="{}?{}"><span aria-hidden="true">&raquo;</span></a></li>'.format(
                    self.url_path, self.get_urlparam(self.page + 1)))
        # 获取尾页按钮
        self.page_str_list.append(
            '<li class="disabled"><a href="{}?{}"><span aria-hidden="true">尾页</span></a></li>'.format(
                self.url_path, self.get_urlparam(self.total_page)))
        page_string = mark_safe("".join(self.page_str_list))
        return page_string

    # 获取url参数,并且给定参数拼接
    def get_urlparam(self, page=None):
        """
        根据给定的页码拼接url的get参数
        :param page: 页码
        :return: url.get参数
        """
        if self.paga_param:
            url_param = copy.deepcopy(self.requests.GET)
            url_param._mutable = True
            # 先去除页码的当前页面参数，方便给生成html的拼接url
            url_param.pop(self.paga_param, None)
            # 去除指定的参数
            if self.dis_param:
                if isinstance(self.dis_param, list):
                    for i in page:
                        url_param.pop(i, None)
                else:
                    print("输入参数类型非列表")
            url_param.setlist(self.paga_param, [page])
            return url_param.urlencode()

    # 获取当前页面数据
    def get_data(self):
        """
        获取当前页的数据
        :return: data.objects
        """

        start_data = (self.page - 1) * self.max_data
        end_data = self.page * self.max_data
        data = self.query_object.objects.all()[start_data: end_data]
        return data

```

调用方法：

```python
    paginstion = Paginstion(request, project_info, max_data=10)
    html = paginstion.get_html()
    data = paginstion.get_data()
    return render(request, "employee.html", {'form': data, "page": html})
```

##### 其中对get请求参数操作的有

```python
# 如果需要删除某个参数，可以使用 QueryDict 对象来实现。QueryDict 是 Django 提供的一个类，用于处理 HTTP 请求参数。首先将 GET 请求参数转换为 QueryDict 对象
from django.http import QueryDict

params = request.GET.copy()
params.pop('param', None)

# 第二种方法，修改源码参数，使请求中的参数可以修改
import copy
params = copy.deepcopy(self.reques.GET)  # 用深拷贝拷贝不影响原来的对象
params._mutable = True  # 如果不改这个，给url改变或者添加参数时是会报错的
query_params.pop('param', None)

# 接第一种方法
# 修改参数值
params['page'] = 2

# 删除参数
if 'sort' in params:
    del params['sort']

# 转换为查询字符串
query_string = params.urlencode()

# 重定向到当前 URL 并带上修改后的查询字符串
return redirect(request.path + '?' + query_string)



主要是对url进行修改，删除，例如有时候url会携带一些数据，或者自动输入的数据超出了总页码做的操作

```

注意，在实际应用中，为了避免一些特殊字符导致的错误，建议使用 quote() 或 unquote() 函数对参数进行编码或解码。例如：

```python
from urllib.parse import quote, unquote

# 编码参数
params['q'] = quote(params['q'])

# 解码参数
q = unquote(params.get('q', ''))
```



### 附加.项目启动步骤总结

```python
## 首先创建项目
python manage.py startapp manage

## 创建app，后续可以规划页面为多个app
python manage.py startapp managepage

## 如果是测试的话可以不设置app，直接在view中进行编写就行了，然后记得在INSTALLED_APPS注册

## 在settings中修改TEMPLATES配置，'DIRS': [os.path.join(BASE_DIR, 'templates')],具体意思上面有
## 前面设置了，就需要在每个APP下面创建一个目录名为templates的目录，用来存放模板

## 创建static目录，下面创建css、img、js、plugins目录


```



#### 8、实操（部门管理）

制作部门管理，在这里忽略页面的模板

##### 1.model表字段

**部门表**

```python
# 部门名称
class department(models.Model):
    dp_id = models.AutoField(primary_key=True, verbose_name="部门ID")  # 部门ID
    dp_name = models.CharField(max_length=32, verbose_name="部门名称")  # 部门名称
    dp_time = models.DateField(null=True, blank=True, default=None, verbose_name="建立时间")  # 建立时间

    def __str__(self):
        return self.dp_name

    class Meta:
        db_table = 'department'  # 指明数据库表名
        verbose_name = '部门表'  # 在admin站点中显示的名称

```

**员工表**

```python
class employee(models.Model):
    ep_id = models.AutoField(primary_key=True, verbose_name="员工ID")  # 员工ID
    ep_name = models.CharField(max_length=32, verbose_name="姓名")  # 姓名
    ep_brdata = models.DateField(verbose_name="出生日期")
    ep_dpid = models.ForeignKey(to="department", to_field="dp_id", null=True, blank=True, on_delete=models.SET_NULL,
                                verbose_name="归属部门ID")
    gender_choices = (
        (0, "男"),
        (1, "女")
    )
    status_choices = (
        (0, "离职"),
        (1, "在职"),
        (2, "待入职")
    )
    ep_gender = models.IntegerField(choices=gender_choices, verbose_name="性别")
    ep_status = models.IntegerField(choices=status_choices, verbose_name="状态")

    class Meta:
        db_table = 'employee'  # 指明数据库表名
        verbose_name = '员工表'  # 在admin站点中显示的名称

```

##### 2、查看功能

**view**

```python
def user(request):
    # csrfmiddlewaretoken
    respond_data = {}
    if request.GET.get("q"):
        q = request.GET.get("q")
        employeeForm = employee.objects.filter(ep_name__contains=q)
        data_count = employee.objects.filter(ep_name__contains=q).count()
        respond_data["q"] = q
    else:
        employeeForm = employee.objects.all()
        data_count = employee.objects.all().count()
    # 调用封装的分页功能
    paginstion = Paginstion(request, employeeForm, data_count, dis_param=["csrfmiddlewaretoken"], max_page=3)
    respond_data["page"] = paginstion.get_html()
    respond_data["form"] = paginstion.employeeForm
    if respond_data["form"].count() == 0:
        respond_data["count"] = "抱歉，查无该关键词的相关数据"

    return render(request, "employee.html", respond_data)
```

**html**

```python
<table class="table table-bordered table-cz">
    <thead>
    <tr>
        <th> ID</th>
        <th> 姓名</th>
        <th> 性别</th>
        <th> 部门</th>
        <th> 状态</th>
        <th> 操作</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        {% for item in form %}
        <td>{{ item.ep_id }}</td>
        <td>{{ item.ep_name }}</td>
        <td>{{ item.get_ep_gender_display }}</td>
        <td>{{ item.ep_dpid.dp_name }}</td>
        <td>{{ item.get_ep_status_display }}</td>
        <td>
            <a style="text-decoration:none; color: white" class="btn btn-primary btn-xs" href="/edit_user/{{ item.ep_id }}/">编辑</a>
            <a style="text-decoration:none; color: white" class="btn btn-danger btn-xs" href="/sy/">删除</a>
        </td>
    </tr>
        {% endfor %}

    </tbody>
```

##### **3.添加员工**

需要创建ModelForm类，然后需要实例化改列，并且传入前端

**ModelForm**

```python
# 添加用户的modelform
class EpModelForm(forms.ModelForm):
    class Meta:
        model = employee
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field in ['ep_name', 'ep_brdata']:
                field.widget.attrs = {"class": "form-control", "placeholder": field.label}
            elif field in ['ep_dpid', 'ep_gender', 'ep_status']:
                field.widget.attrs = {"class": "form-control", "placeholder": field.label}
            else:
                field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_ep_number(self):
        text_ep_number = self.cleaned_data["ep_number"]
        if len(text_ep_number) != 11:
            raise ValidationError("号码格式不准确")
        return text_ep_number
```

**view**

```python
def add_user(request):
    if request.method == "GET":
        da = EpModelForm()
        return render(request, 'add_user.html', {"data": da})
    da = EpModelForm(data=request.POST)
    if da.is_valid():
        print(da.cleaned_data)
        da.save()
        return redirect('/sy/', {"err": "保存成功"})
    else:
        print(da.errors)
        return render(request, "add_user.html", {"data": da})
```

**html**

```html
<form method="post" novalidate>
    {% csrf_token %}
    {% for i in data %}
    <div class="form-group">
    <label>{{ i.label }}</label>{{ i }}
    <span style="color: red;">{{ i.errors.0 }}</span>
    </div>
    {% endfor %}
    <div class="button-wz">
        <button type="submit" class="btn btn-primary">提交添加</button>
        <a href="/sy/"><div class="btn btn-info" style="clear: both; margin-left: 30px">返回首页</div></a>
    </div>

</form>
```

##### 4.删除功能

```python
def delete_user(request, nid):
    data = employee.objects.filter(ep_id=nid).delete()

    return redirect('/sy/', {"err": "删除成功"})
```

##### 5.编辑功能

编辑也跟添加一样，要用ModelForm进行验证，这里就不写了，直接跟添加差不多，多几个逻辑

```python
def edit_user(request, nid):
    if request.method == "GET":
        row_object = employee.objects.filter(ep_id=nid).first()
        da = eidtEpModelForm(instance=row_object)
        da.Meta()
        return render(request, "edit_user.html", {"data": da})
    else:
        row_object = employee.objects.filter(ep_id=nid).first()
        da = eidtEpModelForm(data=request.POST, instance=row_object)
        print(da.is_valid())
        if da.is_valid():
            da.save()
            return redirect('/sy/', {"err": "保存成功"})
        else:
            return render(request, "edit_user.html", {"data": da, "err": "修改失败"})
```

#### 9、时间组件的使用

引入bootstrap-datetimepicker库
官网地址：https://www.bootcss.com/p/bootstrap-datetimepicker/index.htm

引入依赖

```python
前提是要有jQuery

{% block script %}
<link rel="stylesheet" href="{% static 'plugins/bootstrap-datetimepicker/css/bootstrap-datetimepicker.min.css' %}">
<script src="{% static 'plugins/bootstrap-datetimepicker/js/bootstrap-datetimepicker.js' %}"></script>
<script src="{% static 'plugins/bootstrap-datetimepicker/js/locales/bootstrap-datetimepicker.zh-CN.js' %}"></script>
{% endblock %}

然后写一段js
{% block js %}
$('#id_ep_brdata').datetimepicker({
    language: 'zh-CN', // 中文语言包
    autoclose: 1, // 选中日期后自动关闭
    format: 'yyyy-mm-dd', // 日期格式
    minView: "month", // 最小日期显示单元，这里最小显示月份界面，即可以选择到日
    todayBtn: 1, // 显示今天按钮
    todayHighlight: 1, // 显示今天高亮
  });
{% endblock %}

然后在要输入时间的input框中添加js方法名给id属性，如果后台传过来的默认有id可以将方法名改为对应的id
```

#### 11.bootstrap样式父类

在前面的操作中，每一次设置ModelForm是都需要给字段添加样式，例如：

```python
class eidtEpModelForm(forms.ModelForm):
    ep_name = forms.CharField(disabled=True, label="姓名")

    class Meta:
        model = employee
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if field in ['ep_name', 'ep_brdata']:
                field.widget.attrs = {"class": "form-control", "placeholder": field.label}
            elif field in ['ep_dpid', 'ep_gender', 'ep_status']:
                field.widget.attrs = {"class": "form-control", "placeholder": field.label}
            else:
                field.widget.attrs = {"class": "form-control", "placeholder": field.label}
```

但是这样是有bug存在，比如我们在定义一个字段时还可以先自定义widget组件数据，如`ep_name = forms.CharField(disabled=True, label="姓名",widget=forms.TextInput(attrs = {"class": "form-control"}))`这样是在定义字段还是就直接定义了，如果这样的话，再向上面那样的写法就会被覆盖掉，可以先判断是否为空再添加，例如：

```python
class eidtEpModelForm(forms.ModelForm):
    ep_name = forms.CharField(disabled=True, label="姓名",widget=forms.TextInput(attrs = {"class": "form-control"}))

    class Meta:
        model = employee
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # 先判断是否存在，存在就直接添加，没有在创建
            if field.widget.attrs:
             	field.widget.attrs["class"] = "form-control"
            else:
            	if field in ['ep_name', 'ep_brdata']:
                	field.widget.attrs = {"class": "form-control", "placeholder": field.label}
            	elif field in ['ep_dpid', 'ep_gender', 'ep_status']:
                	field.widget.attrs = {"class": "form-control", "placeholder": field.label}
            	else:
                	field.widget.attrs = {"class": "form-control", "placeholder": field.label}
```

但是如果每次都这么写的话很麻烦，可以结合面向对象的方法去重新定义一个样式父类，然后以后每次创建ModelForm是直接继承就行，后续就会共享同一个属性了

如：

**BootstrapModelForm父类**

```python
from django import forms

class BootstrapModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # 先判断是否存在，存在就直接添加，没有在创建
            if field.widget.attrs:
                field.widget.attrs["class"] = "form-control"
            else:
                field.widget.attrs = {"class": "form-control", "placeholder": field.label}
```

**继承**

```python
class eidtEpModelForm(BootstrapModelForm):
    class Meta:
        model = employee
        fields = '__all__'
```

以后就这么写，可以避免过多的重复代码

#### 12.规范

在开发中，为了方面维护和可读性，必须规范

```
1.创建app来区分各个功能。记得创建完要注册

2.在app中创建static来存放静态文件
	-css 存放css样式文件
	-js 存放编写完的js文件
	-img 存放相片
	-plugins 存放外部插件，如Bootstrap

3.创建templates来存放html模板，添加模板配置[os.path.join(BASE_DIR,"templates")]

4.创建utils来存放公用功能文件的存放，如数据库、各种父类等

5.创建，ModelForm/form来存放对应脚本

6.对视图view的脚本不一定全部都要存放在view.py里面，如果想要每个都存放一个py也可以，可以创建一个目录来存放，最后可以将views.py删除

7.models不能进行拆分，注意
```

#### 13.密码输入

当有一个字段是密码输入时，在ModelForm中可以这么写

```python
class add_admin(BootstrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )

    class Meta:
        model = admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)  # render_value=True就是当输入的密码有问题时不会被清空
        }
```

这里是表示确认密码的，其中添加widgets插件forms.PasswordInput就是表示这一列是密码框，如果给定参数render_value是表示当输入密码不正确或者不符合规则时，密码框不会被清除，默认情况下，密码框都会被清除的

#### 14.密码加密

在规范中，一般密码都是进行加密存储的，我们可以将加密方式存放到共用组件目录下，列入在utils中创建一个encrypt来存储加密方法。这里是md5加密方法

```python
from django.conf import settings  # 导入配置文件
import hashlib


def md5(data_string):
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))  # 加盐，用Django配置文件自带的字符串
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()
```

这里用的是Django随机生成的字符串来进行加盐的

密码验证时在ModelForm中的情况

```python
class add_admin(BootstrapModelForm):
    confirm_password = forms.CharField(
        label="确认密码",
        widget=forms.PasswordInput
    )

    class Meta:
        model = admin
        fields = ["username", "password", "confirm_password"]
        widgets = {
            "password": forms.PasswordInput(render_value=True)  # render_value=True就是当输入的密码有问题时不会被清空
        }

    def clean_password(self):
        pwd = self.cleaned_data["password"]
        return md5(pwd)

    def clean_confirm_password(self):
        # 这里再次获取到的password的数据就是前面加密过的了，因为执行是有顺序的
        text_password = self.cleaned_data["password"]
        text_confirm_password = md5(self.cleaned_data["confirm_password"])
        if text_password != text_confirm_password:
            raise ValidationError("两次输入号码不正确")
        return text_confirm_password

```

这样的话就会改变前端用户输入的值了，结果就是加密后的值，因为验证是顺序的，所以后面的钩子方法拿到的密码也就是加密完的了

**在钩子方法中可以通过print(self.instance.id)获取instance=row_object输入的数据值，如果是self.instance.pk就是id**

这个可以在前端例如修改密码时，前端没显示出对应的id，如果要获取id那么就必须通过前面的方式获取到传进去的id去查看原始的密码

#### 15.用户认证

##### 1.session&cookie

session是存储在服务端个人验证信息的键值对数据
cookie是存储在浏览器端个人验证信息的键值对数据

##### 2.登录页面及脚本

**html**

```html
{% load static %}
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>登录页面</title>
    <link rel="stylesheet" href="{% static 'css/login.css' %}">
        <script src="{% static 'js/jquery-3.6.3.js' %}"></script>
    <link rel="stylesheet" href="{% static 'plugins/bootstrap-3.4.1/css/bootstrap.css' %}">
    <link rel="stylesheet" href="{% static 'plugins/font-awesome-4.7.0/css/font-awesome.css' %}">
    <script src="{% static 'plugins/bootstrap-3.4.1/js/bootstrap.js' %}"></script>
  </head>
  <body>
    <div class="container">
      <h1 class="title">欢迎登录</h1>
      <form method="post" novalidate>
        {% csrf_token %}
        <div class="form-group">
        <label>用户名</label>
        {{ form.username }}
        <span style="color: red">{{ form.username.errors.0 }}</span>
        </div>
        <div class="form-group">
        <label>密码</label>
        {{ form.password }}
        <span style="color: red">{{ form.password.errors.0 }}</span>
        </div>
        <button type="submit" class="btn btn-primary">登录</button>
      </form>
    </div>
  </body>
</html>

```

**Form**

```python
from django import forms
from managepage.utils.encrypt import md5

class loginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control", "id": "exampleInputEmail1", "placeholder": "用户名"}),
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={"class": "form-control", "id": "exampleInputPassword1", "placeholder": "密码"}),
        required=True
    )
    def clean_password(self):
        pwd = self.cleaned_data["password"]
        return md5(pwd)
```

**view**

```python
def login(request):
    """  登录  """
    if request.method == "GET":
        form = loginForm()
        return render(request, "login.html", {"form": form})
    else:
        form = loginForm(data=request.POST)
        if form.is_valid():
            # 数据库验证，form.cleaned_data是存储原始数据的
            # 条件可以是字典，前提是字段跟key要对应
            admin_log = admin.objects.filter(**form.cleaned_data).first()
            if not admin_log:
                # form和ModelForm都可以用改方法添加错误信息,第一个是字段名
                form.add_error("password", "账号密码不存在")
                return render(request, "login.html", {"form": form})
            # 用户名密码正确
            # 网站生成随机字符串，写到用户浏览器的cookie中去，再保存到服务端的session中去
            # Django自带的方法，前端会保存Django自动生成的sessionid，字符串也会保存sessionid并且和以下对应的数据
            request.session["info"] = {'id': admin_log.id, 'username': admin_log.username,
                                       "password": admin_log.password}
            return redirect("/toadmin/")
        else:
            return render(request, "login.html", {"form": form})
```

·在判断账号密码时，可以将验证的数据字典直接去数据库查询，但是参数的形式是`**form.cleaned_data`cleaned_data是数据字典
·form和ModelForm都可以继续往里面加错误信息，用`form.add_error("password", "账号密码不存在")`,第一个是字段，第二个是错误信息
·Django自带的session方法，设置后会自动向客户端浏览器中的cookie添加sessionid的数据，值是Django随机生成的字符串，而这个字符串是我们保存在服务端session数据的key，值是我们设置的数据
·添加方法用request.session，可以随便定义名字，这个名字是后续获取数据的key

后台获取session数据方法如：

`request.session["info"]`:这个呢如果用户没登录过的话就会报存
`request.session.get("info")`：这个呢如果用户没登录获取到的就是None，不会保存

##### 3.登录验证步骤

登录验证步骤就是在每个需要验证的函数里，写上`request.session["info"]`/`request.session.get("info")`获取用户的登录信息，如果有那么就给访问，没有就跳转到登录页面。

在这里还需要多做几步验证，拿到数据后还要验证用户名、密码等是否准确的一系列操作...

登录成功后：
·cookie，生成随机字符串保存在客户端
·session，存储要存储的用户数据到服务端
·验证，拿到用户的cookie值去验证session数据

##### 4.使用中间件进行验证

```python
from django.utils.deprecation import MiddlewareMixin
from managepage.models import admin
from django.shortcuts import redirect, render

class AutoLogin(MiddlewareMixin):
    def process_request(self, request):
        # 1.排除不需要登录验证的链接
        pc_url = ["/login/"]
        if request.path_info in pc_url:
            return
        info_dict = request.session.get("info")
        # 有cookie数据
        if info_dict:
            # 验证账号密码是否存在或者密码是否正确
            admin_log = admin.objects.filter(**info_dict).first()
            # 正确情况，继续走下去
            if admin_log:
                return
            # 不正确情况进去登录界面
            request.session.clear()
            return redirect("/login/")
        return redirect("/login/")

```

注册

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'managepage.middleware.auth.AutoLogin'
]
```



#### 16.Django中间件

中间件顾名思义，是介于request与response处理之间的一道处理过程，相对比较轻量级，并且在全局上改变django的输入与输出。因为改变的是全局，所以需要谨慎实用，用不好会影响到性能

在Django中setting里MIDDLEWARE就是中间件的注册表，执行顺序是从上到下的

##### 1.中间件的使用

中间件类必须继承自`django.utils.deprecation.MiddlewareMixin`类

中间件类必须实现下列五个方法中的一个或多个

- `process_request(self,request)`：  **请求时做的操作**
  作用：执行主路由之前被掉用，在每个请求上调用，返回None(请求通过)或者HttpResponse对象(请求不通过)
  用途：过滤请求

- `process_view(self,request,callback,callback_args,callback_kwargs)`:
  作用：callback：为视图函数；callback_args：视图函数的位置参数,callback_kwargs：视图函数的关键字参数；调用视图之前被调用，在每个请求上调用，返回None(请求通过)或者HttpResponse对象(请求不通过)
  用途：用于代码层面的替换和过滤，这个方法可以拿到视图函数的参数

- `process_response(self,request,response)`： **响应时做的操作**
  作用：response：即是视图函数的响应对象；在所有响应返回浏览器之前被调用，在每个请求上调用，返回HttpResponse对象

- `process_exception(self,request,exception)`：
  作用：处理过程中抛出异常时被调用，返回一个HttpResponse对象
  用途：用于一般用于捕获发生的异常，并将其邮件发送给开发人员

- `process_template_response(self,request,response)`：
  作用：在视图函数执行完毕，且视图函数返回的对象中包含render方法时被调用；该方法需要返回实现了render方法的响应对象

  **注：中间件中的大多数方法在返回None时表示忽略当前操作进入下一项事件,当返回HttpResponse对象时，表示此请求结束，直接返回给客户端**

中间件可以编写在不用的py文件下。并且必须是一个类，示例：

```python
# file:mymiddleware.py
from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
import re
class MWare(MiddlewareMixin):
   count_dict = {} #创建用于统计次数的字典
   def process_request(self,request):
      request_ip = request.META['REMOTE_ADDR'] #获取请求IP
      request_url = request.path_info #获取请求URL
      if re.match(r'^/test',request_url): #匹配请求是否以/test开头
            times = self.count_dict.get(request_ip,0) #查询当前IP的请求次数，默认为0
            self.count_dict[request_ip]= times + 1 #请求次数 + 1
            if times < 5: #如果请求次数＜5次，请求正常通过
               return
            else: #如果请求次数＞5次，则返回HttpResponse，阻止请求
               return HttpResponse("访问次数超过5次，请求失败")
      else: #如果不是以/test开头则直接正常通过
            return

```

注册中间件

```python
# file:settings.py
MIDDLEWARE = [
   ....,
   'middleware.mymiddleware.MWare',
]

```

中间件在发起请求到视图函数的中间执行的操作是process_request,视图到浏览器的中间件是process_response

**如果在process_request中没回返回值或者返回none，那么说明请求可以继续往回走，否则就只能停止走，从response返回**

#### 17.用户注销

用户注销其实就是清除当前的session数据信息，在Django使用`request.session.clear()`进行清除当前的session信息，示例：

```python
def outlogin(request):
    request.session.clear()
    return redirect('/login/')
```

在前端中，如果有传request给前端，那么可以直接在前端中使用`{{ request.session.info.username }}`获取数据

因为在中间件已经判断是否有session了，所以在这里可以直接取消

#### 18.验证码

##### 1.随机生成验证码方式

参考网站：https://www.cnblogs.com/wupeiqi/articles/5812291.html

```python
import random

from PIL import Image, ImageDraw, ImageFont, ImageFilter


def check_code(width=120, height=30, char_length=5, font_file='kumo.ttf', font_size=28):
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')

    def rndChar():
        """
        生成随机字母
        :return:
        """
        return chr(random.randint(65, 90))

    def rndColor():
        """
        生成随机颜色
        :return:
        """
        return random.randint(0, 255), random.randint(10, 255), random.randint(64, 255)

    # 写文字
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = rndChar()
        code.append(char)
        h = random.randint(0, 4)
        draw.text([i * width / char_length, h], char, font=font, fill=rndColor())

    # 写干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())

    # 写干扰圆圈
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())

    # 画干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)

        draw.line((x1, y1, x2, y2), fill=rndColor())

    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img, ''.join(code)


if __name__ == '__main__':
    # 1. 直接打开
    img,code = check_code()
    img.show()

    # 2. 写入文件
    # img,code = check_code()
    # with open('code.png','wb') as f:
    #     img.save(f,format='png')

    # 3. 写入内存(Python3)
    # from io import BytesIO
    # stream = BytesIO()
    # img.save(stream, 'png')
    # stream.getvalue()

    # 4. 写入内存（Python2）
    # import StringIO
    # stream = StringIO.StringIO()
    # img.save(stream, 'png')
    # stream.getvalue()
```

##### 2.前端代码

```html
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>登录页面</title>
    <link rel="stylesheet" href="{% static 'css/login.css' %}">
    <script src="{% static 'js/jquery-3.6.3.js' %}"></script>
    <link rel="stylesheet" href="{% static 'plugins/bootstrap-3.4.1/css/bootstrap.css' %}">
    <link rel="stylesheet" href="{% static 'plugins/font-awesome-4.7.0/css/font-awesome.css' %}">
    <script src="{% static 'plugins/bootstrap-3.4.1/js/bootstrap.js' %}"></script>
</head>
<body>
<div class="container1">
    <h1 class="title">欢迎登录</h1>
    <form method="post" novalidate>
        {% csrf_token %}
        <div class="form-group">
            <label>用户名</label>
            {{ form.username }}
            <span style="color: red">{{ form.username.errors.0 }}</span>
        </div>
        <div class="form-group">
            <label>密码</label>
            {{ form.password }}
            <span style="color: red">{{ form.password.errors.0 }}</span>
        </div>
        <label for="yzminput">请输入验证码</label>
        <div class="yzm">
            <div class="row">
                <div class="col-md-7">
                    <input id="yzminput" class="form-control" placeholder="请输入验证码" name="yzm">
                </div>
                <div class="col-md-5">
                    <img src="/image/code/" alt="加载不出来">
                </div>
            </div>
        </div>
        <span style="color: red">{{ err }}</span>
        <button type="submit" class="btn btn-primary">登录</button>
    </form>
</div>
</body>
</html>
```

##### 3.前端获取

在登录界面将img的src改成一个url，直接访问url获取图片

```html
<div class="col-md-5">
    <img src="/image/code/" alt="加载不出来">
</div>
```

再将生成代码的脚本放到Django目录中去，我们这里只需要一个对象去调用，所有不需要main方法

记得在中间件把这个图片的url去掉验证

路由也改加上去

```python
path('image/code/', account.image_code)
```

注意：字体文件如果没写路径的话应该吧字体放到Django的根目录下

##### 4.后端脚本

```python
from managepage.utils.code import check_code
from io import BytesIO  # 将数据写到内存中去

def image_code(request):
    img, code = check_code()  # 调用
    stream = BytesIO()  # 创建一个内存地址
    img.save(stream, 'png')  # 将图片保存到内存中去

    return HttpResponse(stream.getvalue())
```

##### 5.验证码内容存储

验证码验证需要用户从前端输入之后给后端做验证，在这里呢我们可以通过code获取到我们要的验证码数据，但是前提是怎么给用户做绑定，并且不同用户登录不受影响，这个就得用到session了，可以通过session生成一个字符串给cookie，我们可以通过session将我们要的数据进行保存到数据库，并且设置过期时间。示例：

```python
def image_code(request):
    img, code = check_code()  # 调用

    # 将数据写到session中，前端验证通过这个获取
    request.session['image_code'] = code
    # 设置session失效时间
    request.session.set_expiry(60)

    stream = BytesIO()  # 创建一个内存地址
    img.save(stream, 'png')  # 将图片保存到内存中去
    return HttpResponse(stream.getvalue())
```

直接在获取图片的函数中就可以设置session了

##### 6.验证码验证

验证码验证需要先在ModelForm或者form中添加一列验证码的字段，并且前端要把输入验证码的框改变一下，示例

**Form**

```python
from django import forms
from managepage.utils.encrypt import md5


class loginForm(forms.Form):
    username = forms.CharField(
        label="用户名",
        widget=forms.TextInput(attrs={"class": "form-control", "id": "exampleInputEmail1", "placeholder": "用户名"}),
        required=True
    )
    password = forms.CharField(
        label="密码",
        widget=forms.PasswordInput(attrs={"class": "form-control", "id": "exampleInputPassword1", "placeholder": "密码"}),
        required=True
    )

    code = forms.CharField(
        label="验证码",
        widget=forms.TextInput(attrs={"class": "form-control", "id": "exampleInputEmail1", "placeholder": "验证码"}),
        required=True
    )
    
    def clean_password(self):
        pwd = self.cleaned_data["password"]
        return md5(pwd)
```

**login**

```python
def login(request):
    """  登录  """
    if request.method == "GET":
        form = loginForm()
        return render(request, "login.html", {"form": form})
    else:
        form = loginForm(data=request.POST)
        if form.is_valid():
            """
                验证码做验证
            """
            user_input_code = form.cleaned_data.pop('code')  # 获取code数据并且从字典中删除，因为后面我们要查询和保存数据这字段是没有的
            code = request.session.get('image_code', "")  # 获取生成的验证码数据保存在session中的code数据，过期获取不到就为空
            if code == "":
                form.add_error("code", "验证码过期，请重新输入")
                return render(request, "login.html", {"form": form})
            # 转大写做验证
            if code.upper() != user_input_code.upper():
                form.add_error("code", "验证码不正确")
                return render(request, "login.html", {"form": form})

            """
                账号密码做验证
            """
            # 数据库验证，form.cleaned_data是存储原始数据的
            # 条件可以是字典，前提是字段跟key要对应
            admin_log = admin.objects.filter(**form.cleaned_data).first()
            if not admin_log:
                # form和ModelForm都可以用改方法添加错误信息,第一个是字段名
                form.add_error("password", "账号密码不存在")
                return render(request, "login.html", {"form": form})

            """
                账号密码验证码正确
            """
            # 网站生成随机字符串，写到用户浏览器的cookie中去，再保存到服务端的session中去
            # Django自带的方法，前端会保存Django自动生成的sessionid，字符串也会保存sessionid并且和以下对应的数据
            request.session["info"] = {'id': admin_log.id, 'username': admin_log.username,
                                       "password": admin_log.password}
            # 因为获取验证码时设置了session的过期时间，所以这里要重新设置，不然这里的session也是60秒过期
            request.session.set_expiry(60 * 60 * 24 * 7)

            return redirect("/user/")
        else:
            return render(request, "login.html", {"form": form})
```

在这里内需要注意的是我们在获取验证码时给session设置了失效为60秒，因为用的是通过sessionid，所以注意把session失效修改一下时间。

有一个bug就是我只要重新访问login页码session的失效时间就会变成60秒，60秒后就得重新登录了。解决方法可以获取sessionid，将数据保存到其它地方，并且在其它地方做验证

**html**

```html
{% load static %}
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>登录页面</title>
    <link rel="stylesheet" href="{% static 'css/login.css' %}">
    <script src="{% static 'js/jquery-3.6.3.js' %}"></script>
    <link rel="stylesheet" href="{% static 'plugins/bootstrap-3.4.1/css/bootstrap.css' %}">
    <link rel="stylesheet" href="{% static 'plugins/font-awesome-4.7.0/css/font-awesome.css' %}">
    <script src="{% static 'plugins/bootstrap-3.4.1/js/bootstrap.js' %}"></script>
</head>
<body>
<div class="container1">
    <h1 class="title">欢迎登录</h1>
    <form method="post" novalidate>
        {% csrf_token %}
        <div class="form-group">
            <label>用户名</label>
            {{ form.username }}
            <span style="color: red">{{ form.username.errors.0 }}</span>
        </div>
        <div class="form-group">
            <label>密码</label>
            {{ form.password }}
            <span style="color: red">{{ form.password.errors.0 }}</span>
        </div>
        <label for="yzminput">请输入验证码</label>
        <div class="yzm">
            <div class="row">
                <div class="col-md-7">
                    {{ form.code }}
                    <span style="color: red">{{ form.code.errors.0 }}</span>
                </div>
                <div class="col-md-5">
                    <img src="/image/code/" alt="加载不出来">
                </div>
            </div>
        </div>
        <span style="color: red">{{ err }}</span>
        <button type="submit" class="btn btn-primary">登录</button>
    </form>
</div>
</body>
</html>
```

#### 19.Ajax请求

浏览器向网站发送请求时:url和表单的形式提交

- GET
- POST

特点：页码刷新

- 依赖jQuery
- 编写Ajax代码

```js
$.ajax({
	url:"发送的地址",
	type:"get",
	data:{
		n1:123,
		n2:233
	},
	success:function(res){
		console.log(res);
	}
})
```

##### 1.实例

**前端**

```js
<script type='text/javascript'>
	function clickMe() {
		$.ajax({
            url:"/task/ajax",
            type:"get",
            data:{
                n1:123,
                n2:233
            },
            success:function(res){
                console.log(res);
            }
        })
	}
</script>
```

只要某个标签绑定了clickMe函数的事件，触发就能实现。后端只需要返回一串数据就行，或者json

如果向后端发送post请求时，或触发csrf机制，这个时候记得给后端的函数设置排除csrf机制的验证，实例

```
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def task_ajax(request):
	return HttpResponse('成功了')
```

##### 2.返回json数据

后端返回json数据要将字典转换一下，`json.dump(dict)`

后端也可以通过`return JsonResponse({})`返回json数据

ajax获取到的全部是字符串数据，要转成json数据必须指定类型

<script type='text/javascript'>
	function clickMe() {
		$.ajax({
            url:"/task/ajax",
            type:"get",
            data:{
                n1:123,
                n2:233
            },
            dataType: "JSON",
            success:function(res){
                console.log(res);
                console.log(res.status);
            }
        })
	}
</script>

##### 3.ajax获取表单的值

获取单个id的输入框的值

```
<script type='text/javascript'>
	function clickMe() {
		$.ajax({
            url:"/task/ajax",
            type:"get",
            data:{
                n1:$("#name).val()",
                n2:$("#pwd).val()"
            },
            dataType: "JSON",
            success:function(res){
                console.log(res);
                console.log(res.status);
            }
        })
	}
</script>
```

获取整个表单中所有输入框，在这里后端拿到的数据是一个字典对象，key是name值，value是一个列表数据

```
<script type='text/javascript'>
	function clickMe() {
		$.ajax({
            url:"/task/ajax",
            type:"get",
            data:$("#form3).serialize(),
            dataType: "JSON",
            success:function(res){
                console.log(res);
                console.log(res.status);
            }
        })
	}
</script>
```

#### 20.后端验证数据返回成json

前面我们返回给前端的错误信息都是一个html格式的。然后前后端分离的话就必须是返回一个json数据的，示例

```
data_dict = {"status":true, "error": form.errors}
return HttpResponse(json.dumps(data_dict,ensure_ascil=False))

或者
retutn JsonResponse({"status":true, "error": form.errors})
```

#### 21.前后端交互

##### 1.jQuery的ajax应用

```js
<script type="text/javascript">
	// 设置页面加载完成自动加载会在DOM加载完成之后执行
	$(function(){
		bindBtnAddEvent();  // 调用函数
	})
	
	function bindBtnAddEvent(){
		$.ajax({
            url:"/task/ajax",
            type:"get",
            data:$("#form3).serialize(),
            dataType: "JSON",
            success:function(res){
                console.log(res);
                console.log(res.status);
            }
        })
	}
</script>
```

在后续可以使用这种形式去写jQuery操作，前后端交互，可以设置点击调用函数

删除的可以设置点击删除是把对应的id传给全局变量，因为在弹出框那里是拿不到id的，只能去读取全局变量的id，所以就在弹出框那里去获取对应的id，然后把id传给后端，让后端执行操作。

弹出框的显示和关闭可以看插件里面的介绍，有说怎么使用

##### 2.后端访问数据库直接返回字典

```python
row_dict = models.Order.objects.filter(id=111).values("id","title").first()

返回：{"id":xxx,"title":xxx}

获取多条数据时，是一个列表套着字典

如果想返回字典给前端的可以直接这么写，比较方便


models.Order.objects.filter(id=111).values_list("id","title")

返回：[(xxx,xxx),(xxxx,xxx)]
```

##### 3.常用的jQuery操作

`````js
给指定id添加内容
$("#xxx").val("");

清空填写内容
$("#xxx")[0].reset();

刷新页面
location.reload();

获取列表的值
dict.data

修改
dict.data = res.data
`````

#### 22.可视化

可视化选择用Echarts，有很多图表可以用，用法在官网都可以找到。

https://echarts.apache.org/examples/zh/index.html

直接看官网教程

如果页面的搭配可以拿插件的栅格布局

#### 23.文件上传

文件上传如果表单这么写的话，后端获取到的数据只有是文件名，没有文件

```html
<form method="post">
	{% csrf_token %}
	<input type="text" name="username">
	<input type="file" name="avatar">
	<input type="submit" value="提交">
</form>



这样的话后端获取的数据只要上传的文件名
```

需要在表单属性中添加enctype="multipart/form-data"

```html
<form method="post">
	{% csrf_token %}
	<input type="text" name="username">
	<input type="file" name="avatar">
	<input type="submit" value="提交">
</form>


后端通过：
requests.POST 获取的是请求体的数据

requests.FILES  获取的是发过来的数据对象
```

获取方法：

`````python
file_object = request.FILES.get("avatar")
print(file_object.name)  # 文件名：改变过的文件名

# 获取文件，分块读取
f = open(file_object.name,mode="wb")
for chunk in file_object.chunks():
    f.write(chunk)
f.close()
`````

#### 24.上传Excel并且多操作

这里的上传Excel可以直接把数据上传上去，比如说批量添加员工，然后用Excel上传，后台做操作将数据保存进去，但是在这里我们不想把数据文件保存下来，想直接打开并且操作，可以用`openpyxl`打开数据，他这里上传可以是文件路径和文件对象，我们在获取到前端上传的表单数据时就是一个对象，可以将这个上传

`````python
from openpyxl import load_workbook
def depatr_multi(request):
    file_object = request.FILES.get("exec")
    wb = load_workbook(file_object)  # 直接把文件对象传进去
    sheet = wb.worksheets[0]
`````

#### 25.Form上传

上传的数据文件通过Form进行验证，如果调用Form验证是，必须将数据和文件都给过去

```
form = UpForm(data=request.POST,files=request.FILES)

这个时候获取到的数据是这样的
如：
form.cleaned_data  # {"name":xxx,age:13,"img":图片对象}

如果想将图片保存到数据库的步骤：
1.将文件读取完保存到本地路径上
2.将路径保存到数据库
3.读取时直接域名+路径；如：127.0.0.1:8000/static/img/xxx.img
```

#### 26.ModelForm上传

在Django的开发中两个特殊的文件夹

- static：存放静态文件的路径，包括：css、js、项目图片
- media：存放用户上传的数据

##### 启动media目录

1.需要在urls.py中加上

```
from django.urls import path,re_path
from django.views.static import serve
from django.conf import settings

re_path(r'^media/(?P<path>.*)$',serve,{'document_root':settings.MEDIA_ROOT},name='media'),
```

2.在settings.py中配置

`````py
import os

MEDIA_ROOT = os.path.join(BASE_DIR,"media")
MEDIA_URL = '/media/'
`````

后续所有上传的数据都保存在media目录下，访问如下：127.0.0.1:8000/media/1.png

文件保存就用：

`os.path.join('media',image_obj.name)`  在数据库形式：media/111.png

访问直接拼接就行了

##### models

`````python
class City(models.Model):
    name = models.CharField(verbose_name="名称", max_length=32)
    counr = models.IntegerField(verbose_name="人口")
    # FileField本质上也是CharField，好处就是自动保存数据,自动保存到media的city路径下，存储数据是路径
    img = models.FileField(verbose_name="Logo", max_length=128,upload_to='city/')
`````

##### ModelForm

`````python
from app01.utils.bootstrap import BootStrapModelForm

class UpModelForm(BootStrapModelForm):
    class Meta:
        model = models.City
        fields = "__all__"
`````

在这里如果前端上传的数据验证通过了，直接`form.save()`保存就行了

数据库中保存的路径是：city/1111.png1

如果上传的文件名是一样的，那么Django会自动在文件名后面随机加字符串



##### 例子，通过ajax上传

**ModelForm**

````python
class add_projrct_info(ModelForm):
    class Meta:
        model = project_info
        fields = ["project_name", "project_file", "remarks"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # 先判断是否存在，存在就直接添加，没有在创建
            if name == "project_file":
                field.widget.attrs = {"class": "form-group", "placeholder": field.label}
            else:
                if field.widget.attrs:
                    field.widget.attrs = {"class": "form-control", "placeholder": field.label}
                else:
                    field.widget.attrs = {"class": "form-control", "placeholder": field.label}

    def clean_project_file(self):
        file = self.cleaned_data.get("project_file")
        if not file:
            raise ValidationError("请上传文件")
        elif file.size > 20 * 1024 * 1024:
            raise ValidationError("文件太大，请上传小于20M的文件")
        return file
````

**model**

```python
class project_info(models.Model):
    id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=32, null=False, blank=False, verbose_name="项目名称")
    person = models.CharField(max_length=16, null=False, blank=False, verbose_name="负责人")
    project_file = models.FileField(verbose_name="脚本路径", upload_to='project_file/%Y/%m/%d/')
    upload_date = models.DateField(null=False, blank=False, verbose_name="上传时间")
    change_date = models.DateField(null=True, blank=True, verbose_name="最近一次更改时间")
    remarks = models.CharField(max_length=128, null=True, blank=True, verbose_name="备注")

    class Meta:
        db_table = 'projrct_info'
        verbose_name = '项目信息表'
```

**前端**

```html
<form method="post" novalidate id="add_form" enctype="multipart/form-data">
{% csrf_token %}
    <div class="modal-body">
            {% for i in form %}
                <span>{{ i.label }}</span>{{ i }}
                <span class="error-ts" style="color: red;" id={{ i.name }}></span><br>
            {% endfor %}
    </div>
    <div class="modal-footer">
        <button type="button" class="btn btn-default" data-dismiss="modal">关闭</button>
        <button type="button" class="btn btn-primary" onclick="bindBtnAddEvent()">提交</button>
    </div>
</form>
```

**ajax**

```python
   <script type="text/javascript">

   function bindBtnAddEvent(){
        $.ajax({
            url:"/add_project/",
            type:"POST",
            {#data:$("#add_form").serialize(),#}
            data:new FormData($("#add_form")[0]),
            dataType: "JSON",
            processData : false,
            contentType: false,
            success:function(res) {
                alert("添加成功");
                window.location.reload();
            },
            error: function (xhr, status, error) {
                $('.error-ts').html("")
                var errors = JSON.parse(xhr.responseText).errors;
                for (var field in errors) {
                    if (errors.hasOwnProperty(field)) {
                        var errorMessages = errors[field];
                        var field_id = $("#" + field);
                        field_id.html(errorMessages);
                    }
                }
            }
        })
   }
</script>
```

ajax这里在两个情况下执行操作，失败是前获取报错信息标签清空，然后获取后端返回的json数据中的errors的值，后端传过来要对应，然后循环，并且找到指定id添加报错信息，这里的field是列名

**view**

```python
def add_project(request):
    if request.method == "POST":
        print(request.FILES)
        form = add_projrct_info(request.POST, request.FILES)
        # print(form.cleaned_data)
        if form.is_valid():
            article = form.save(commit=False)  # 创建一个Article对象但不保存到数据库中
            article.person = "袁润和"  # 添加person属性
            # 获取当前日期和时间
            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            article.upload_date = date_str
            article.change_date = date_str
            article.save()  # 保存到数据库
            return JsonResponse({"suc": "True"})
        else:
            errors = {}
            for field, messages in form.errors.items():
                errors[field] = messages
            return JsonResponse({"errors": errors}, status=400)
```

# 做项目中添加的笔记

### 1.form操作

当form或者ModelForm在通过is_valid时，如果要添加值，可以这么操作

```
        if form.is_valid():
            article = form.save(commit=False)  # 创建一个Article对象但不保存到数据库中
            article.person = "袁润和"  # 添加person属性
            # 获取当前日期和时间
            now = datetime.now()
            date_str = now.strftime("%Y-%m-%d")
            article.upload_date = date_str
            article.change_date = date_str
            article.save()  # 保存到数据库
            return JsonResponse({"suc": "True"})
```

### 2.jQuery常用操作

在日常的交互中，ajax写法如下：

```js
function addNote() {
    // const formData = new FormData(this);
    $.ajax({
        url: '/add_note/',
        type:'POST',
        data: new FormData($("#addModelForm").get(0)),
        // data: formData,
        dataType: "JSON",
        processData: false,
        contentType: false,
        success: function (response) {
            $('#add_err').empty();
            if (response.success) {
                window.location.reload()
            }else {
                // $('.adderr').after('<span id="add_err" style="color: red">'+response.err+'</span>')
                $('#add_err')[0].innerHTML = response.err
            }
        }
    })
}
```

### 3.附件下载

```python
from django.http import JsonResponse, FileResponse, Http404

def load_note(request, nid):
    file_object = note_info.objects.filter(id=nid).first()
    if file_object:
        try:
            file_name = str(file_object.note_file.path).split("\\")[-1]
            file = open(file_object.note_file.path, 'rb')
            response = FileResponse(file)
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = f'attachment; filename="{file_name}"'.encode('utf-8', 'ISO-8859-1')
            return response
        except Exception:
            raise Http404
```

这样下载如果前端点击下载就直接会把附件下载下来

### 4.models的附件设置

#### setting设置

```
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
MEDIA_URL = '/media/'
```

#### models

```python
class note_info(models.Model):
    id = models.AutoField(primary_key=True)
    note_name = models.CharField(max_length=32, null=False, blank=False, verbose_name="笔记名称")
    person = models.CharField(max_length=16, null=False, blank=False, verbose_name="负责人")
    note_file = models.FileField(verbose_name="笔记路径", upload_to='note_file/%Y/%m/%d/')
    upload_date = models.DateField(null=False, blank=False, verbose_name="上传时间")
    remarks = models.CharField(max_length=128, null=True, blank=True, verbose_name="备注")

    class Meta:
        db_table = 'note_info'
        verbose_name = '笔记管理表'
```

upload_to是下载的路径，后面是表示年月日

#### url

```
# 附件
re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
```

#### js

```js
// 项目添加
function bindBtnAddEvent() {
    $.ajax({
        url: "/add_project/",
        type: "POST",
        data: new FormData($("#add_form")[0]),
        dataType: "JSON",
        processData: false,
        contentType: false,
        beforeSend: function () {
            $.LoadingOverlay("show");
        },
        success: function (res) {
            window.location.reload();
        },
        error: function (xhr, status, error) {
            $('.error-ts').html("")
            var errors = JSON.parse(xhr.responseText).errors;
            console.log(errors);
            for (var field in errors) {
                if (errors.hasOwnProperty(field)) {
                    var errorMessages = errors[field];
                    var field_id = $("#" + field);
                    field_id.html(errorMessages);
                }
            }
        },
        complete: function () {
            // 隐藏加载指示器
            $.LoadingOverlay("hide");
        }
    });
}


// 项目修改
$(function () {
    $('.edit-btn').click(function () {
        var id = $(this).data('id');
        $.ajax({
            url: '/edit_project/',
            type: 'GET',
            dataType: 'json',
            data: {'id': id},
            success: function (response) {
                // 获取模态框的位置
                let edm = $('#editModal');
                // 将内容渲染进去，记得后端返回应该是form.as_p()
                // edm.find('.modal-body').find('#edit_form').html(response.form);
                edm.find('.modal-body').find('#edit_form').find(".modal-body1").html(response.form);

                // 保存选项
                $('#save-btn').click(function () {
                    $.ajax({
                        url: '/edit_project/',
                        type: 'POST',
                        data: new FormData($("#edit_form")[0]), // 得用这种方法才能拿到上传得文件
                        // data:  $('#edit_form').serialize(), // 得用这种方法才能拿到上传得文件
                        dataType: "JSON",
                        processData: false,
                        contentType: false,
                        success: function (response) {
                            console.log(1111)
                            if (response.success) {
                                // 验证成功，关闭弹框并刷新页面
                                $('#editModal').modal('hide');
                                location.reload();
                            } else {
                                // 验证失败，显示错误信息
                                edm.find('.error').remove();
                                console.log(response.errors)
                                for (var field_name in response.errors) {
                                    var field_errors = response.errors[field_name];
                                    var field_input = $('#editModal').find('[name=' + field_name + ']');
                                    field_input.after('<span class="error">' + field_errors.join(', ') + '</span>');
                                }
                            }
                        }
                    });
                });
                edm.modal('show');  // 显示模块
            }
        });
    });
});

// 项目删除
$(function () {
    $(".del-btn").click(function () {
        const id = $(this).data('id');
        let edm = $('#delModal');
        edm.modal('show');  // 显示模块
        $('#del-btn').click(function () {
            $.ajax({
                url: '/del_project/',
                type: 'POST',
                data: {'id': id},
                dataType: "JSON",
                success: function (response) {
                    if (response.success) {
                        $('#delModal').modal('hide');
                        location.reload();
                    } else {
                        alert("删除失败")
                    }
                }
            });
            $('#delModal').modal('show');
        });
    })
})

// 图书按钮监听
$(function (){
    $('.addbtn').click(function () {
                $('#add_err')[0].innerHTML = "";
    })
});

// 添加笔记
function addNote() {
    // const formData = new FormData(this);
    const errpt = $('#add_err');
    $.ajax({
        url: '/add_note/',
        type:'POST',
        data: new FormData($("#addModelForm").get(0)),
        // data: formData,
        dataType: "JSON",
        processData: false,
        contentType: false,
        success: function (response) {
            errpt.empty();
            if (response.success) {
                window.location.reload()
            }else {
                // $('.adderr').after('<span id="add_err" style="color: red">'+response.err+'</span>')
                errpt[0].innerHTML = response.err
            }
        }
    })
}

// 笔记删除
$(function () {
    $(".delbtn").click(function () {
        $("#note_del_Modal").modal('show');
        const id = $(this).data('id');
        $('.note_del').click(function () {
            $.ajax({
                url: "/del_note/",
                data: {"id": id},
                type: 'POST',
                dataType: "JSON",
                success: function (response) {
                    if (response.success) {
                        window.location.reload()
                        console.log("成功");
                    }else {
                        console.log("失败")
                    }
                }
            })
        })
    });
});
```

#### setting

在配置文件中，见debug设置为False时，访问了一些非路由的url就不会显示出具体报错，但是如果ALLOWED_HOSTS时是访问不了网站的。

改成false后，django就不会自动取加载静态文件，前端页码有一些样式显示不出来，这个时候就要修改启动方式了。

如果在生产环境上，就应该用nginx,apache来配置静态环境

```
DEBUG = False

ALLOWED_HOSTS = ['*']  # DEBUG改false后，这里也跟着改，本来是[]，改成这样后就加载不了静态文件了，用python manage.py 127.0.0.1:8000  --insecure启动
# 在正式环境下可以用nginx,apache来配置静态环境

python manage.py runserver 127.0.0.1:8000  --insecure
```

#### 文件夹上传

在前端要允许上传文件夹必须添加参数`<input type="file" name="directory" webkitdirectory="" >`在这里如果上传的是文件夹，其实是将文件夹内所有文件一并上传而已，而并不是将文件夹上传。

在后台用FILES获取到的是一个文件列表获取到的是一个列表，里面每个元素是一个文件，所以在前端要将文件夹名称和文件都传给后端，这里是ajax获取的。

```js
var form = document.getElementById("my-form");
var formContainer = $("#form-container");
$(function () {
    // 点击添加按钮
    // 这里是向另一个url请求的，并且将另一个网页给模态框的，具体将下面
    $(".btn-add").click(function () {
        $.ajax({
            url: "/add_folder/",
            type: "GET",
            dataType: "html",
            success: function (response) {
                formContainer.html(response);
                $(".add_modal").modal('show');
            },
            error: function (xhr, status, error) {
                console.log(error);
            }
        });
    });

    // 提交文件按钮，并且获取到数据给后端
    $(".sub_folder").click(function () {
        // 获取上传的文件
        const formData = new FormData($("#my-form")[0]);

        // 获取上传的文件夹名称
        const folderInput = $('#id_directory');
        const folderPath = folderInput[0].files[0].webkitRelativePath;
        const folderName = folderPath.split('/')[0];

        // 将文件夹名称添加到formData给后台
        formData.append("folderName",folderName)

        // const formData = new FormData(this);
        $.ajax({
            url: "/add_folder/",
            method: "POST",
            data: formData,
            processData: false,
            contentType: false,
            headers: {
                "X-CSRFToken": "{{ csrf_token }}"
            },
            success: function (response) {
                // 处理成功响应情况
                if (response.success) {
                    alert("表单提交成功！");
                    $(".add_modal").hide();
                    window.location.reload();
                }
            },
            error: function (xhr, status, error) {
                // 处理错误响应情况
                alert("表单提交失败，请重试！");
            }
        });
    })
})
```

视图

在视图中，如果是get请求是获取到ModelForm渲染给add_folder_model.html，在这里还将form_html进行.content转换成二进制，只要是能将内容渲染后给前端模态框渲染上去。这样就可以异步请求渲染上去了，返回的是一个HttpResponse

在post中，获取到刚添加的数据id可以给插入数据的操作赋值给一个变量，通过变量可以获取到对应的数据

```python
def add_folder(request):
    response = {}
    if request.method == "POST":
        form = UploadFolderForm(request.POST, request.FILES)
        if form.is_valid():
            Folder_name = request.POST['folderName']  # 文件夹名称
            uploaded_files = request.FILES.getlist('directory')  # 获取文件列表
            # 第一层保存
            new_yunpan_first = yunpan_first.objects.create(file_name=Folder_name, file_type=3, person="袁润和")
            new_yunpan_first_id = new_yunpan_first.id

            # 第二层保存
            for uploaded_file in uploaded_files:
                try:
                    yunpan_second.objects.create(file_name=uploaded_file.name, file=uploaded_file, file_type=2, person="袁润和", ParentID_1_id=new_yunpan_first_id)
                except Exception as e:
                    print(f'Error: {e}')

            response['success'] = "success"
            return JsonResponse(response)
        else:
            response['err'] = "上传失败"
            return JsonResponse(response)
    else:
        form = UploadFolderForm()
        # 将 ModelForm 渲染为 HTML 表单
        form_html = render(request, "add_folder_model.html", {"form": form}).content
        return HttpResponse(form_html)

```

add_folder_model.html

因为这里只需要一个from表单，所以只需要简简单单的生成一个表单就行了

```html
{% load static %}
    <script src="{% static 'plugins/bootstrap-3.4.1/js/bootstrap.min.js' %}"></script>
    <script src="{% static 'plugins/bootstrap-3.4.1/css/bootstrap.min.css' %}"></script>
{% csrf_token %}
{{ form.as_p }}
```


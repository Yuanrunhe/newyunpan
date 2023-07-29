源码：https://www.cnblogs.com/wupeiqi/articles/5433893.html
学习博客

## 一、web框架本质基于jinja模板渲染

**用来渲染的网页代码：**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>动态</title>
</head>
<body>
    <table>
        <thead>
            <th>ID</th>
            <th>用户名</th>
            <th>邮箱</th>
        </thead>
        <tbody>
            {% for row in data %}
                <tr>
                    <td>{{row.id}}</td>
                    <td>{{row.username}}</td>
                    <td>{{row.password}}</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
```

**python搭建的服务端代码**

```python
import socket
import threading
import pymysql
from jinja2 import Template

# 连接数据库操作
def l_mysql(user, password, db):
    db = pymysql.Connect(host="localhost",
                         port=3306,
                         user=user,
                         password=password,
                         db=db,
                         charset="utf8"
                         )
    return db


# f1-f3都是打开网页的函数
def f1():
    f = open("f1.html", 'r', encoding="utf-8")
    data = f.read()
    f.close()
    data = bytes(data, encoding="utf-8")
    return data


def f2():
    f = open("f2.html", 'r', encoding="utf-8")
    data = f.read()
    f.close()
    data = bytes(data, encoding="utf-8")
    return data


def f3():
    # mysql操作
    db = l_mysql("root", "1312014657", "ceshi")
    # 创建游标,将数据以字典形式存取
    cur = db.cursor(cursor=pymysql.cursors.DictCursor)
    # 执行SQL语句进行查询
    sql = """select id,username,password from userdata"""
    cur.execute(sql)
    user_list = cur.fetchall()
    cur.close()
    db.close()

    f = open("userdata.html", 'r', encoding="utf-8")
    data = f.read()
    f.close()

    # 基于第三方工具实现的模板渲染
    template = Template(data)
    data = template.render(data=user_list)
    print(data)
    return data.encode("utf-8")

    # data = bytes(data, encoding="utf-8")
    # return data


# 用来判断输入的是要打开哪个网页对应的函数名
wen_list = [
    ("/f1", f1), ("/f2", f2), ("/userdata.html", f3)
]


def conn_web(conn, ip):
    # print("客户端的ip和端口号为：", ip, "上线了")
    # 这里具体什么意思看网路编程基础笔记
    while True:
        data = conn.recv(4096)
        if data:
            funName = None
            data = data.decode("utf-8")
            # 如何判断网址的信息到底要打开哪个网站，在数据返回的
            # 信息里第一行中有，所以要将改信息提取出来进行判断
            heard, da = data.split("\r\n\r\n")
            temp = heard.split("\r\n")
            method, url, protato = temp[0].split(" ")
            for i in wen_list:
                if url == i[0]:
                    funName = i[1]
                    break
                else:
                    funName = b"404"
            if funName != b"404":
                rsp = funName()
            else:
                rsp = "404".encode("utf-8")
            conn.sendall(bytes('HTTP/1.1 201 OK\r\n\r\n', 'utf8'))
            conn.send(rsp)
        else:
            break
    conn.close()
    print("客户端的ip和端口号为：", ip, "下线了")


if __name__ == '__main__':
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)  # 表示服务端程序退出端口号立即释放
    s.bind(("", 8000))
    s.listen(5)

    while True:
        new_client, ip_port = s.accept()
        a = threading.Thread(target=conn_web, args=(new_client, ip_port))
        # 设置守护主线程，主线程退出所有主线程退出
        a.setDaemon(True)
        a.start()
```

**web框架本质梳理**

1、http：无状态，短连接
2、浏览器(socket客户端)
		网站（socket服务端）
3、自己写的网站
	a.socket服务器
	b.根据url不同返回不同的内容
			旅游系统：
				URL -> 函数
	c.字符串返回给用户
		模板引擎渲染
			HTML充当模板渲染就是将HTML中的特殊字符进行替换，替换成数据库里的数据)
			自己创造任意数据
		在代码中我们是打开html文件，然后返回的是字符串，在通过函数将HTML中内容进行替换，
		在这里打开的文件不要求后缀名是HTML，一个浏览器设别的都是HTML文件，我们传给客户端
		数据浏览器会以HTML样式进行解析，注意传入头在传入HTML文档，否则无法显示
	**（这上面就是web框架的本质）**

4.Web框架：
	框架种类：
		-包含a,b,c					-->比如Tornado，这三种都包括
		-[使用第三方a],b,c     -->比如Django，使用第三方的wsgiref来替代a
		-[第三方a],b,[第三方c]-->比如flask
	分类：
		-Django框架(因为Django提供了很多功能，调用即可)
		-其他

## 二、Django框架

#### 1、初始Django框架

**安装Django:**pip install django

**通过命令创建Django过程**

**创建Django文件，在终端执行，先切换到自己目录下**
	Django-admin startproject 文件名

**创建完里的文件介绍：**
	创建完成会出现一个与创建是给定的文件名相同的文件
	manage.py：一个实用的命令行工具，可让你以各种方式与该Django项目进行交互。(管理和运行就通过这个文件)

​	\__init__.py：一个空文件，告诉Python该目录是一个Python包
​	settings.py：该Django项目的设置/配置。
​	urls.py：该Django项目的URL声明，一份由Django驱动的网站“目录”。就是url和函数的对应关系(路由系统)
​	wsgi.py：一个WSGI兼容的Web服务器的入口，以便运行你的项目。(里面就是调用wsgiref模块)。web服务网关接口

**启动Django文件**
	只要创建好了，就可以运行了，代表已经创建一个网站了
	进入创建完的目录 cd 目录名
	启动命令：python manage.py runserver 127.0.0.1:8080
		这样就是代码监听8080端口，如果后面的都不写，只写到runserve，那么就是默认监听8000端口

​	创建完就可以访问了

#### 2、Django程序目录

​	manage.py   对应当前Django程序所有操作可以基于 python manage.py runserver
​	settings.py    Django配置文件
​	url.py			  路由系统：url->函数
​	wsgi.py			用于定义Django用socket、wsgiref、uwsgi

#### 3、第一个Django请求

在执行的时候我们访问的时候回默认回显示一个页面，那么我们如果给url是会输出另一个页面或者输出一个字符串的操作。
第一个请求是给定url参数是，页面显示一行字符串
**示例代码：**

```python
from django.contrib import admin
from django.urls import path
from django.shortcuts import HttpResponse

def login(request):
    """
    处理用户请求，并返回内容。request必须有的参数
    :param request:用户请求相关的索引信息(直接搭建的是字节类型的，而这里是对象)
    在这不需要传请求头什么的，他这里已经写好了
    # 这里能如果放回的是字符串就必须引用HttpResponse模块
    # 导入from django.shortcuts import HttpResponse，来将字符串进行处理一下
    # 这样只要字符串是什么用户就看到什么
    """
    return HttpResponse('login')


# 路由关系：格式path('url', 调用的字段，比如函数)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login)
]
```

这里的urlpatterns列表就是来规定url和函数之间的关系的，必须要注意格式
我们定义了当url为login是显示login函数，login函数返回的就是一行字符串
在这里传出的是字符串的话需要调用HttpResponse函数来处理字符串，调用之前需要先引入模块：from django.shortcuts import HttpResponse

#### 4、Django静态文件以及模板配置

静态文件表示图片、css样式这些文件
如果HTML模板中这些静态文件是导入的，必须先在配置文件中配置这两项东西：

```python
# 这个是使用是的前缀，比如找到com.css文件：/static/com.css
STATIC_URL = '/static/'
# 静态文件目录配置,将静态文件得目录地址配置好，sta就是目录名称
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,"sta"),
)
```

这里的STATIC_URL是已经配置好的了，STATICFILES_DIRS需要自己写的，这里写的是静态文件的存放位置，/static/就是就是使用的前缀，可以说是用来指定目录的。
例如：在HTML模板中导入css样式文件

```html
<link rel="stylesheet" href="/static/com.css" />
```

必须这样写才能将这些静态文件显示出来。

**Django以文件方式输出：**

在前面使用sockset方式搭建服务端是，传入文件的方式需要先定义头标签，而在Django这里不需要，只需引入模块:from django.shortcuts import render就可以了
例如：**return render(request, "demo01.html")**在这里的request是表示函数的参数，函数是什么参数，这里就写什么参数。

例子：

```python
from django.contrib import admin
from django.urls import path
from django.shortcuts import HttpResponse, render


def login(request):
    # 自动找到模板路径下的demo01.html文件，读取文件并返回给用户
    # 需要先在配置文件中找到TEMPLATES将里面的DIRS指定下文件的目录，
    # 这样就可以找到指定文件了
    # 这里的request是参数名称，什么参数名就写什么
    return render(request, "demo01.html")


# 路由关系：格式path('url', 调用的字段，比如函数)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login)
]
```

#### 5、Django创建程序步骤

1、创建project
2、配置：
		-模板路径：在settings.py中TEMPLATES里的DIRS里配置
		-静态文件路径：
			STATIC_URL = '/static/'
			STATICFILES_DIRS = (
  			  os.path.join(BASE_DIR,"sta"),
			)
3、额外配置
	找到MIDDLEWARE将里面的'django.middleware.csrf.CsrfViewMiddleware'注释掉

#### 6、Django用户登录示例

在Django中request.method可以来判断是GET请求还是POST请求
如果POST请求是可以使用request.POST来获取POST请求的表单
Django中的redirect是用来挑转页面的：redirect("http://www.baidu.com")
当如果在HTML中设置特殊字符时(特殊字符在没有被替换时是不会被显示出来的)，Django中的render函数中的第三参数可以来传入字典进行特殊字符替换的
比如在HTML中有特殊字符{{msg}}时，在某些条件下要将这个特殊字符替换掉可以使用：
render(request, "demo01.html", {"msg": "密码错误，登录失败"})  将特殊字符进行替换掉

在这里使用一个例子：

**HTML代码demo01.html：**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <link rel="stylesheet" href="/static/com.css" />
</head>
<body>
    <h1>用户登录</h1>
    <!--这里的action是表示当提交表单是会再次去路由里匹配一下/login/，如果
    匹配到了就再次调用指定函数，而且这一次他是POST请求访问的-->
    <form method="post" action="/login/">
        <input type="text" name="user">
        <input type="password" name="pwd">
        <input type="submit" value="登录">
        {{msg}}
<!--这里返回的是：
{'user': ['root'], 'pwd': ['123123']}
所有可以使用这个来匹配了
-->
    </form>

</body>
</html>
```

**python代码块：**

```python
from django.contrib import admin
from django.urls import path
from django.shortcuts import HttpResponse, render, redirect


def login(request):
    # request.method可以用来判断网页的请求方式GET和POST
    if request.method == "GET":
        return render(request, "demo01.html")
    else:
        # 当用户提交表单是就是POST请求
        u = request.POST.get('user')
        p = request.POST.get('pwd')
        print(request.POST)  #打印出post请求表单数据
        if u == "root" and p == "123123":
            # 登录成功，利用redirect来挑转网页
            return redirect("http://www.baidu.com")
        else:
            # 登录失败，并且将特殊字符串替换成密码错误登录失败
            return render(request, "demo01.html", {"msg": "密码错误，登录失败"})


# 路由关系：格式path('url', 调用的字段，比如函数)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', login)
]
```

request.GET可以获取get发的值：如
http:127.0.0.1:8000/login/?p=100       此时的request.GET={'p':['123']}

#### 7、Django模板语言特殊标记（1）

**特殊字符提取列表指定元素：**
如果特殊字符替换时指定的还是列表，在网页中也是显示列表：
如：render(request, "demo01.html", {"name": ['张三'，'李四']"})
如果想提取的是指定元素的话，特殊字符可以这么写:**{{name.0}}**或者**{{name.1}}**

**特殊字符提取字典元素:**
render(request, "demo01.html", {"name_dict":{'k1':1,'k2':2}})
{{name_dict.k1}}

**特殊字符的循环：**
格式：（这里的users是要循环的对象，与python循环语句差不多）
{% for item in users %}

{% endfor %}

**例如：与HTML一起写**
\<ul>
	{% for item in users %}
		\<li>{{item}}\</li>
	{% endfor %}
\</ul>

**例子：将列表中每个字典值都显示出来**

python传入的数据

```python
render(
	request, 
	"demo01.html", 
	{
		'user_list_dict':[
		{'id':1,'name':'alex1','email':'0000001'},
		{'id':2,'name':'alex2','email':'0000002'},
		{'id':3,'name':'alex3','email':'0000003'}
		]
	}
	)
```

html特殊字符写法：

```
<table>
	{% for row in user_list_dict %}
		<tr>
			<td>{{row.id}}</td>
			<td>{{row.name}}</td>
			<td>{{row.email}}</td>
		</tr>
	{% endfor %}
</table>
```

**这种方式也可以mysql中取数据，并且返回的是字典形式，用法是一样的**

#### 8.学员管理系统知识点总结

**1、http请求生命周期**
		请求头->提取URL->路由关系匹配->函数(函数+数据渲染)->返回给用户(响应体)
**2、后端用到的提取信息方法，和返回给用户页面的方法**
def index(request):
		request.POST.get()
		request.GET.get()
		request.POST.getlist()
		request.method()
		request.COOKIES.get('ticket')	获取cookie

	obj = redirect("/class/")
	        # 如果登录成功就给obj添加cookie
	        obj.set_cookie('ticket', 'asadscsxx')
	        return obj
		return render()  #跳转页面，这个多了一个页面渲染功能
		return HttpResponse()#返回字符串给网页
		return redirect()#跳转页面，但是没有渲染功能

​		模板的渲染是在后台的执行

**3、模板渲染和语句功能**
		for循环{{% for i in index%}}...{{%endfor%}}
		if语句{% if ..%}...{%endif%}
		索引用.获取
		取值{{}}
**4、后端页面返回方法**
**render：**后端执行好放回页面
render(request, "class.html", {"class_list": class_list})
这里的request是函数的参数，第二个是要放回的页面，第三个参数是要渲染放回的值，可以多个，前端代码可以使用这个值去渲染页面

**5、使用到的JavaScript用法**
**定义函数**：function showModal(){}
**指定id添加和去除标签class中的值：**
document.getElementById('shadow').classList.add('hide');
document.getElementById('shadow').classList.remove('hide');
**获取当前标签方法，这里必须在函数加上参数，并且使用该函数的标签参数要先this,例如这里的函数参数是ths**
var row = $(ths).parent().prevAll();  这个是获取当前标签的父标签的所有上方标签
**给指定id标签进行文本设置**：$('#editTitle').val(content); 
**获得指定id的文本值：**var nid = $('#editId').val();
**判断值是否在列表里**：例如v是数组，v.indexOf(value)



**6、AJAX提交数据方法**

先导入包，这里使用的是jQuery的AJAX方法：

```HTML
<script src="https://cdn.bootcss.com/jquery/3.4.1/jquery.js"></script>
```

AJAX是写在JavaScript方法里的：
格式：

```JavaScript
$.ajax({
                url:'/modal_edit_class/',  //往哪提交的url
                type:'POST',//提交方式
                data:{'nid':nid,'content':content},//提交过去的数据
                //当提交后服务器执行完毕后执行下面函数
                success:function(arg){
                    //arg传过来的是字符串
                    //在前端中字符串转对象的有这两种
                    //JSON.parse(字符串) => 对象
                    //JSON.stringify(对象) => 字符串
                    arg = JSON.parse(arg);
                    if(arg.status){
                        // location.href = '/class/';这个是转载页面
                        location.reload();//这个是刷新页面
                    }else{
                        alert(arg.message);
                    }
                }
            })
```

url是往哪提交的url；type是提交方式，data是提交的数据(这里的值需要在方法中先获得到)；success:function(arg)是当后台处理完数据后返回来的值，这里的arg就是后台返回的值，在进行处理；
在这个函数里如果放回的值是json数据的，可以使用JSON.parse(字符串)或JSON.stringify(对象)进行转换；location.reload();是刷新页面；如果不想在success中写转换json方法，可以在success前面写dataType:'JSON',相当于JSON.parse()

注意：如果传数据是是列表形式的，后台是接收不到的，一定要在AJAX中加上traditional:true
AJAX不支持传字典，只支持列表。如果是字典就序列化为列表，例如在AJAX加上JSON.stringify(字典)

**7、AJAX获得数据方法**

```JavaScript
$.ajax({
    url:'/get_all_class/',
    type:'GET',
    dataType:'JSON',
    success:function(arg){
        /*
        arg = [
            {id:1,title:xx}
            {id:2,title:xx}
        ]
        */
        /*
        arg进行循环，each就是循环，对arg进行循环
        后面的函数就是要循环的项，i是索引，row是arg里的一行一行的数据
        */
        $.each(arg,function(i,row){
        /*tag=<option><option/>就是创建一个option标签
        tag.innerHTML是给中间添值
        tar.setAttributes是添加属性
        最后再将他添加到select
        */
            var tag = document.createElement('option');
            tag.innerHTML = row.title;
            tag.setAttribute('value',row.id);
            $("#classIds").append(tag);
        })
      }
   })
```

这里是在url中获得数据，提取数据方式是GET，success:function(arg){}这里的arg就是获得到的数据，因为是json数据的所以要转换，$.each(arg,function(i,row){}是进行数据的遍历，arg是遍历的数据，i是每一行，row是每一行数据。

**例子：**

```js
function borrow(t){

	var arr = document.getElementsByTagName("button");
	for(var i = 0;i<arr.length;i++){
		arr[i].onclick = function(){
			var id = this.getAttribute("value");
			$.ajax({
			url:'/user_book/',
			type:'POST',
			data:{"id":id},
			dataType:"JSON",
//注意，传给后端只能是字典，如果指定里出现列表要添加traditional:true
//后端传过来的是json数据的，要添加dataType:"JSON"进行解析，前后端提取用key
			success:function(arg){
				if(arg.status){
					console.log(arg.message);
					location.reload();
				}else{
					console.log(arg.message);
					location.reload();
				}
		}
	})
		}
	}
	
}

```



#### 9、初始Bootstrap(Font Awesome如果图表不够用就是要这个)

先去百度下载Bootstrap，下载个用于环境变量的Bootstrap，在进行解压，解压完就拷贝到静态文件里
然后导入：\<link rel="stylesheet" href="/static/plugins/bootstrap-3.3.7-dist/css/bootstrap.css" />

然后去官方中查找要的样式，将class替换了就行了
Bootstraps是一个包含css和js的一个代码库
	-样式
	-响应式  @media关键字
			-导航条
			-栅格		


**响应式例子：**

```css
.pg_header{
	background-color:red;
	height:48px;
}
当页面宽度小于700像素是执行
@media(max-width:700px){
	.pg_header{
		background-color:red;
		height:48px;
	}
}
```

#### 10、Django模板引擎值母版

在页面中如果有一个网页框架是共用的，只是里面有一些数据是来自其他网页是，此时就可以使用Django模板引擎来设置。Django模板是存放所有页面共用的东西，子版继承模板，还可以自定义当前页面私有东西
比如：
在母版(共用网页)中某个位置上要要写上其他网页的内容就可以在那里写上：
**{% block xx %} {% endblock %}**这里的xx表示名称
一般传过来的有css样式和主要内容还有js内容，所有在母版中要在存放这三个地方上写上对应的block

在要继续母版的HTML中要这样写：
首先要继续**{% extends ‘继承的模板名称.html’ %}**
然后就是：**{% block xx %}..{% endblock %}**这里的xx要对应模板的block名称
css和主要内容还有js要写成三个block
比如：我这里要将页面内容继承过去ss.html中的{% block body %} {% endblock %}中：
{% extends ‘ss.html’ %}
{% block body %}
	\<h1>abada\</h1>
{% endblock %}

**补充：**

其实就是把一个框架模板写好，然后哪些地方是需要后续在里面加的就写上`{% block xxxx %} {% endblock %}`,这里的xxxx是定义的名称，这样其他模块想要基础你的格式就在自己的html顶部写上`{% extends 'xxxx.html' %}`，然后需要在模块中哪个位置写上内容就写上前面定义好的名称引用出来，然后在中间写上标签内容，例如：

```html
{% block data %}
<h2 style="text-align: center;">用户借书信息</h2>
{% endblock %}
```

#### 11、cookie

**(1)、初识cookie**
格式：

```python
set_cookie(self, key, value='', max_age=None, expires=None, path='/',
               domain=None, secure=False, httponly=False, samesite=None):
```

key是键，value是值，max_age是间隔秒，expires是具体时间，path是表示cookie要给那些url访问，当为/是就表示所有的url都可以读取到。domain是域名。httponly表示写的cookie只能用来http请求传输，通过js代码不能访问。secure是给https使用的

登录判断密码并且设置cookie

```python
def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        if user == "alex" and pwd == "123":
            obj = redirect("/class/")
            # 如果登录成功就给obj添加cookie,这里是键值对，第一个是key，第二个是值
            obj.set_cookie('ticket', 'asadscsxx')
            return obj
        else:
            return render(request, "login.html")
```

当登录成功跳转时，并且给class的请求头中设置cookie，这里不止是使用redirect返回，其他方法都可以
在class进行识别

```python
def class(request)
	# 去请求的cookie中找凭证
	# 如果没有凭证的话就跳转回去ticket
	tk = request.COOKIES.get('ticket')
	if not tk:
    	return redirect("/login/")
```

a.保存在浏览器端的“键值对”
b.服务端可以先用户浏览器端写cookie
c.客户端每次发请求时，会携带cookie

**(2)、Django设置cookie**

给cookie设置停留时间：**obj.set_cookie('ticket', 'asadscsxx',max_age=10)**
这里的max_age是无操作下浏览器停留的时间，以每秒计算

**(3)、扩展cookie签名**

```python
set_signed_cookie(self, key, value, salt='', **kwargs):
    value = signing.get_cookie_signer(salt=key + salt).sign(value)
```

这个就是给cookie进行加密，如果使用这个cookie加密的话
例如：
设置cookie：obj.set_signed_cookie('k','123',salt='jjjjj')
获取cookie：k = request.get_signed_cookie('k',salt='jjjjj')
其实可以把salt了解为加密密码

获取cookie是使用：request.get_signed_cookie(key,salt)

**如果登录写完了，可以用装饰器装饰你的代码，这样就不用每一个函数都加上cookie判断了**

总结：
def index(request):
	request.COOKIES
	request.get_signed_cookie('k1',salt='ff')

​	obj = HttpReponse(..)
​	obj = render(...)
​	obj = redirect(...)
​	obj.set_cookie(k1,v1,max_age)
​	obj.get_signed_cookie(k1,v1,max_age,salt='fff')

#### 12、Django主流web框架

在前面我们都是用原生的mysql语句进行查表，和直接参加了app目录把Django代码写里面，其实在Django里不是怎么写的。
Django:
	-路由
	-视图
	-模板
	-ORM（类-表：对象-行；也可以使用pymysql连接数据库）

今日内容：
	1、路由系统
	2、视图函数
	3、ORM操作

#### 13、Django程序目录

创建Django：**Django-admin startproject demo01**
创建存放程序目录(以前是自己创建的，这里使用命令创建，需要切换到项目目录里去)：**python manage.py startapp app01**
在project里可以多个app，每一app可以是网站中每一个功能的文件

创建完的目录介绍
1.migrations：数据库相关使用的
2.admin.py:Django自带后台管理相关配置
3.apps.py：相关的配置文件
4.models.py:写类，根据类创建数据库表
5.tests.py：单元测试
6.views.py：业务处理

如果也业务太多也可以在目录下创建一个views目录，在目录里重新创建业务处理py文件

#### 14、路由系统之动态路由

**url -> 函数**
第一种：
/login/ -> def login
第二种：可以在url后面写正则表达式
/add-user/(\d+)/ -> def add_user(request)

**（1）、动态路由设置**
动态路由就是在原url后面加上一串东西，后端可以去接收
例如：
**路由写法：**
首先需要导入re_path，在path后写就行，然后路由这样写：**re_path(r'edit/(\w+)/', views.edit)**这个就是匹配url后面的所有字符
后端接收写法：
首先需要在参数中在加入一个参数，然后这个参数就是正则匹配的字符了，例如：

```python
def edit(request, a1):
    print(a1)
    return HttpResponse("....")
```

页面写法例子:

```html
<ul>
    {% for i in user_list %}
        <li>{{i}} | <a href="/edit/{{i}}">编辑</a></li>
    {% endfor %}
</ul>
```

在url中也可以写多条正则表达式，如果有两个函数就得在添加两个参数
例如：**re_path(r'edit/(\w+)/(\w)', views.edit)**
**def edit(request, a1,a2):**

**url写法二：**

re_path(r'edit/(?P\<a1>\w+)/(?P\<a2>\w)', views.edit)

此时他就会去函数找到相对应的参数，并且把值赋给他。这里的名称要与函数参数名称对应
**第二种可以不用考虑顺序**

在写路由是后面还可以加上.html:path(r'edit.html', views.edit)
这种方法是叫做**伪静态**。

**终止符：r'edit.html$'**  因为路由是相当是一个正则表达式，所以加上$可以终止url，否则url后面怎么写都行，只要前面匹配到了，后面的乱写也能进行匹配

#### 14、路由系统之路由分发

路由分发就是当有多个app时，为了不让url重复，可以在另外的app目录下在创建一个url文件.
**include('app01.urls')格式，参数中写路径，是字符串的**
例如：
**总路由中写：path('app01/',include('app01.urls'))**(需导入from django.urls import include)
**子路由中写：path('index.html', views.index)**

在app01文件下载创建一个urls.py先
因为路由系统是正则匹配的，在总路由中匹配到了app01后，就会跳到app01文件下的urls中再进行匹配，匹配成功就返回index网页给他
例如url怎么写：http://127.0.0.1:8000/app01/index.html
这样他就会到总路由上进行匹配，匹配到了app01就执行include函数去了app01下进行匹配

#### 15、路由系统之别名方向生成URL(1)

**（1）、应用1**
就是在路由匹配后面加上name给url进行命名，并且后台能给浏览器反生成另外的url名称
**例子1**：url上没加正则表达式的情况下可以利用reverse获取url名称
**路由写法：path('index/', views.index,name='n1')**
**后端上可以使用reverse(name)进行获取url(需导入reverse)**
如：v = reverse('n1') ----> /index/

**例子2**：在url加上正则，没指定参数名情况下
**路由写法：re_path(r'index/{\d}/', views.index,name='n1')**
**后端写法：reverse(name,args=111)**
此时不论url在index/后面写任何数字，后端都会方向的吧url的index/后面改成111

**例子3**：在url加上正则，指定参数名情况下
**路由写法：re_path(r'index/{?P\<a1>\d}/', views.index,name='n1')**
**后端写法：reverse(name,kwargs={'a1':111})**
**因为是指定参数传参的，所以要使用kwargs**
此时不论url在index/后面写任何数字，后端都会方向的吧url的index/后面改成111

只要给url命名，在python代码中就可以反生成url
**（2）、应用2**

当我们给url命名是，在前端代码中要可以不用写url了，直接写名字就像
**格式：{% url “name” %}**
例如：\<form merhod="POST" action="{% url "n1" %}"
这样他也会根据名字去找到对应的url了

**（3）、应用3**
当如果url上有正则匹配的内容是
**路由：re_path(r'index/{\d}/', views.index,name='n1')**
**前端上：**
**{% for i in user_list %}**
	**\<a href="{% url "n1" i %}">编辑\<\a>**
**{% endfor %}**
只需这样写照样也能匹配到

**以后如果要加权限，用这个别名可以方便点**

#### 16、ORM操作概要

在原来http请求中是通过url访问得到视图的，视图是通过http模板和数据库将视图完善的
在Django中有个ORM，可以来代替mysql操作
**ORM操作表**：创建表、修改表、删除表
**操作数据行**：增删改查
ORM利用pymysql第三方工具连接数据库
默认：mysql连接方式是MySQLDB
所以我们用mysql连接数据库是要修改Django默认连接mysql方式

#### 修改Django连接mysql方式

进入到配置文件中找到DATABASES配置文件将他全部注释掉，否则就将他删掉，如果将下面的内容替换进去：

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # 默认表示连接数据库
        'NAME': 'ceshi',  # 数据库名字，需要自己创建数据库
        'USER': 'root',  # 用户名
        'PASSWORD': '1312014657',  # 密码
        'HOST': 'localhost',  # ip地址，不写默认本地localhost
        'PORT': '3306',  # 端口号
    }
```

注：数据库需要自己先创建，否则会报错
然后在工程目录下的\_\_init\_\_.py中添加：

```python
import pymysql
pymysql.install_as_MySQLdb()
```

如果有报错的话：AttributeError: 'str' object has no attribute 'decode'
就到C:\Program Files (x86)\Python35\Lib\site-packages\django\db\backends\mysql下将operation.py文件将里面的decode修改成encode就解决了。如果编辑不了该文件就在该文件右键安全里修改权限
如果是编码错误就是这个东西：就是将query = query.encode(errors='replace')进行修改

**步骤：1、创建数据库，2.配置数据库连接，3在init文件中写上内容**

#### 17、ORM操作之创建数据表（一）

上面步骤做完了就到自己创建的app目录里进行操作了：
**（1）、进入app里的models.py**
		创建一个类，并且类要继承models.Model
		例如：

```python
class UserInfo(models.Model):
    # BigA=bigint,Auto=自增，括号里表示是主键，
    nid = models.BigAutoField(primary_key=True)
    # Char是代表字符串类型，括号是长度
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=62)
```

这里面的变量就是表格的字段，这里的Big就是BigInt类型，Auto是自增，primary_key=True是设置为主键，Char是字符类型，max_length=62是最大长度。
在这里如果不创建nid的话他会自动帮我们创建一列，名称为id，类型为int，并且是自增和主键
**（2）、注册app**
		注册app就是在你的配置文件里找到INSTALLED_APPS，然后将你的app目录名添加进去
		例如：我这里的目录名字叫app01

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app01',
]
```

**（3）、创建数据表**
创建数据表需要执行命令：
**python manage.py makemigrations**
**python manage.py migrate**

执行完毕后他会创建很多表，其中app01_userinfo就是我们的表(app01是我们的目录名，userinfo是我们的类名)

**(4)、修改列名**
修改列名只需在原来的类中将字段名进行修改一下，并且重新只需一下命令就可以了
**(5)、增加列**
增加列也只需在类中添加一列，然后在执行命令，例如

```python
age = models.IntegerField(null=True)
```

如果这里不写允许为空的话，在原本数据里要是存在数据的话，会叫你输入数据。如果加了，新增的列数据会默认为null
如果不想为空，并且在执行命令是不停顿让输入数据的话可以这样写：默认为数据1

```python
age = models.IntegerField(default=1)
```

**(6)、创建FK关系**
如果用两个表，一个UserGroup和UserInfo，然后需要在第二个表中要FK第一个表，可以在第二个表的列中写下：

```
ag = models.ForeignKey("UserGroup",null=True,on_delete=models.CASCADE)
```

这里的第一个参数就是要创建FK的表，第二个如果是双方都数据是都可以不加
执行命令后UserInfo里会新加一列为ug_id，默认为“名称_id"

django 升级到2.0之后,表与表之间关联的时候,必须要写on_delete参数,否则会报异常:

```
n_delete=None, # 删除关联表中的数据时,当前表与其关联的field的行为
on_delete=models.CASCADE, # 删除关联数据,与之关联也删除
on_delete=models.DO_NOTHING, # 删除关联数据,什么也不做
on_delete=models.PROTECT, # 删除关联数据,引发错误ProtectedError
# models.ForeignKey('关联表', on_delete=models.SET_NULL, blank=True, null=True)
on_delete=models.SET_NULL, # 删除关联数据,与之关联的值设置为null（前提FK字段需要设置为可空,一对一同理）
# models.ForeignKey('关联表', on_delete=models.SET_DEFAULT, default='默认值')
on_delete=models.SET_DEFAULT, # 删除关联数据,与之关联的值设置为默认值（前提FK字段需要设置默认值,一对一同理）
on_delete=models.SET, # 删除关联数据,
```

**(注：创建出来的FK那个变量，是对应表格的对应以后数据，在获取数据是可以使用*变量名.列名*进行获取，如果关联的数据表也对其他表格做了关联，此时也可以进行获取“*变量.关联表的关联变量.关联表的关联表的列名”*进行获取)**

#### 18、ORM操作之操作数据表（二）

**增操作：**
首先需要在函数里面写，必须导入model进来：from app01 import models
**增使用：models.UserGroup.objects.create()然后括号里写要添加的数据**
**这里的models就是对于的文件，UserGroup就是数据表名，object是固定的**
**例如**：models.UserInfo.objects.create(username='root', password='pwd', ag_id=1)

**查数据操作：**
**查所有数据：group_data = models.UserGroup.objects.all()**
此时会返回一个QuerySet类型的数据(相当一个列表)，然后里面每一个参数就是每一行的数据
提取可以使用循环将每一行数据给提取出来，然后再使用‘.列名’将每一个数据提取出来
例如：

```python
for i in group_data:
    print(i.id)
    print(i.title)
```

在前端也可以将每一个数据给提取出来，例如：

```
{% for row in group_list %}
	{{row.id}}{{row.title}}
{% endfor %}
```

**条件查询**

```
group_data = models.UserGroup.objects.filter(id=1) # id=1
group_data = models.UserGroup.objects.filter(id__gt=1) # id>1
group_data = models.UserGroup.objects.filter(id__lt=1) # id<1
```

**使用filter，在括号里可以添加多个条件，多个就是and关系**
**在id后面加上两个下划线和gt表示大于，在id后面加上两个下划线和lt表示小于**

**删除数据**

删除数据只需在查询后面加上delete()就表示删除数据了，前面的就删除条件
例如：

```
group_data = models.UserGroup.objects.filter(id=1).delete()
```

**更新数据操作**

更新数据只需在查询后面加上update()就表示更新数据了，前面的就更新条件
然后括号里面可以添加要更新的数据
例如：

```
group_data = models.UserGroup.objects.filter(id=1).update(title="公关部")
```

#### 19、Django视图之CBV

**(1)路由以类方式传递：**
路由写法：**path(r'login.html', views.Login.as_view())**
这里的Login是定义的类，.as_view()是固定的写法
类的写法：

```python
from django.views import View
class Login(View):
    def get(self, request):
        return render(request, 'login.html')
    def post(self, request):
        print(request.POST.get('user'))
        return HttpResponse("post")
```

定义类需要继承View，所以需要导入这个模块
类里面的方法get和post表示页面的请求方式是什么，就执行那个函数
这里有很多种方法：

```
http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
```

其他最常用的是get、post、put、delete。需要那个就直接创建那个函数
**这里的写法跟以前的函数写法一样**

#### 20、Django视图ORM连表操作

**(1)、连表查数据(正向操作)**
有两个表

```python
class UserType(models.Model):
    title = models.CharField(max_length=32)


class UserInfo(models.Model):
    name = models.CharField(max_length=16)
    age = models.IntegerField()
    # FK操作
    ut = models.ForeignKey('UserType', on_delete=None)
```

给表插入数据

```python
def text(request):
    # 创建数据
    models.UserType.objects.create(title='普通用户')
    models.UserType.objects.create(title='VIP用户')
    models.UserType.objects.create(title='牛逼用户')

    models.UserInfo.objects.create(name='张三', age=13, ut_id=1)
    models.UserInfo.objects.create(name='李四', age=16, ut_id=2)
    models.UserInfo.objects.create(name='王五', age=43, ut_id=2)
    models.UserInfo.objects.create(name='小明', age=22, ut_id=3)
```

现在想要获取UserInfo表中的数据，并且将对应的用户类型给获取出来
可以使用

```python
result = models.UserInfo.objects.all()
for obj in result:
	print(obj.name,obj.age,obj.ut_id,obj.ut.title)
```

**在Django里想要连表将对应数据给提取出来，可以使用创建FK是的变量进行提取，例如ut.title,这样就是ut_id值表中对应的title数据**

**(2)、如果是*三个表*连接查数据的，也可以通过这个方法进行获取，例如**
在表格里多了一个表

```
class foo(models.Model):
    caption = models.CharField(max_length=32)
```

然后在UserType表中也对foo表进行FK操作

```
fo = models.ForeignKey('foo', on_delete=None)
```

此时查询可以这样：

```
result = models.UserInfo.objects.all()
for obj in result:
	print(obj.name,obj.age,obj.ut_id,obj.ut.title,obj.ut.fo.caption)
```

**以此类推**

**(3)、通过FK关系反向操作**

如果想通过被关联表查询数据时，并且将与我关联下的数据都查询出来可以使用一下例子：
如，这里的UserInfo表中有有对UserType进行FK连表ut = models.ForeignKey('UserType', on_delete=None)，想通过UserType查出第一条数据，并且将UserInfo下与我该数据有关联数数据查出来：

```python
obj = models.UserType.objects.all().firsr()
print('用户类型',obj.id,obj.title)
# 将UserInfo中与我查出来数据相关联的数据给提出来
for row in obj.userinfo_set.all():
	print(row.name,row.age)
```

可以使用**查出来的对象名.表名小写_set.all()**将关联的数据查出来
这里方向查询也可以使用filter进行筛选：
**如：obj.userinfo_set.filter(列名=key)**

**(4)、对查询出来的所有数据进行列的筛选**

只需在查出来的代码后面加上.values(列名，列名..)，这样就只会查询出指定的列数据。如**models.UserType.objects.all().values('id','name')**
但是他返回的每一函数据就不是对象了，但是整体是QuerySet类型，而里面每一行数据是字典类型了
**返回结果：QuerySet[{'id':'xx','name':'xx'},.....]**

使用values_list()进行列筛选是返回的是元组
**models.UserType.objects.all().values_list('id','name')**
返回结果：**QuerySet[(1,xx),(2,xx)]**

如果想使用values或者values_list跨表查找是不能使用.类名取值了，要使用双下划线加列名
如：**models.UserInfo.objects.all().values_list('id','name','ut__title')**

**跨表使用filter也可以这样使用：**
**正向：xxxx.filter('ut__title'=‘超级用户’).values('id','name','ut\_\_title')**
**方向：xxxx.filter('表名称__title'=‘超级用户’).values('id','name','表名称\_\_title')**

#### 21、Django视图之内置分页

**（1）、分批获取数据：**
分批获取数据可以在查询出来的数据使用中括号并且给定要获取的值数据进行分批获取，如：
models.UserInfo.objects.all()[0:10]
models.UserInfo.objects.all()[10:20]
**（2）、Django自带分页功能**

**Paginator**函数介绍：Paginator是将查询出来的数据进行分批次的
**Paginator(object_list, per_page)**
参数1是查询出来的数据，第二个参数是每一页要几条数据
如：

```python
from django.core.paginator import Paginator	# 导入模块
user_list = models.UserInfo.objects.all()	# 查询数据
paginator = Paginator(user_list, 10)	#将数据进行分页，即每一批为10条数据
```

**Paginator功能：**
**.per_page**:		每一页显示条目数量
 **.count**:			数据的总个数
 **.num_pages**:	总页数
 **.page_range**:	总页数索引范围：如(1,10),(1,200)
 **.page(page)**:			返回的是page对象，可以用来返回的指定的页数

**.page(page)介绍**

参数是要返回的页码，这里可以接收前端请求发来的页面将数据返回过去
**.page()功能：**
**has_next**:是否有下一页
**next_page_number**:下一页页码
 **has_previous**:是否有上一页
**previous_page_number:上一页页码**
**object_list**：分页之后的数据列表
**number**：当前页
**paginator**：paginator对象

例如：

```python
from django.core.paginator import Paginator, Page,PageNotAnInteger,EmptyPage
current_page = request.GET.get('page') #获取前端给定页码
try:
    post = paginator.page(int(current_page))  # 这是获取第一页数据，是page对象
except PageNotAnInteger as e:  # 这里是当输入的非数字是的异常
    post = paginator.page(1)
except EmptyPage as e:  # 这里是当输入的是负数是的处理异常
    post = paginator.page(1)
```

例子：

```python
# -*- coding=utf-8 -*-
from django.shortcuts import render, HttpResponse
from app01 import models
from django.views import View
from django.core.paginator import Paginator, Page,PageNotAnInteger,EmptyPage


def index(request):
    # 接收前端发来的数据
    current_page = request.GET.get('page')
    # Django自带分页操作
    user_list = models.UserInfo.objects.all()
    paginator = Paginator(user_list, 10)
    # paginator是将查出来的数据进行分批次，每一批为10条数据
    try:
        post = paginator.page(int(current_page))  # 这是获取第一页数据，是page对象
    except PageNotAnInteger as e:  # 这里是当输入的非数字是的异常
        post = paginator.page(1)
    except EmptyPage as e:  # 这里是当输入的是负数是的处理异常
        post = paginator.page(1)
	
    # 这里传过去的数据是page对象的，所以在前端要使用object_list将数据提取出来
    return render(request, 'index.html', {'post': post})
```

这里，因为用户输入是页面有可能输入不是数字或者小数内容，所以要进行判断
**前端接收数据**

```html
<body>
    <h1>用户列表</h1>
    <ul>
        接收数据
        {% for row in post.object_list %}
            <li>{{ row.name }}</li>
        {% endfor %}
    </ul>

    <div>
        实现上一页切换
        {% if post.has_previous %}
            <a href="/index?page={{post.previous_page_number}}">上一页</a>
        {% endif %}
        实现页码
        {% for num in post.paginator.page_range %}
            <a href="/index?page={{num}}">{{num}}</a>
        {% endfor %}
        实现下一页切换
        {% if post.has_next %}
            <a href="/index?page={{post.next_page_number}}">下一页</a>
        {% endif %}
    </div>
</body>
```

数据传过来是page是page对象，所以在这边要进行函数转换
**Django自带换也缺点：页码只能全部显示出来，当页码多的话就不行了，所以Django只能实现上一页和下一页的切换较好**

#### **22、自定义分页**

#### 自定义分页(一)

自定义分页就是接受用户给定页码，将页码进行加工，在将数据进行提取返回给用户
这里使用了：models.UserInfo.objects.all()[start:end]
例如：

```python
def custom(request):
    # 用户当前想要访问的页码
    current_page = request.GET.get('page')
    current_page = int(current_page)
    # 每页显示的个数
    per_page = 10

    # 当第一页时[0,10]
    # 2，[10:20]
    # 3，[20:30]
    start = (current_page-1)*per_page
    end = current_page*per_page
    # user_list = models.UserInfo.objects.all()[起始:结束]
    user_list = models.UserInfo.objects.all()[start:end]

    return render(request,'custom.html',{'user_list':user_list})
```

接收了用户给定页码，将页码进行加工，在提取数据将数据返回给用户

#### 23、定义通用的分页

```python
class PageInfo(object):
    def __init__(self, current_page, all_count, base_url, per_page, show_page=11):
        # 如果当前页面不是数字，那就将页面弄成1
        try:
            self.current_page = int(current_page)
        except:
            self.current_page = 1
        self.per_page = per_page

        # 这个是将参数1和参数2进行整除并且取余数
        # 返回结果是divmod(101,10)->(10,1)
        # 所以这里可以通过判断余数来确定总页码
        # 如果b不等于0，那么a就要多一页
        a, b = divmod(all_count, per_page)
        if b:
            a = a + 1

        self.all_pager = a  # 所有页码
        self.show_page = show_page  # 展示做的页码
        self.base_url = base_url  # 跳转的url
    # 编写开始和结束值，就是获取数据的范围
    def start(self):
        return (self.current_page - 1) * self.per_page

    def end(self):
        return self.current_page * self.per_page

    # 编写换页的函数
    def pager(self):
        # 因为当前页面在中间，所以要将展示页码数除2
        # 并且获取当前页面前后的页码数量
        num = int((self.show_page - 1) / 2) 
        start = self.current_page - num
        end = self.current_page + num + 1
        
        # 将所有页码代码存放在这里
        page_list = []

        # 注：前端一定要使用Bootstrap插件的换页的组件
        # 上一页，当当前页码为1时上一页href就是#，不会跳转
        if self.current_page <= 1:
            prev = "<li><a href ='#' aria-label='Previous'><span " \
                   "aria-hidden='true'>&laquo;</span></a></li> "
        else:
            prev = "<li><a href ='%s?page=%s' aria-label='Previous'><span aria-hidden='true'>&laquo;</span></a></li>" \
                   % (self.base_url, self.current_page - 1)
        page_list.append(prev)

        # 将页面显示
        for i in range(start, end):
            if i <= 0 or i > self.all_pager:
                pass
            else:
                # 判断如果i是当前页面就改变当前页页面样式
                if i == self.current_page:
                    temp = "<li><a style = 'background-color:#5cb85c;' href='%s?page=%s'>%s</a></li>" % (
                        self.base_url, i, i)
                else:
                    temp = "<li><a href='%s?page=%s'>%s</a></li>" % (self.base_url, i, i)
                page_list.append(temp)

        # 下一页
        if self.current_page >= self.all_pager:
            nex = "<li><a href ='#' aria-label='Next'><span aria-hidden='true'>&raquo;</span></a></li>"
        else:
            nex = "<li><a href ='%s?page=%s' aria-label='Next'><span aria-hidden='true'>&raquo;</span></a></li>" \
                  % (self.base_url, self.current_page + 1)
        page_list.append(nex)

        return ''.join(page_list)


def custom(request):
    # 获取总页码
    all_count = models.UserInfo.objects.all().count()
    # 创建PageInfo对象
    page_info = PageInfo(request.GET.get('page'), all_count, "/custom", 10)
    # user_list = models.UserInfo.objects.all()[起始:结束]
    user_list = models.UserInfo.objects.all()[page_info.start():page_info.end()]
    # 将page_info传到前端去，前端调用数据是不需要加括号，例如page_info.pager就行
    return render(request, 'custom.html', {'user_list': user_list, 'page_info': page_info})

```

这里是将分页功能封装成一个类，其中参数current_page, all_count, base_url, per_page, show_page=11的意思是：
**current_page**当前页码，通过前端获取传过来
**all_count**是所有数据的行数，可以通过models.UserInfo.objects.all().count()获取所有数据的函数
**base_url**是要跳转的url
**per_page**是指定一页要多少行数据
**show_page**是展示在下方最多要多上个页码的数字

**前端代码可以这么写：**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
    <link rel="stylesheet" href="/static/plugins/bootstrap-3.3.7-dist/css/bootstrap.css" />
</head>
<body>
    <h1>用户列表</h1>
    <ul>
        {% for row in user_list %}
            <li>{{ row.name }}</li>
        {% endfor %}
    </ul>

    <nav aria-label="Page navigation">
  <ul class="pagination">
    {{page_info.pager | safe}}  因为后端传入的代码这里会将他是做不安全的以字符串显示，所以这里要加上safe
  </ul>
</nav>

</body>
</html>
```

这里需要导入Bootstrap，使用组件换页
{{page_info.pager | safe}}  因为后端传入的代码这里会将他是做不安全的以字符串显示，所以这里要加上safe
**以后换页功能使用该代码就行**

#### 24、Django的ORM操作

**(1)、排序ordre_by()**
从小到大：models.UserInfo.objects.all().ordre_by('id')
从大到小：models.UserInfo.objects.all().ordre_by('-id')
如果id出现重复可以多给他一个排序条件：models.UserInfo.objects.all().ordre_by('id','name')

**(2)、分组annotate**
分组相当于GROUP BY
没加条件的分组：

```python
from django db.models import Count,Sum,Max,Min
v = models.UserInfo.objects.values('ut_id').annotate(xxx=Count('id'))
```

给分组加条件

```python
from django db.models import Count,Sum,Max,Min
v = models.UserInfo.objects.values('ut_id').annotate(xxx=Count('id')).filter(xxx__gt=2) 
```

这里的意思是查询ut_idl列的数据，然后进行id分组，这里的名称可以随便起，Count还有这几张功能Sum,Max,Min，后面的filter(xxx__gt=2) 是将分组的总是大于2的进筛选

**(3)、条件查询**

```python
models.UserInfo.objects.filter(id__gt=1) #大于
models.UserInfo.objects.filter(id__lt=1) #小于
models.UserInfo.objects.filter(id__lte=1)#小于等于
models.UserInfo.objects.filter(id__gte=1)#大于等于
models.UserInfo.objects.filter(id__in=[1,2,3])#in
models.UserInfo.objects.filter(id__range=[1,2])#范围
models.UserInfo.objects.filter(name__startswith='xxxx')# 还有一个endswith
models.UserInfo.objects.filter(name__contai='xxxx')#包含

# 不等于用exclude
models.UserInfo.objects.exclude(id=1)# id不等于1
```

可参考：https://www.cnblogs.com/wupeiqi/articles/6216618.html

**(4)、F操作**
F操作就是在原来数据中进行更新(如：自加)

需导入模块：from django db.models import F

**让age列每个值加1**

```python
models.UserInfo.objects.all().update(age=F("age")+1)
```

**(4)、Q操作**
需导入模块：from django db.models import F

**Q解决or条件：**

```python
models.UserInfo.objects.filter(Q(id=8) | Q(id=2))
```

加管道符是or，加&是and，当and不用这么麻烦

Q操作方式2

```python
q1 = Q()
q1.connector = 'OR'
q1.children.append(('id', 1))
q1.children.append(('id', 10))
q1.children.append(('id', 9))
#相当于(id=1 or id=10 or id=9)

q2 = Q()
q2.connector = 'OR'
q2.children.append(('c1', 1))
q2.children.append(('c1', 10))
q2.children.append(('c1', 9))
#相当于(c1=1 or c1=10 or c1=9)

q3 = Q()
q3.connector = 'AND'
q3.children.append(('id', 1))
q3.children.append(('id', 10))
q2.add(q3,'OR')


con = Q()
con.add(q1, 'AND')
con.add(q2, 'AND')
#这里在将全部添加到con里去，在作用与条件中

models.Tb1.objects.filter(con)
```

这个方式可以作用与页面筛选是用的，将页面上选的条件进行封装在一个字典上传给后端作为数据查询

**(5)、extra操作**
**操作一：额外查询另一个表数据**

```python
v = models.UserInfo.objects.all().extra(select{'n':'select count(1) from app01_usertype'})
for obj in v:
	print(obj.name,obj.id,obj.n)
# 这里是额外查询app01_usertype表中的数据量，n是查询出来的数据名称
```

**操作二：额外查询另一个表数据并且给定条件**

```python
v = models.UserInfo.objects.all().extra(select{'n':'select count(1) from app01_usertype where id>%s'},select_params=[1,])
for obj in v:
	print(obj.name,obj.id,obj.n)
# 这里是额外查询app01_usertype表中的数据量，n是查询出来的数据名称
```

**额外查询用SQL语句，可以查询多个**

**操作三：用extra来给定查询条件**

```python
models.UserInfo.objects.extra(where=["id=1","name='alex'"])
models.UserInfo.objects.extra(where=["id=1 or id=2","name='alex'"])
models.UserInfo.objects.extra(where=["id=1","name=%s"],params=["alex",])
```

这里的where是用列表的，每个元素之间是and，可以在元素中添加or操作，用原生SQL语句,如果有占位符的话使用params来传递,如果想**排序**可以在后面继续加**order_by={}**

```python
models.UserInfo.objects.extra(tables=['app_usertype'])
# 相当于：select # from app_UserInfo,app_usertype
models.UserInfo.objects.extra(tables=['app_usertype'],where=['app.usertype.id=app01.userinfo.id'])
```

第一种是多表查询

**注意：在Django这里的extra里写原生sql语句是，表要使用数据库里对应的表，不是Django里的类的表名**

**如：models.UserInfo.objects.filter(id__gt=1).extra(where=["app01\_userinfo.id<100"])**

#### 25、Django的ORM操作之补充

**所有操作代码**

```python
def all(self)
    # 获取所有的数据对象

def filter(self, *args, **kwargs)
    # 条件查询
    # 条件可以是：参数，字典，Q

def exclude(self, *args, **kwargs)
    # 条件查询
    # 条件可以是：参数，字典，Q

def select_related(self, *fields)
     性能相关：表之间进行join连表操作，一次性获取关联的数据。
     model.tb.objects.all().select_related()
     model.tb.objects.all().select_related('外键字段')
     model.tb.objects.all().select_related('外键字段__外键字段')

def prefetch_related(self, *lookups)
    性能相关：多表连表操作时速度会慢，使用其执行多次SQL查询在Python代码中实现连表操作。
            # 获取所有用户表
            # 获取用户类型表where id in (用户表中的查到的所有用户ID)
            models.UserInfo.objects.prefetch_related('外键字段')



            from django.db.models import Count, Case, When, IntegerField
            Article.objects.annotate(
                numviews=Count(Case(
                    When(readership__what_time__lt=treshold, then=1),
                    output_field=CharField(),
                ))
            )

            students = Student.objects.all().annotate(num_excused_absences=models.Sum(
                models.Case(
                    models.When(absence__type='Excused', then=1),
                default=0,
                output_field=models.IntegerField()
            )))

def annotate(self, *args, **kwargs)
    # 用于实现聚合group by查询

    from django.db.models import Count, Avg, Max, Min, Sum

    v = models.UserInfo.objects.values('u_id').annotate(uid=Count('u_id'))
    # SELECT u_id, COUNT(ui) AS `uid` FROM UserInfo GROUP BY u_id

    v = models.UserInfo.objects.values('u_id').annotate(uid=Count('u_id')).filter(uid__gt=1)
    # SELECT u_id, COUNT(ui_id) AS `uid` FROM UserInfo GROUP BY u_id having count(u_id) > 1

    v = models.UserInfo.objects.values('u_id').annotate(uid=Count('u_id',distinct=True)).filter(uid__gt=1)
    # SELECT u_id, COUNT( DISTINCT ui_id) AS `uid` FROM UserInfo GROUP BY u_id having count(u_id) > 1

def distinct(self, *field_names)
    # 用于distinct去重
    models.UserInfo.objects.values('nid').distinct()
    # select distinct nid from userinfo

    注：只有在PostgreSQL中才能使用distinct进行去重

def order_by(self, *field_names)
    # 用于排序
    models.UserInfo.objects.all().order_by('-id','age')

def extra(self, select=None, where=None, params=None, tables=None, order_by=None, select_params=None)
    # 构造额外的查询条件或者映射，如：子查询

    Entry.objects.extra(select={'new_id': "select col from sometable where othercol > %s"}, select_params=(1,))
    Entry.objects.extra(where=['headline=%s'], params=['Lennon'])
    Entry.objects.extra(where=["foo='a' OR bar = 'a'", "baz = 'a'"])
    Entry.objects.extra(select={'new_id': "select id from tb where id > %s"}, select_params=(1,), order_by=['-nid'])

 def reverse(self):
    # 倒序
    models.UserInfo.objects.all().order_by('-nid').reverse()
    # 注：如果存在order_by，reverse则是倒序，如果多个排序则一一倒序


 def defer(self, *fields):
    models.UserInfo.objects.defer('username','id')
    或
    models.UserInfo.objects.filter(...).defer('username','id')
    #映射中排除某列数据

 def only(self, *fields):
    #仅取某个表中的数据
     models.UserInfo.objects.only('username','id')
     或
     models.UserInfo.objects.filter(...).only('username','id')

 def using(self, alias):
     指定使用的数据库，参数为别名（setting中的设置）


##################################################
# PUBLIC METHODS THAT RETURN A QUERYSET SUBCLASS #
##################################################

def raw(self, raw_query, params=None, translations=None, using=None):
    # 执行原生SQL
    models.UserInfo.objects.raw('select * from userinfo')

    # 如果SQL是其他表时，必须将名字设置为当前UserInfo对象的主键列名
    models.UserInfo.objects.raw('select id as nid from 其他表')

    # 为原生SQL设置参数
    models.UserInfo.objects.raw('select id as nid from userinfo where nid>%s', params=[12,])

    # 将获取的到列名转换为指定列名
    name_map = {'first': 'first_name', 'last': 'last_name', 'bd': 'birth_date', 'pk': 'id'}
    Person.objects.raw('SELECT * FROM some_other_table', translations=name_map)

    # 指定数据库
    models.UserInfo.objects.raw('select * from userinfo', using="default")

    ################### 原生SQL ###################
    from django.db import connection, connections
    cursor = connection.cursor()  # cursor = connections['default'].cursor()
    cursor.execute("""SELECT * from auth_user where id = %s""", [1])
    row = cursor.fetchone() # fetchall()/fetchmany(..)


def values(self, *fields):
    # 获取每行数据为字典格式

def values_list(self, *fields, **kwargs):
    # 获取每行数据为元祖

def dates(self, field_name, kind, order='ASC'):
    # 根据时间进行某一部分进行去重查找并截取指定内容
    # kind只能是："year"（年）, "month"（年-月）, "day"（年-月-日）
    # order只能是："ASC"  "DESC" 排序
    # 并获取转换后的时间
        - year : 年-01-01
        - month: 年-月-01
        - day  : 年-月-日

    models.DatePlus.objects.dates('ctime','day','DESC')

def datetimes(self, field_name, kind, order='ASC', tzinfo=None):
    # 根据时间进行某一部分进行去重查找并截取指定内容，将时间转换为指定时区时间
    # kind只能是 "year", "month", "day", "hour", "minute", "second"
    # order只能是："ASC"  "DESC"
    # tzinfo时区对象
    models.DDD.objects.datetimes('ctime','hour',tzinfo=pytz.UTC)
    models.DDD.objects.datetimes('ctime','hour',tzinfo=pytz.timezone('Asia/Shanghai'))

    """
    pip3 install pytz
    import pytz
    pytz.all_timezones
    pytz.timezone(‘Asia/Shanghai’)
    """

def none(self):
    # 空QuerySet对象


####################################
# METHODS THAT DO DATABASE QUERIES #
####################################

def aggregate(self, *args, **kwargs):
   # 聚合函数，获取字典类型聚合结果
   from django.db.models import Count, Avg, Max, Min, Sum
   result = models.UserInfo.objects.aggregate(k=Count('u_id', distinct=True), n=Count('nid'))
   ===> {'k': 3, 'n': 4}

def count(self):
   # 获取个数

def get(self, *args, **kwargs):
   # 获取单个对象

def create(self, **kwargs):
   # 创建对象


def bulk_create(self, objs, batch_size=None):
    # 批量插入
    # batch_size表示一次插入的个数
    objs = [
        models.DDD(name='r11'),
        models.DDD(name='r22')
    ]
    models.DDD.objects.bulk_create(objs, 10)

def get_or_create(self, defaults=None, **kwargs):
    # 如果存在，则获取，否则，创建
    # defaults 指定创建时，其他字段的值
    obj, created = models.UserInfo.objects.get_or_create(username='root1', defaults={'email': '1111111','u_id': 2, 't_id': 2})

def update_or_create(self, defaults=None, **kwargs):
    # 如果存在，则更新，否则，创建
    # defaults 指定创建时或更新时的其他字段
    obj, created = models.UserInfo.objects.update_or_create(username='root1', defaults={'email': '1111111','u_id': 2, 't_id': 1})

def first(self):
   # 获取第一个

def last(self):
   # 获取最后一个

def in_bulk(self, id_list=None):
   # 根据主键ID进行查找
   id_list = [11,21,31]
   models.DDD.objects.in_bulk(id_list)

def delete(self):
   # 删除

def update(self, **kwargs):
    # 更新

def exists(self):
   # 是否有结果
```

去https://www.cnblogs.com/wupeiqi/articles/6216618.html学习

#### 26、Django的ORM补充(连表查询使用这个)

**select_related**

在原本的有FK关联的连表查询中：

```python
q = models.UserInfo.objects.all()
for row in q:
	print(row.name,row.ut.title)
```

这里在循环中连表查询有FK关联的ut列FK的表中的title列，每一次循环都回去连表查一次，所以这样是不行的，要使用select_related，如：

```python
# 查询主动做连表
q = models.UserInfo.objects.all().select_related('ut')
for row in q:
	print(row.name,row.ut.title)
```

在select_related中写入有FK的列，这样在第一次就会给我们进行连表，这样效率会高一点

**prefetch_related: 不做连表，做多次查询**

```python
q = models.UserInfo.objects.all().prefetch_related('ut')
for row in q:
	print(row.name,row.ut.title)
```

这里相当于：
select * from userinfo;
Django内部：ut_id=[2,4]
select * from usertype where id in [2,4]

**注：**如果数据较少，查询少的话使用**select_related**，查询多使用**prefetch_related**

#### 27、Django之多表操作（一）

现有三个表,一个男生表和女生表，还有一个两个表的关系表
**Boy**

|  id  | name |
| :--: | :--: |
|  1   | 小明 |
|  2   | 小李 |
|  3   | 小凯 |
|  4   | 小子 |

**Girl**

|  id  | nick |
| :--: | :--: |
|  1   | 小猫 |
|  2   | 小狗 |
|  3   | 小红 |
|  4   | 小丽 |

**Love**

| id   | b(FK-Boy.id) | g(FK-Girl.id) |
| ---- | ------------ | ------------- |
| 1    | 1            | 1             |
| 2    | 1            | 4             |
| 3    | 2            | 4             |
| 4    | 2            | 2             |

**(1)、找出与小明有关联的女生**
**第一种写法**，找出boy表的小明，然后通过boy对象找出Love与小明关联的数据，然后在通过love方向找出girl的名称

```python
obj = models.Boy.objects.filter(name='小明').first()
love_list = obj.love_set.all()#找出与obj相关联的所有数据
for row in love_list:
	print(row.g.nick)	#通过找出来的相关联数据g_id在反向的去找出girl对应的数据
```

第二种写法：直接查询Love表，然后通过fk关键列用列名__对应列名的形式去跨表查询数据

```python
love_list = models.Love.objects.filter(b__name='方少伟').values('g__nick')
for item in love_list:
	print(item['g__nick'])
```

这里在第一次就开始连表查询了，所有第一个没第二个号


**创建联合唯一索引：**

```pyrhon
class Love(models.Model):
	b = models.ForeigKey('Boy')
	g = models.ForeigKey('Girl')
	clsee Meta:
		unique_together = [
			('b','g')
		]
```

这样子写了就表示b和g两个只能一次出现两个都一样的

#### 28、Django之多表操作（二）

Django内部的自动创建关系表，跟上面例子一样，上面的是自己创建的关系表，在Django中有自带的创建。
可以在有关联的两张表里随意一个表写上**xx=models.ManyToManyField(相关联的表名)**，此时就会创建一个app\_表名\_xx
如：

```python
class Boy(models.Model):
	name = models.CharField(max_length=32)
	m = models.ManyToManyField('Girl')  # 这个放在哪个表的里面都可以
class Girl(models.Model):
	nick = models.CharField(max_length=32)
	# m = models.ManyToManyField('Girl')
```

这样就会创建出一个关联表,app_boy_m表(如果是放在Girl里面就是app_girl_m)，里面有**id,Boy_id,Girl_id**
**在Django里自动帮我们生成的关联表，因为没有表类名，无法对该表进行操作，所以只能间接的操作**

例如：

```python
obj = models.Boy.objects.filter(name='小明').first()
# 这里因为在Boy里面写的关系表，所以可以通过这样来对关系表添加数据
obj.m.add(2)	#添加一条数据，给Girl_id列添加2，这里的obj是上面的Boy对象，所以Boy_id是小明的id
obj.m.add(3,4)	#添加两行数据
obj.m.add(*[1,])#用列表添加一条数据

obj.m.remove(2)#删除
obj.m.remove(3,4)
obj.m.remove(*[1,])

q =obj.m.all() # 这个是获取Girl表中与小明对应的所有数据
```

所以想找到与Boy中小明所对应的Girl数据：

```python
# 这个是先获得Boy表的指定数据，在通过创建关系表变量名进行获取与查询出来数据相关联的Girl数据
obj = models.Boy.objects.filter(name='小明').first()
girl_list = obj.m.all()# 这个就是Girl对象，并且这里还可以做筛选filter

obj.m.clear()#将所有相关的数据删除
```

通过查询Girl也可以获取Boy表数据，用反向：

```python
obj = models.Girl.objects.filter(nick='小鱼').firts()
print(obj.id,obj.nick)
v = obj.boy_set.all()
print(v.id,v.name)
```

#### 29、CSRF(form表单)

**(1)、CSRF的全部应用(在form表单加验证)**

CSRF可以防止攻击，就是防止请求伪造，在网页提交表单的时候启动CSRF的话，后端会随机生成一段字符串给用户，当用户提交表单的时候，如果没有这个字符串就提交失败。所以他可以防止那些伪造请求登录的人。
在Django里启动Django的CSRF的话要到配置文件将MIDDLEWARE里第四条注释取消，然后以后在做些from表单是要写上{% csrf_token %}，表单才能提交成功。
如：

```html
<body>
    <form method="post" action="/csrf1.html">
        {% csrf_token %}
        <input type="text" name="user"/>
        <input type="submit" value="提交"/>
    </form>
</body>
```

这种方法是整个网站都有这个验证的，所以每个表单提交都要加上这个

**(2)、局部应用**

需要将配置文件的MIDDLEWARE里第四条注释，然后在提交表达所对应的后端函数上加上装饰器，以后就只有这个地方会做验证，如：

```python
from django.views.decorators.csrf import csrf_exempt,csrf_protect
@csrf_protect
def csrf1(request):
    if request.method == "GET":
        return render(request, 'csrf1.html')
    else:
        return HttpResponse("ok")
```

后端对应的位置还是要加上{% csrf_token %}

#### 30、CSRF(AJAX)

**(1)、第一种方法**

使用AJAX请求提交时，有CSRF时要在AJAX提交数据的时候也要将随机字符串进行提交
例如：
后端写法：

```python
from django.views.decorators.csrf import csrf_exempt,csrf_protect
@csrf_protect
def csrf1(request):
    if request.method == "GET":
        return render(request, 'csrf1.html')
    else:
        return HttpResponse("ok")
```

前端写法

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    <form method="post" action="/csrf1.html">
        {% csrf_token %}
        <input id="name" type="text" name="user"/>
        <input type="submit" value="提交"/>
        <a onclick="sub{}"></a>
    </form>
</body>
    <script src="https://cdn.bootcss.com/jquery/3.4.1/jquery.js"></script>
    <script>
        function sub(){
             var csrf = $('input[name="csrfmiddlewaretoken"]').val()
             var user = $('$name').val()
             $.ajax({
                url:'/csrf1.html',
                type:"POST",
                data:{'user':user,"csrfmiddlewaretoken":csrf},
                success:function(args){
                    console.log(arg):
                }
             })
        }
    </script>
</html>
```

在这里获取CSRF的随机值要通过这里给我吗定的name是什么，然后我们根据这个name去获取，具体看name值是什么要到网页上看。传过去的key也要是name值，因为后端获取是也是用name去获取的

#### 31、ORM操作补充

更多字段的类型在https://www.cnblogs.com/wupeiqi/articles/5246483.html
邮箱类型等的，在Django里输入什么时都会输入成功，在admin里输入就有限制
这些是针对于Django中admin的，通过admin操作数据库是有限制

**枚举：**

```python
color_list = (
	(1,'黑色'),
	(2,'白色'),
	(3,'蓝色')
)
color = models.IntegerFild(choices=color_list)
```

这以后执行要写入1，2，3就代表颜色了。在admin中修改时改列有下拉框选择
应用场景，选项固定。如果选项不确定，要动态变化的话就用FK来实现

**在不考虑DjangoAdmin情况下记住以下字段和参数就行了**
字段：

```python
class UserInfo(models.Model):
	username = models.CharField(max_length=32) #字符串
	# 数值
	username = models.IntegerField()
	username = models.DecimalField()
	#时间
	username = models.DateTimeField()
	username = models.DateField()
	#抬举
	color_list=(
		(1,'黑色'),
		(2,'白色'),
		(3,'蓝色')
	)
	color = models.IntegerFild(choices=color_list)
```

参数：

```python
null = True
default='xx' #默认值
db_index=True #索引
unique = True #唯一索引
primary_key = True #索引
max_length = 32 

#多列索引
#Mate这些名字是固定的
#在表函数中写上这个，可以创建多列索引
class Mate:
	unique_together = (
		('email','ctime'),
	)
	index_together = (
		('email','ctime'),
	)
```

#### 32、模板

**（1）、母版**
一个子版只能继承一个模板（在上面有笔记了）
**（2）、函数**

```
return render(request,'text.html',{"user":{'k1':'v1','k2':'v2'}})
```

```html
#提取key
{% for item in user.key %}
	{{item}}
{% endfor %}

#提取值
{% for item in user.values %}
	{{item}}
{% endfor %}

{% for k,v in user.items %}
	{{k}}-{{v}}
{% endfor %}
```

再给模板引擎中传一个函数名的是后只要给名字就行，不用加括号，不能加参数

**将传入来的值变成大写**
在Django里面有自带很多函数，函数使用如下面，upper就是函数，但是也可以自己定义函数

```
{{name|upper}}  #这样会将值变大写
```

**(3)、自定义simple_filter**

自定义simple_filter就是自定义函数，这些函数在模板引擎中可以调用
定义步骤：
a.在app中创建templatetags模块(名字固定的)
b.创建任意文件.py  ,如xx.py
c.在文件中写代码，需要先导入模块
如：

```python
from django import template
register = template.Library() #固定的
@register.filter
def my_upper(value):	#自定义函数
    return value.upper()
```

d.在前端接收前要加上{% load xx %}这个xx是你的文件名
如：

```html
{% load xx %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    {{name|my_upper}}
</body>
</html>
```

e.然后在配置文件中需要将app在INSTALLED_APPS中注册

**(4)、自定义simple_filter(最多定义两个参数)**

在两个参数情况下的使用方法

```python
from django import template
register = template.Library() #固定的
@register.filter
def my_upper(value,args):	#自定义函数
    return value+args
```

模板写法

```html
{% load xx %}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    {{name|my_upper:"666"}}
</body>
</html>
```

第二个参数是在函数名后加冒号在加字符串，但是记得不能有空格

**(5)、自定义simple_tag**

simple_tag与上面的用法一样，但是导入的装饰器不一样，模板引擎也不一样
如：

```
@register.simple_tag()
def lower(value):
    return value
```

模板使用

```
{% lower "AAA" %}
```

**(5)、自定义simple_tag带多个参数时**
simple_tag可以多个参数，没有限量，而simple_filter最多两个参数如：

```
@register.simple_tag()
def lower(value,a1,a2,a3):
    return value+a1+a2+a3
```

模板使用

```
{% lower "AAA" "x" "d" "V" %}
```

**simple_tag与filter的区别：在模块引擎中simple_filter可以作为判断语句放在if后面，而simple_tag不行**

**(6)、include**

include其实就是导入的意思，在HTML中如果有一个小组件，这个组件很多地方都要用到，为了节省代码空间，可以在另外一个HTML文件中将改组件写好放在那里，以后需要他的地方就调用就是，例如：
**在phb.html文件中写上这么一个东东**：(不需要写头什么的，只需将具体东西写上就可)

```HTML
<div>
    <h1>好看的组件</h1>
    <p>kkk</p>
    <p>dsscd</p>
</div>
```

**在另外一个文件中调用**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Title</title>
</head>
<body>
    {% include 'pub.html' %}

    {% include 'pub.html' %}
</body>
</html>
```

使用{% include 组件名 %}就可以将组件进行调用了

如果后端传入渲染的值的话，在组件里写上对应的名字，也可以接受到数据
如：在后将{'name':'aaaaaa'}传入text.html中去，然后text文件中调用了pub.html文件，在pub.html文件中这么写也可以接收数据：

```html
<div>
    <h1>好看的组件</h1>
    <p>kkk</p>
    <p>{{name}}</p>
    <p>dsscd</p>
</div>
```

**他的实现是将组件内容的代码都替换掉include部分，不管后端传入什么数据，这里只有对应上了都能接收**

#### 33、Session

https://www.cnblogs.com/wupeiqi/articles/5246483.html

**Cookie是：保存在客户端浏览器上的键值对**
**Session是：保存在服务器端的数据(本质是键值对)。应用需依赖cookie。作用：保持会话(web网站)**
Session的好处:不会将敏感信息个客户端
例如：
	当用户来访问我们网站后，验证过后会产生cookie，而cookie是我们定义的，我们不想将敏感信息给客户端，所以我们在服务器端可以随机给cookie一段字符串,如给个sfdvscdscd，这是我们可以将这个随机字符串做个键值对的保存在服务端：如
{"sfdvscdscd":{"id":1,"name":"吴彦祖"}}，这样以后我们就可以保证访问安全，用户不会随意修改。而这些就是Session，保存在服务端的。

例如：
在前端中用form的登录表单，后端接收后给定义session，并且用一个网页进行验证是否登录成
设置session函数

```python
def login(request):
    if request.method == "GET":
        return render(request, "login.html")
    else:
        u = request.POST.get("user")
        p = request.POST.get('pwd')
        if u == "root" and p == "123":
            # Session设置
            # 1、生成随机字符串
            # 2、通过cookie发送给客户端
            # 3、服务器保存
            # 下面执行完session的保存结果:
			#{
            #	随机字符串:{'username':'root','pwd':'123'}
            #}
            request.session['username'] = 'root'
            request.session['pwd'] = '123'
            return redirect("/index/")
        else:
            return render(request,'login.html',{'msg':"用户名错误"})
```

登录成功后跳转的页面，在里面做了验证session的措施

```python
def index(request):
    # 对Session进行验证方法
    # 1、获取客户端cookie中的随机字符串
    # 2、从session中查找有没有随机字符串
    # 3.查session对应的key的value中是否有username
	
    # 因为cookie是保存在浏览器的，所以这里可以直接通过key获取value了
    v = request.session.get('username')
    if v:
        return HttpResponse("登录成功：%s"%v)
    else:
        return redirect('/login/')
```

**设置session并且向cookie传随机字符串：**
在设置session时和给cookie一段随机字符串这些都不用我们做，Django会自动帮我们自己生成。我们只需要对session里面的value中字典里的键值对进行设置就行
如：request.session['username'] = 'root'。这里可以设置多个
设置完这些数据保存在数据库中django_session表中，其中session_Key就是随机字符串，session_data是Django对value进行加密的值。

**通过key获取session中的value**
当登录成功就会Django就会自动获取cookie，这里使用request.session.get('username')就能自动获取到对应的值了，可以通过值去进行匹配。在数据库中Django给我们保存的数据是加密的，在这里获取我们不需要去界面，这些Django会自动帮我们去完成

#### 34、Session的基本使用

```python
b. 使用
 
    def index(request):
        # 获取、设置、删除Session中数据
        request.session['k1']
        request.session.get('k1',None)
        request.session['k1'] = 123
        request.session.setdefault('k1',123) # 存在则不设置
        del request.session['k1']
 
        # 所有 键、值、键值对
        request.session.keys()
        request.session.values()
        request.session.items()
        request.session.iterkeys()
        request.session.itervalues()
        request.session.iteritems()
 
 
        # 用户session的随机字符串
        request.session.session_key
 
        # 将所有Session失效日期小于当前日期的数据删除
        request.session.clear_expired()
 
        # 检查 用户session的随机字符串 在数据库中是否
        request.session.exists("session_key")
 
        # 删除当前用户的所有Session数据
        request.session.delete("session_key")
 
        request.session.set_expiry(value)
            * 如果value是个整数，session会在些秒数后失效。
            * 如果value是个datatime或timedelta，session就会在这个时间后失效。
            * 如果value是0,用户关闭浏览器session就会失效。
            * 如果value是None,session会依赖全局session失效策略。
```

默认cookie保存时间是两周，但是数据库里不会删除

**缓存session：**

```python
a. 配置 settings.py
 
    SESSION_ENGINE = 'django.contrib.sessions.backends.cache'  # 引擎
    SESSION_CACHE_ALIAS = 'default'# 使用的缓存别名（默认内存缓存，也可以是memcache），此处别名依赖缓存的设置
 
 
    SESSION_COOKIE_NAME ＝ "sessionid" # Session的cookie保存在浏览器上时的key，即：sessionid＝随机字符串
    SESSION_COOKIE_PATH ＝ "/"    # Session的cookie保存的路径
    SESSION_COOKIE_DOMAIN = None  # Session的cookie保存的域名
    SESSION_COOKIE_SECURE = False # 是否Https传输cookie
    SESSION_COOKIE_HTTPONLY = True # 是否Session的cookie只支持http传输
    SESSION_COOKIE_AGE = 1209600  # Session的cookie失效日期（2周）
    SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # 是否关闭浏览器使得Session过期
    SESSION_SAVE_EVERY_REQUEST = False # 是否每次请求都保存Session，默认修改之后才保存
 
```

#### 35、男士女士关系表(一)

**创建数据表**

```python
from django.db import models
class Boy(models.Model):
    nickname = models.CharField(max_length=32)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
class Girl(models.Model):
    nickname = models.CharField(max_length=32)
    username = models.CharField(max_length=32)
    password = models.CharField(max_length=64)
class B2G(models.Model):
    b = models.ForeignKey(to='Boy', to_field='id',on_delete=None)
    g = models.ForeignKey(to='Girl', to_field='id',on_delete=None)
```

后端函数，因为有多个功能，所以在app01中创建了views文件，将这些内容放里面
**account.py**

```python
from django.shortcuts import render, HttpResponse, redirect
from app01 import models
# 登录
def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        # 获取前端提交内容
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        gender = request.POST.get('gender')
        rmb = request.POST.get('rmb')
        # 做个判断，判断是男是女，并且将自己的信息查询出来
        if gender == "1":
            obj = models.Boy.objects.filter(username=user, password=pwd).first()
        else:
            obj = models.Girl.objects.filter(username=user, password=pwd).first()
        if not obj:
            # 如果填写的内容数据库里找不到，就登录失败
            return render(request, 'login.html', {'msg': '密码错误'})
        else:
            # 登录成功
            # request.session['user_id'] = obj.id
            # request.session['gender'] = gender
            # request.session['username'] = user
            # 设置session，上面和下面都可以
            request.session['user_info'] = {'user_id': obj.id, 'gender': gender,
                                            'username': user, 'nickname': obj.nickname}

            return redirect('/index.html')
# 注销
def logout(request):
    # 将数据库的随机字符串删除
    request.session.delete(request.session.session_key)
    # 这个是删除cookie，就是cookie删除了
    request.session.clear()
    return redirect('/login.html')
```

**love.py**

```python
from django.shortcuts import render, HttpResponse, redirect
from app01 import models

# 将内容展示给前端
def index(request):
    if not request.session.get('user_info'):
        return redirect('/login.html')
    else:
        # current_nike_name = request.session.get('user_info').get('nickname')
        # 男士：查看女生列表
        # 女生：查看男士列表
        gender = request.session.get('user_info').get('gender')
        if gender == '1':
            user_list = models.Girl.objects.all()
        else:
            user_list = models.Boy.objects.all()
        return render(request, 'index.html', {'user_list': user_list})

def others(request):
    # 获取与当前用户相关的异性

    current_user_id = request.session.get('user_info').get('user_id')
    gender = request.session.get('user_info').get('gender')
    if gender == '1':
        user_list = models.B2G.objects.filter(g_id=current_user_id).values('g__nickname')
    else:
        user_list = models.B2G.objects.filter(b_id=current_user_id).values('b__nickname')
    return render(request, 'others.html', {'user_list': user_list})
```

**others.html**

```html
<body>
    <h1>有关系的异性列表</h1>
    <ul>
    {% for row in user_info %}
        {% if row.g__nickname %}
            <li>{{row.g__nickname}}</li>
        {% else %}
            <li>{{row.b__nickname}}</li>
        {% endif %}
    {% endfor %}
    </ul>
</body>
```

**index.html**

```html
<body>
    <h1>当前用户：{{request.session.user_info.nickname}}</h1>
    <a href="/logout.html">注销</a>
    <h3>异性列表</h3>
    <a href="/others.html"> 查看和我有关系的列表</a>
    <ul>
        {% for row in user_list %}
            <li>{{row.nickname}}</li>
        {% endfor %}
    </ul>
</body>
```

**login.html**

```html
<body>
    <form method="post" action="/login.html">
        {% csrf_token %}
        <p><input type="text" name="username"/></p>
        <p><input type="text" name="password"/></p>
        <p>
            性别:
                男<input type="radio" name="gender" value="1"/>
                女<input type="radio" name="gender" value="2"/>
        </p>
        <p>
            <input type="checkbox" name="rmb" value="11"/>一个月免登陆
        </p>
        <input type="submit" value="提交"/>{{msg}}
    </form>
</body>
```

我们使用render将页面放回的时候，request也跟着传过去了，所以在前端使用{{request.session.user_info.nickname}}也能提取到想要的内容，但是这里使用.，没有括号。
在后端写法request.session.get('user_info').get('nickname')

#### 36、男士女士关系表(二)

在上面数据库创建是将男女放在两个表里，这里放在同一个表里

```python
class UserInfo(models.Model):
	nickname = models.CharField(max_length=32)
	username = models.CharField(max_length=32)
	password = models.CharField(max_length=32)
	gender_choices=(
		(1,'男'),
		(2,'女')，
	)
	gender = models.IntegerField(choices=gender_choices)

# 方向查找
# related_query_name
# obj对象男.b_set.all()
# obj对象女.b_set.all()
# related_name
# obj对象男.b.all()
# obj对象女.b.all()
clss U2U(models.Model):
	b = models.ForeignKey('UserInfo',related_name='boys')
	g = models.ForeignKey('UserInfo',related_name='girls')
```

用related_query_name或者related_name是，方向查找就不是使用表名_set查找了，使用上面规则查找了

如果不加这个的话，使用obj.u2u_set.all()查找是会将g对应的数据和b对应的数据查找出来
因为是将男女都写在一个表了，为了想查找上面就展示上面就得给每一列关系列命名，他就能将对应的数据给你
**例如：**

```python
class UserType(models.Model):
	title = models.CharField(max_length=32)
class User(models.Model):
	username = models.CharField(max_length=32)
	ut =  models.ForeignKey('UserType',related_name='xxx')
```

**这样子以后方向可以使用：将user_set.all()换成xxx.all()**

**在ForeignKey列可以传对象**

```
boy = models.UserInfo.objects.filter(gender=1,id=2).first()
girl = models.UserInfo.objects.filter(gender=2,id=6).first()
models.U2U.objects.create(b=boy,g=girl)
```

这里可以b=boy.id,也可以直接将对象给赋值进行，如果在这里已经知道id了，可以直接将id赋值就行。但是如果是用对象传的话，使用的列名要是创建是的变量名
models.U2U.objects.create(b_id=2,g_id=1)

**反向查询：**

```python
xz = models.UserInfo.objects.filter(id=1).first()
# 查出和xz相关的所有信息
result = xz.girl.all()
for u in result:
# 在循环，获取与表中与g_id对应的名字
	print(u.g.nickname)
```

#### 37、子关联

```python
class UserInfo(models.Model):
	nickname = models.CharField(max_length=32)
	username = models.CharField(max_length=32)
	password = models.CharField(max_length=32)
	gender_choices=(
		(1,'男'),
		(2,'女')，
	)
	gender = models.IntegerField(choices=gender_choices)
	m = models.ManyToManyFieId('UserInfo')
```

上面创建表完会自动创建多一个表app01_userinfo_m，其中有id、from_userinfo_id、to_userinfo_id
我们可以把from_userinfo_id认为男生id，to_userinfo_id为女生id

```python
obj = models.UserInfo.objects.filter(id=1).fires()
obj.m  =>  select xx from xx where from_userinfo_id=1
obj.userinfo_set  =>  select xx from xx where to_userinfo_id=1

如：
#男生对象
obj = models.UserInfo.objects.filter(id=1).fires()
# 根据男生对象id=1查找所有关联的女生
obj.m.all()

#女生对象
obj = models.UserInfo.objects.filter(id=3).fires()
# 根据女生对象id=3查找所有关联的男生
obj.userinfo_set.all()
```

#### 38、FK自关联

表格可以FK自己
如：

```python
class Comment(models.Model):
	new_id = models.IntegerField()
	content = models.CharField(max_length=32)
	user = models.CharField(max_length=32)
	reply = models.ForeignKey('Comment',null=True,blank=True,related_name='xx')
    
评论表格案例
id	新闻id	content		用户user		reply_id
1		1		真好			root		null
2		1		别比比			root		null
3		1		就比比			xm			null
4		2		写的真好		root		null
5		1		拉倒吧			kl			2
6		1		嗯嗯			k2			2


新闻1
	真好
    	拉倒吧
        嗯嗯
    别比比
    就比比
    
新闻2
	写的真好
```

#### 39、中间件

在Django里面中有自带的中间件，也可以直接自定义中间件，在配置文件中MIDDLEWARE就是中间件

```python
MIDDLEWARE = [	#中间件
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# 视图函数
ROOT_URLCONF = 'demo04.urls'
```

在这里面执行是这样执行的，当用户访问服务器是会先顺序执行中间件里的process_request，执行完再执行视图函数，在返回从后面开始顺序的执行中间件的process_response
![img](file:///C:\Users\User\AppData\Roaming\Tencent\Users\1312014657\QQ\WinTemp\RichOle\K$~UN}SAI8]GBG_9BRGZ7`W.png)

自定义可以创建一个py文件，并且根据格式在里面创建一个类和两个方法
如：

```python
class mm(MiddlewareMixin):
    def process_request(self, request):
        print("request中间件")


    def process_response(self, request, response):
        print("response中间件")
        return response
```

然后在配置文件中中间件里加入'm1.mm'，m1是py文件名
这里的response要加return response
request不要加，如果加return的话，中间件执行到这来就结束了，直接执行response返回

#### 40、中间件(一)

**process_view(self, request,callback,callback_atgs,callback_kwargs)函数**

在中间件中有process_view这个函数，他在执行中间件是也会执行这个
他的执行是这样的：先执行request函数的，执行完毕就执行view函数的，如果view函数里有某一个有返回值的话，他会直接跳过后面的所有中间件的view函数，跳到视图函数中去，过后在返回到最后一个response函数处继续执行完返回给用户

**process_exception(self, request, exception)函数**

这个函数是处理异常的，当视图模块中有异常的话，就会执行这个函数
他的执行顺序是这样的：
**执行request->执行view->调用视图模块（如果视图模块出现异常）->从后到头执行exception函数->在返回来执行response函数**

如果在执行exception的时候，有某个exception把异常给处理了，有返回值了，后面的exception就不会在执行了，就会返回到response函数执行了

**process_template_view(self, request)函数**

这个函数是在视图函数的返回值中如果用render方法才会被调用


#### 41、初识Form验证

定义规则：

```python
from django.forms import Form,fields
class LoginForm(Form):
	username = fields.CharField(max_length=18,
	min_length=6,required=True,error_messages={
	'required':'用户名不能为空',
	'min_length':'太短了',
	'max_length':'太长了'
	})
	password = fields.CharField(min_length=16,required=True)
```

这里是定义匹配规则类，这里的变量命名要和传进来的数据名称一样，fields里面有很多的正则验证规则
这里的error_messages是设置错误信息

```
def login(request):
	if request.method == 'GET':
		return render(request,'login.html')
	else:
		# 调用匹配函数，将表单数据传进去，这里不需要拆开，Django内部会自动帮我们解析
		obj = LoginForm(request.POST)
		if obj.is_valid():	#这个是返回布尔值的
			#用户输入格式正确
			print(obj.cleaned_data) #正确信息字典类型
			return redirect('http://www.baidu.com')
		else:
		# 用户输入格式错误
		return render(request,'login.html',{'obj':obj})
```

obj.is_valid()是返回布尔类型，obj.cleaned_data是返回错误信息，字典类型的。
这里将obj传入前端，前端可以根据内容提取错误信息
**如：obj.errors.username.0**这样就是提取username错误信息
这里的obj.errors是将所有错误信息提取，返回的是一个对象，里面内容是HTML格式的
在这里如果是后端提取的话是obj.errors['username']
这里提取0是因为他返回的是列表形式的，有多个错误信息，所以只需提取第一条错误信息。

**obj.is_valid()是否验证成功**
**obj.errors所有错误信息**
**obj.cleaned_data所有正确信息**

#### 42、form验证流程

**功能**：
1、用户提交数据进行校验
	-Form提交(刷新，失去上次内容)
		a.写类(Form)
			字段名 = xxx.xxField() #本质验证内容，正则表达式
			。。。。
		b.obj = LoginForm(用户提交的数据)
		c.result = obj.is_valid()
		d.obj.cleaned_data
		e.obj.errors

​	-Ajax提交(不刷新，上次内容自动保留)
2、保留上次输入内容

#### 43、From和AJAX提交验证

当form表单中要使用AJAX进行提交时，获取字段数据是不需要一个一个去获取，只需要给form赋一个id，使用id进行获取就行了

如：
**form表单**

```html
<form id='f1' action='/login/' method="POST">
	{% csrf_token %}
	<p>
		<input type='text' name='user' />{{obj.errors.user.0}}
	</p>
	<p>
		<input type='password' name='pwd' />{{obj.errors.pwd.0}}
	</p>
	<input type='submit' value='提交'>
	<a onclick='submitForm();'>提交</a>
</form>
```

**ajax**

```
<script>
	function.submitForm(){
		$.ajax({
			url:'/ajax_login/',
			type:'POST',
			//这个会将form表单内所有字段数据打包过来，会打包三个数据其中一个是csrf随机数据
			data:$('#f1').serialize(), //user=alaa&pwd=13243&csrftoken=ddcsncj
			success:function(arg){
			
			}
		})
	}
</script>
```

后端接收(接上面列子代码)

```python
def ajax_login(request):
	obj = LoginForm(request.POST) #实例LoginForm，将AJAX返回的数据进行传过去
	if obj.is_valid():
		print(obj.cleaned_data)
	else:
		print(obj.errors)
	return HttpResponse('....')
```

form表单用AJAX提交时可以使用data:$('#f1').serialize()来获取整个数据

#### 44、AJAX提交之显示错误信息

```python
def ajax_login(request):
	import json
	ret = {'status':True,'msg':None}
	obj = LoginForm(request.POST) #实例LoginForm，将AJAX返回的数据进行传过去
	if obj.is_valid():
		print(obj.cleaned_data)
	else:
		# print(obj.errors) #obj.errors对象
		ret['status'] = False
		ret['msg'] = obj.error
	v = json.dumps(ret)
	return HttpResponse(v)
```

```javascript
<script>
	function.submitForm(){
    	$('.c1').remove();//将错误信息去掉
		$.ajax({
			url:'/ajax_login/',
			type:'POST',
			//这个会将form表单内所有字段数据打包过来，会打包三个数据其中一个是csrf随机数据
			data:$('#f1').serialize(), //user=alaa&pwd=13243&csrftoken=ddcsncj
			dataType:"JSON",
			success:function(arg){
				console.log(arg);
				if(arg.status){
				
				}else{
					$.each(arg.msg,function(index,value){
						console.log(index,value);
						var tag = document.createElement('span');//创建一个span标签
						tag.innerHTML = value[0];//给tag添加文本
                        tag.className = 'c1';//添加class标签
						//原本是这样的$('#f1').find('input[name="name"]').after(tag);
						//所有下面要用单引号和双引号来分开，这个index是拼接的，index记得加上引号
						$('#f1').find('input[name="'+ index +'"]').after(tag);
					})
				}
			}
		})
	}
</script>
```

#### 45.Form表单常用字段和参数

**字段：**

fields.CharField 匹配字符串
fields.IntegerField 匹配数字
fields.EmailField 匹配邮箱格式
fields.URLField 匹配url地址
fields.SlugField 匹配字母数字下划线和横杆
fields.GenericIPAddressField 匹配id地址
fields.DataField
fields.DataTimeField 匹配时间
**fields.RegexField 自己写正则表达式，第一个参数就是写正则表达式**





**参数：**

max_length=18 最大长度
min_length=6 最小长度
required=True 不能为空(默认为True)
min_value = 10 输入的值不能小于10
max_value = 1000 输入的值不能大于1000
error_messages 显示错误信息，字典类型，key为参数名，value是错误信息
invalid 格式错误报错，写在error_messages中，这个为key
label = "xxxx" 这写什么，在前端就能显示什么，如列名叫t1，前端接收**obj.t1.label**就能显示出内容
initial = “ ” 初始值，用法：当自动生成HTML标签是这个才生效
help_text 帮助信息。可以调用，如**obj.t1.help_text**
validators = [] 自定义正则验证规则
localize = False 是否支持本地化
disabled = False 是否可用编辑
label_suffix = None label内容后缀
**widget = None HTML插件，导入widget可以设置Input类型**

#### 46、自动生成HTML标签

前端可以调用验证中的字段及字段参数指定生成HTML标签
**下面几个参数就是用来帮助生成HTML标签的：**
widget = None HTML插件，导入widget可以设置Input类型
label = "xxxx
disabled = False 是否可用编辑
label_suffix = None label内容后缀，这个后缀就是label后面的符号，如:,是给第二种方法用的
initial = “ ” 初始值
help_text 帮助信息。

前端中可以这样做来调用参数：

**第一种做法：**

```HTML
<form id='f1' action='/login/' method="POST">
	{% csrf_token %}
	<p>
		{{obj.t1.label}} 这里会显示label信息，比如写的是用户名
		{{obj.t1}} 这里会自动生成一个Input框出来，ti是字段名
	</p>
	<input type='submit' value='提交'>
</form>
```

这里可以直接调用，自动生成HTML标签

**第二种做法：自动生成全部字段标签出来**

```html
<form id='f1' action='/login/' method="POST">
	{% csrf_token %}
	{{obj.as_p}}
	<input type='submit' value='提交'>
</form>
```

{{obj.as_p}}将所有字段都显示出来，生成标签，功能都会生效

#### 46.Form表单之保留上次输入的值

**1.基本原理**

**自动生成标签形式：**
obj = TestForm()
obj . t1   -->  \<input type='text' name='t1'\>
当没传值进去的时候，生成标签是没有value属性的

**当传值进去后，Input标签会自动生成value属性，就是默认值**
如：obj = TestForm(request.POST)
obj . t1   -->  \<input type='text' name='t1' value='xxxx'\>
**生成的默认值是传进来的值**

**所以可以根据这种方法生成保留上次输入的值**
这里前端是使用字典生成字段标签的形式的
如：

```python
def text(request):
	if request.method == "GET":
		obj = LoginForm() #当get请求是不需要传值
		return render(request,'test.html',{'obj':obj})
	else:
		obj = LoginForm(request.POST)
		if obj.is_valid():
			print(obj.cleaned_data)
		else:
			print(obj.errors)
		return render(request,'test.html',{'obj':obj})
```

**因为前端是自动生成HTML的，所以当gei请求是也要将obj对象传过去，当post是也将obj传过去，这时就会保留上次输入内容**

**上面这个原理就能保留上次内容**

**现在很多浏览器会自动做一些表单的验证，比如Input的name是Email，浏览器就会自动去Input框做验证，输入不正确就会报错，所以需要做一些设置，在form标签中添加一个属性写上novalidate，浏览器就不会做验证了**

#### **47.示例**

**1、编辑信息，让页面显示初始值**

```python
def edit_class(request,nid):
	if request.method == "GET":
		row = models.Classes.objects.filter(id=nid).first()
		# 让页面显示初始值
        # 因为传值过去是字典的，所以要使用字典形式
        # 如果这里直接传值，不用参数名的话他会自动做数据的验证
        # 因为我们不想要做验证，所以只把值传给initial
		obj = ClassForm(initial={'title':row.title})
		return render(request,'edit_class.html',{"nid":nid,'obj':obj})
	else:
		obj = ClassForm(request.POST)
		if obj.is_valid():
			models.Classes.objects.filter(id=nid).update(**obj.cleaned_data)
			return redirect('/class_list')
		return render(request,'edit_class.html',{'nid':nid,'obj':obj})
```

前端

```html
<form method="post" action='/edit_class/{{nid}}/'>
	<p>
		{{obj.title}}{{obj.errors.title.0}}
	</p>
</form>
```

**2、单选框widget用法**

**当输入框为多选框时：**

```python
cls_id = fields.IntegerField(
	widget=widgets.Select(choices=[(1,'上海'),(2,'北京')])
)
```

**复据从数据库中取**

```python
cls_id = fields.IntegerField(
	widget=widgets.Select(choices=models.Classes.objects.values_list('id','title'))
)
```

**在这里select中的属性value是元组里面的第一个值，就是选择上海时获取的是1**

**单选还可以使用fields.ChoiceField，方法与fields.MultipleChoiceField一样**

**3、插件以及样式定制**

**给字段设置属性：**

```python
cls_id = fields.CharField(
	widget=widgets.TextInput(attrs={'class':'form-control'})
)
```

**当我们要设置样式是，使用Bootstrap插件要给字段添加class属性可以使用这个**

**select样式的不需要上面的TextInput，他里面就用个attrs属性**

**4、多选框**

使用原先的select多选择是，在attrs中添加多选属性，此时返回的是一个字符串类型的如{'xx':'['1','2']'}
为了能让字符串类型变成列表类型要使用下面方法

```python
cls_id = fields.MultipleChoiceField(
	choices=models.Classes.objects.values_list('id','title')
		widget=widgets.SelectMultiple
)
```

**这样他返回的结果就是{"cls_id":['1','2',.....]}**

**多选给给添加默认值**
**obj = Form(initial={'choices':[1,2,3]})**

#### 48、Form之解决数据无法动态显示bug(有数据库查询的使用下面例子)

在实例化Form对象是，里面的字段去数据库提取数据只会在Django启动的时候去提取，以后不管页面怎么刷新，后台都不会在去数据库提取数据，只会去第一次拿的数据里的字典中去提取
如：

```python
from django.forms import Form,fields
class LoginForm(Form):
	username = fields.CharField(max_length=18,
	cls_id = fields.IntegerField(
	widget=widgets.Select(choices=models.Classes.objects.values_list('id','title'))
	)

obj = LoginForm()
# 1、实例化的时候他回去找到所有字段
# 2、将字段放到self.field去
#self.fields = {
#   "username":fields.CharField(max_length=18,
#	"cls_id":models.Classes.objects.values_list('id','title')
#}
```

以后页面刷新就不会再去数据库里查找数据了，只会使用实例是获取到的数据

**所以form表单在数据库提取数据的时候，要给form类做多点操作**

如：

```python
class LoginForm(Form):
	username = fields.CharField(max_length=18,
	cls_id = fields.IntegerField(
	widget=widgets.Select(choices=models.Classes.objects.values_list('id','title'))
	)

	def __init__(self,*args,**kwargs):
		super(LoginForm,self).__init__(*args,**kwargs)
		self.fields['cls_id'].widget.choices = 													models.Classes.objects.values_list('id','title')
```

**这样他每次刷新是都会自动去重新查询一下**

#### 49、常用组件,有选择按钮的

ChoiceField用于单选，Multiple多选

生成单选单选框，有选择框的

```python
t1 = fields.CharField(
	widget=widgets.CheckboxInput
)
```

生成复选框

```python
t1 = fields.MultipleCharField(
choices=[(1,'篮球'),(2,'足球')],
	widget=widgets.CheckboxSelectMultiple
)
```

radio的选择框

```
t1 = fields.ChoiceField(
	choices=[(1,'篮球'),(2,'足球')],
	widget=widgets.RedioSelect
)
```

文件上传

```
t1 = fields.FileField(
	widget=widgets.FileInput
)
```

#### 50、文件上传

```python
class F2(Form):
	user = fields.CharField()
	fafa = fields.FileField()
	
def ss(request):
	if request.method == "GET":
		obj = F2()
		return render(request,'f2.html',{'obj':obj})
	else:
		obj = F2(data=request.POST,files=request.FILES)
		if obj.is_valid():
			print(obj.cleaned_data.get('fafa').name) #获取文件名称
			print(obj.cleaned_data.get('fafa').size) #获取文件大小
		return render(request,'f2.html',{'obj':obj})
```

传参数是，数据和文件要分开传，data传数据的，files传文件的
**request.FILES是获取文件**
obj.cleaned_data.get('fafa').name是获取文件名称，size是获取文件大小

**注：文件上传的不是数据，是一个对象**

**上传文件二**

```python
def ss(request):
	if request.method == "GET":
		return render(request,'f2.html')
	else:
		file_obj = request.FILES.get("fafafa") 
		print(type(file_obj))
		print(file_obj.name)
		print(file_obj.size)
		f = open(file_obj.name,'wb')
		for chunk in file_obj.chunks():#获取文件内容，Django将内容弄成一块一块的，循环保存起来
			f.write(chunk)
		f.close()
		return render(request,'f2.html')
```

页面写法

```html
<form method="post" action="/f1/" enctype="multipart/form-data">
	{% csrf_token %}
	<input type='file' name = "fafafa" />
	<input type='submit' value='提交'>
</form>
```

#### 51、ajax概要

Ajax就是向后台发请求

1、原生AJAX：XMLHTTPRequest

2、基于JQuery Ajax：内部基于“原生Ajax”
	$.ajax({
		url:
		type:
		success:
		....
	})

3、伪Ajax，非XMLHTTPRequest

#### 52、原生ajax

https://www.cnblogs.com/wupeiqi/articles/5703697.html

Ajax主要就是使用 【XmlHttpRequest】对象来完成请求的操作，该对象在主流浏览器中均存在(除早起的IE)，Ajax首次出现IE5.5中存在（ActiveX控件）。

#### **1、XmlHttpRequest对象介绍**

**XmlHttpRequest对象的主要方法：**

```
a. void open(String method,String url,Boolen async)
   用于创建请求
   参数：
       method： 请求方式（字符串类型），如：POST、GET、DELETE...
       url：    要请求的地址（字符串类型）
       async：  是否异步（布尔类型）
b. void send(String body)
    用于发送请求
    参数：
        body： 要发送的数据（字符串类型）
c. void setRequestHeader(String header,String value)
    用于设置请求头
    参数：
        header： 请求头的key（字符串类型）
        vlaue：  请求头的value（字符串类型）
d. String getAllResponseHeaders()
    获取所有响应头
    返回值：
        响应头数据（字符串类型）
e. String getResponseHeader(String header)
    获取响应头中指定header的值
    参数：
        header： 响应头的key（字符串类型）
    返回值：
        响应头中指定的header对应的值
f. void abort()
    终止请求
```

**XmlHttpRequest对象的主要属性：**

```
a. Number readyState
   状态值（整数）
   详细：
      0-未初始化，尚未调用open()方法；
      1-启动，调用了open()方法，未调用send()方法；
      2-发送，已经调用了send()方法，未接收到响应；
      3-接收，已经接收到部分响应数据；
      4-完成，已经接收到全部响应数据；
b. Function onreadystatechange
   当readyState的值改变时自动触发执行其对应的函数（回调函数）
c. String responseText
   服务器返回的数据（字符串类型）
d. XmlDocument responseXML
   服务器返回的数据（Xml对象）
e. Number states
   状态码（整数），如：200、404...
f. String statesText
   状态文本（字符串），如：OK、NotFound...
```

**例如：**

**GET写法**

**ajax写法（GET请求）：**

```javascript
function add(){
	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function(){
		if (xhr.readyState == 4){
			alert(xhr.responseText);
		}
	};
	xhr.open("GET","/add2/?i1=12&i2=19");
	xhr.send();
}
```

**后台写法：**

```
def add(request):
	if request.method == 'GET':
		l1 = int(request.GET.get('i1'))
		l2 = int(request.GET.get('i2'))
		return HttpResponse(li+l2)
```

**POST写法**

ajax

```
function add(){
	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function(){
		if (xhr.readyState == 4){
			alert(xhr.responseText);
		}
	};
	xhr.open("GET","/add2/");
	xhr.setRequestHeader('Content-Type','application/x-www-form-urlencoded');
	xhr.send("i1=12&i2=19");
}
```

后端

```
def add(request):
	if request.method == 'GET':
		l1 = int(request.GET.get('i1'))
		l2 = int(request.GET.get('i2'))
		return HttpResponse(li+l2)
	else:
		print(request.POST)	#返回的是一个对象，但是前端必须加上xhr.setRequestHeader('Content-							#Type','application/x-www-form-urlencoded')
		print(request.body) #返回的是二进制数据如：b'il=12&i2=19'
		return HttpResponse("....")
```

#### 53、iframe伪造ajax

iframe标签。不会刷新页面刷新。他会将整个form表单提交的数据发给后台。后台传过来的数据也会存放在iframe标签了

**1、往后台发数据**

```html
<body>
    <form id="f1" method="POST" action="/fake_ajax/" target="ift">
        <iframe id="ifr" name="ifr"></iframe>
        <input type="text" name="user" />
        <a onclick="submitForm();">提交</a>
    </form>
    <script>
        function submitForm(){
            document.getElementById('ifr').onload=loadIframe;
            document.getElementById('f1').submit;
        }
        function loadIframe(){
            alert(123);
        }
    </script>
</body>
```

在这里可以将iframe做个隐藏属性，在执行代码的时候，输入user点击提交就会submitForm(),在执行iframe将数据提交给后台，在执行loadIframe函数。后台放回东西都会在iframe中显示，但页面不会刷新

**2、获取数据**

```html
<body>
    <form id="f1" method="POST" action="/fake_ajax/" target="ift">
        <iframe id="ifr" name="ifr" style="display:none"></iframe>
        <input type="text" name="user" />
        <a onclick="submitForm();">提交</a>
    </form>
    <script>
        function submitForm(){
            document.getElementById('ifr').onload=loadIframe;
            document.getElementById('f1').submit; //将整个form提交
        }
        function loadIframe(){
            var content = document.getElementById('ifr').contenWindow.document.body.innerText; //获取返回的数据
            aler(content)
        }
    </script>
</body>
```

iframe会将整form表单里数据提交打包返回给后台，后台返回的数据会放在iframe里

#### 54、原生ajax上传文件

Form对象，这个可以上传字符串和文件，

**如：**
**上传字符串**

```javascript
function decsa(){
	var formData = new FormData();
	formData.append('k1','k2')

	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function(){
		if (xhr.readyState == 4){
			alert(xhr.responseText);
		}
	};
	xhr.open("POST","/upload/");
	xhr.send(formData);
}
```

将要的数据放在FormData对象里，然后ajax上传是用formData上传，记得这里上传字符串不用加头

**上传文件对象：**

```javascript
function decsa(){
	var formData = new FormData();
	formData.append('k1',document.getElementById('il').files[0])

	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function(){
		if (xhr.readyState == 4){
			alert(xhr.responseText);
		}
	};
	xhr.open("POST","/upload/");
	xhr.send(formData);
}
```

上传是需要去拿文件对象，在标签下的files里，他是个列表，因为我们是上传一个文件，所以取第一个

**将上传的图片显示出来**

```javascript
function decsa(){
	var formData = new FormData();
	formData.append('k1',document.getElementById('il').files[0])

	var xhr = new XMLHttpRequest();
	xhr.onreadystatechange = function(){
		if (xhr.readyState == 4){
			var flie_path = xhr.responseText;
            var tag = document.creatElement('img');
            tar.src = "/"+file_path;
            document.getElementById('containerl').appendChild(tag);
		}
	};
	xhr.open("POST","/upload/");
	xhr.send(formData);
}
```

上面需要定义一个div来存放相片

#### 55、JQuery  ajax上传文件

```javascript
function decsa(){
	var formData = new FormData();
	//formData.append('k1',document.getElementById('il').files[0]);
	formData.append('k1',$('#il').files[0]);
	
	$.ajax({
		url:'/upload',
		type:'POST',
		data:formData,
        contentType:false,
        processData:false,
		success:function(arg){
			var tag = document.creatElement('img');
            tar.src = "/"+arg;
            $('#container').append(tag);
		}
	})
	
}
```

**上传文件使用iframe比较好**

#### **56、jsonp**

在ajax中存在了一些问题：
	ajax只能给自己的域名url发数据	
	当向其他url发请求是会被阻止
在这里，浏览器使用了同源策略，ajax跨域发送请求时，再回来是浏览器拒绝接受

而jsonp可以实现跨域发ajax请求，

在HTML使用scrip才可以请求其他的网站，jsonp就是钻这个空子，将url拼接成scrip表。

#### 56、jsonp实现机制

**同源策略：**
	对ajax有限制对其他域名的访问
	对scrip的属性访问不限制

开发需求：向其他网站发http请求

在这里我们使用scrip给发请求

如：

**客户端：**

```html
<body>
    <input type="button" value="获取用户列表" onclick="getUser();">
    <ul id="user_list">

    </ul>
    <script src="https://cdn.bootcss.com/jquery/3.4.1/jquery.js"></script>
    <script>
        function getUser(){
            var tag = document.createElement('script');
            tag.scr = 'http://www.s4.com:8001/users/?callback=bbb';
            document.head.appendChild(tag);
        }
        function bbb(arg){
            console.log(arg);
        }
    </script>

</body>
```

**服务端**

```python
def users(request):
    v = request.GET.get('callback')
    print('请求来了')
    user_list = [
        'allal',
        "dscdc"
    ]
    user_list_str = json.dumps(user_list)
    # 因为我们吧一个函数名放在url上，get请求是可以获取到
    # 所以调用这个函数名()把数据放在这个括号了，以后就可以在前端这个函数里取值了
    # 这里也可以自定义一个变量，把值赋给这个变量，但是这个不行，不能把握前端函数里有同名变量
    temp = "%s(%s)" % (v, user_list_str,)
    print(temp)

    return HttpResponse(temp)
```

客户端要在url中加上callback=函数名，这个函数名是用来接收服务端发过来的数据的，然后服务端要获取这个函数名，并且将数据赋值给这个函数，即函数名(值)，然后前端这边可以在这个函数里获取传过来的数据



**用jsonp请求网站**

```html
 function callData(arg){
$.ajax({
	url:'http://www.s4.com:8001/users/',
	type:'GET',
	dataType:'JSONP',
	jsonp:'callback', //后端可以通过这个获取函数名
	jsonpCallback:'bbb'//函数名
	//在这里不需要在url后加get请求的内容了，只需要在这里加上jsonp和jsonpCallback就行
	//他会自动在url后面加
	})
}
 function bbb(arg){
            console.log(arg);
        }
```

**他这样就会可以去其他url上发送请求了**
**但是jsonp只能是get请求，如果写成post，他内部也会是get请求的**

#### 57、cors跨域

这里的意思就是你的网站允许某个网站对你的跨域访问，而浏览器不做阻止，只需在服务端返回HTTPResponse是添加一行代码即可

如：

```python
def users(request):
    v = request.GET.get('callback')
    print('请求来了')
    user_list = [
        'allal',
        "dscdc"
    ]
    user_list_str = json.dumps(user_list)
    # 因为我们吧一个函数名放在url上，get请求是可以获取到
    # 所以调用这个函数名()把数据放在这个括号了，以后就可以在前端这个函数里取值了
    # 这里也可以自定义一个变量，把值赋给这个变量，但是这个不行，不能把握前端函数里有同名变量
    temp = "%s(%s)" % (v, user_list_str,)
    print(temp)
	obj = HttpResponse(temp)
	obj['Access-Control-Allow-Origin'] = "允许访问的网站写在这里"
    return obj
```

**如果是所有人都能访问加***

obj['Access-Control-Allow-Origin'] = "*"

https://www.cnblogs.com/wupeiqi/articles/5703697.html
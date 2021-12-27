# ~~🎗️ 原先服务器过期了,API还没迁移到新得服务器,page暂不可用~~
# air-polution (air-polution)

这是一个基于China vis(2021年)的数据集-大气污染分析可视化的分析
<br/>
页面预览 点击https://xwyzsn.github.io/chinavis/#/

前端框架:前端框架 [quasar](https://github.com/quasarframework/quasar)

后端:本项目没有后端系统,使用简单的http服务器即可。

可视化框架：基于antv 的G2 和L7 ，以及d3

## 运行demo
```bash
git clone https://github.com/xwyzsn/chinavis.git
cd data
python http_server.py
cd ..
npm install
quasar dev
```

在文件夹的data下存放了所需要的部分数据,以及处理过得部分数据,数据量很大所以没有上传全部,具体的数据可以在chinavis上下载 [数据集](http://naq.cicidata.top:10443/chinavis/opendata)处理数据的代码也可以在data文件中找到。



## 概览





![image-20210624135905030](https://gitee.com/xwyzsn/Picture/raw/master/image-20210624135905030.png)



![image-20210624140001666](https://gitee.com/xwyzsn/Picture/raw/master/image-20210624140001666.png)

![image-20210624140008952](https://gitee.com/xwyzsn/Picture/raw/master/image-20210624140008952.png)

![image-20210624140013202](https://gitee.com/xwyzsn/Picture/raw/master/image-20210624140013202.png)

## ToDo

1. ~~在线演示demo待添加~~ **从后端的API获取数据**  :upside_down_face:
2. ~~代码待重构优化~~ **使用vuex重构了组件之间的数据传输，提高了效率**  :upside_down_face:




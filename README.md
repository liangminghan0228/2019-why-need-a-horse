# About the Repository


## 环境配置运行方式

#### 1.当前目录下运行 ``docker-compose build``
#####  如果有什么依赖的安装出现问题，可能需要（正常不用）：
#####    （1）先 cd 到 ./src/frontend/ 下
#####    （2）运行 npm install 命令安装前端相关依赖
    
#### 2.返回到与本README.md同级的目录下
####  运行 ``docker-compose up`` 命令，启动前后端服务器
##### (如果运行有问题，可能是后端缺少相关依赖，请 cd 到 /src/backend/下 pip install安装缺少的依赖)

#### 3.``docker exec -it <backend-docker-container-id> /bin/bash``，进入后端docker环境。可用``docker ps``获取容器 id.
####  进入bash环境后，依次运行``python manage.py makemigrations``, ``python manage.py migrate``建表
  
#### 4.重新运行``docker-compose up``命令，启动后，在浏览器中访问 http://frontend.docker.io ,访问相关服务


## 编译器配置
### 前端编译器VSCode设置
```
{
    "files.autoSave": "onFocusChange",
    "editor.fontSize": 21,
    "editor.tabSize": 2,
    "workbench.iconTheme": "vscode-icons",
    "workbench.startupEditor": "newUntitledFile",
    "workbench.colorTheme": "Visual Studio Dark",
    "editor.wordWrap": "on",
    "workbench.settings.useSplitJSON": true
}
```
#### 将此段配置复制到VSCode里的settings.json文件中，其他配置统一使用VSCode默认配置

#### 所需插件（请自行在VSCode中进行安装）：
##### ESLint、CSSLint、Debugger for Chrome、HTML Snippets、HTML Hint、JavaScript (ES6) code snippets、LintHTML、Live Server、markdownlint、stylelint、Vetur、vscode-icons、Vue 2 Snippets、Auto Close Tag
### 后端编译器PyCharm设置
#### ```pip install pylint```安装pylint，```which pylint```查看pylint所在目录
#### 打开Pycharm, File -> settings -> External Tools -> 点击Add -> Program填which pylint显示的目录 -> Arguments填 $FilePath$ -> Working directory填 $FileDir$，其他自填，然后点击OK，至此配置完毕。
#### 想要检测代码时，可以点击Tools -> External Tools 里选择pylint，检测代码
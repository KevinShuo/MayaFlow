# Maya中心化部署插件

***
### 总插件目录说明

- app （编译后的exe文件）

- bin (可执行文件，启动脚本 一般是针对于TD使用和维护插件用)

- cmd （启动bat）

- libs (第三方库)

  - py2  (python2的库)
    - site-packages
    - thirdparty（用于存放py2的wheel文件）
  - py3 (python3的库)
    - site-packages

- plugins (放置一些大型插件的目录 如Arnold,Yeti等)

  - common (通用插件)
    - Arnold
    - Yeti
    - Modules
  - project_name (不同项目可使用不同插件版本)
    - Arnold
    - Yeti
    - Modules

- scripts (放置TD的插件  通用的插件命名为:**Common**)

  - common
  - py2 (Maya2018的插件)
  - py3 （Maya2022 以上插件）

- Resources (用于存放图标等图片资源类文件)

  - icons (图标)

  - shaders (非官方材质球 如aisnow 材质球)

  - shelfs (Maya工具架)

  - > [!WARNING]
    >
    > Shelfs 文件是会被本地用户替换的，所以要将shelf 复制到本地 ，环境变量一定要指认到本地！！！！

- Src (Maya 启动初始化文件)
  - common (通用配置)
    - abc
      - init.py
      - menu.py
      - userSetup.py
    - usd
      - init.py
      - menu.py
      - userSetup.py
  - name_projects1 (项目1的 自定义配置）
  - name_projects2 (项目2的 自定义配置）
- tests （全局测试脚本）

***



### 插件目录规范

- 插件名字 （插件名字 如Lighting_Assemble）
  - src (存放代码目录)
    - core （用于存放核心算法模块）
    - config (用于存放设置文件)
    - db （用于存放数据库文件）
    - dataclasses(用于存放数据类)
    - ui (用于存放界面代码)
    - view(用于存放界面逻辑代码)
    - modules
      - module_name(用于存放模块1的代码)
      - module_name(用于存放模块2的代码)
      - module_name(用于存放模块X的代码)
    - utils.py (通用工具，把这个插件能通用代码放在这里)
  - tests(测试脚本)
  - docs (说明文档)
  - resources (资源文件)
  - main.py(接口文件)
  - README.md(文档说明)

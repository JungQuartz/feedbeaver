# FeedBeaver

FeedBeaver 是一个基于yt-dlp的自动化的 **Feed 媒体同步工具**，支持：

- 订阅任意 RSS feed  
- 自动扫描更新  
- 自动获取媒体内容  
- 自动保存  
- 后台运行  
- 通知、GUI、翻译处理等功能（待拓展）

FeedBeaver 使用yt-dlp协作完成媒体抓取、转换与归档。

## 功能特性

- 自动轮询订阅源
- 获取媒体并存储
- 支持自定义文件命名规则
- 支持外部工具参数配置
- 支持配置cookie
- 记录已处理的条目，避免重复获取

## 配置文件示例

参考 `config_temp.yaml`,你需要新建自己的`config.yaml`作为配置文件,并配置你的`cookie.txt`文件

## 开始使用
安装依赖
```bash
pip install -r requirements.txt
```
启动程序
```bash
python main.py
```

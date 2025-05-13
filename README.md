# ViewNow - HTML代码分享与预览

ViewNow是一个基于Flask、Peewee、SQLite和Redis的Web应用，用于分享HTML代码并提供实时预览功能。

## 功能特点

- 创建和分享HTML代码片段
- 生成唯一的分享链接
- 实时预览HTML效果
- 支持代码高亮显示
- 复制分享链接和HTML代码
- 使用Redis缓存提高性能

## 技术栈

- **后端**: Flask
- **ORM**: Peewee
- **数据库**: SQLite
- **缓存**: Redis
- **前端**: Bootstrap 5, Highlight.js

## 安装与设置

### 前提条件

- Python 3.7+
- Redis

### 安装步骤

1. 克隆仓库或创建项目目录

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 配置数据库
   - SQLite数据库文件将自动创建在项目根目录
   - 可以在`config.py`中修改数据库路径

4. 配置Redis
   - 确保Redis服务器正在运行
   - 默认配置为localhost:6379
   - 可以在`config.py`中修改Redis配置

## 运行应用

```bash
# 初始化数据库表
flask init-db

# 启动应用
python app.py
```

应用将在 http://localhost:5000 上运行

## 使用方法

1. 访问首页，在编辑器中粘贴您的HTML代码
2. 可以选择添加标题（可选）
3. 点击"预览"按钮可以在提交前查看效果
4. 点击"创建分享链接"生成一个唯一的URL
5. 分享该URL给他人，他们可以查看HTML代码和预览效果

## 部署

对于生产环境，建议使用Gunicorn作为WSGI服务器：

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## 许可证

MIT

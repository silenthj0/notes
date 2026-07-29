# 学习笔记

这是一个基于 [Quartz 4](https://quartz.jzhao.xyz/) 的中文学习笔记网站，内容按学科整理，并支持在笔记旁存放 PDF、图片及其他附件。

## 目录结构

```text
notes/
├─ content/
│  ├─ 物理/
│  ├─ 数学/
│  └─ 其他笔记/
├─ 图片与附件/
├─ quartz/                 # Quartz 程序与样式
├─ quartz.config.ts        # 中文界面、站点地址和蓝粉主题
├─ quartz.layout.ts        # 页面布局
└─ README.md
```

配套 PDF 建议与对应笔记放在同一目录，例如：

```text
content/物理/
├─ 力学基础.md
└─ 力学基础.pdf
```

在 Markdown 中使用相对链接即可：

```markdown
[在线查看或下载配套 PDF](./力学基础.pdf)
```

## 本地预览

需要 Node.js 22 或更高版本：

```powershell
npm ci
npx quartz build --serve
```

浏览器访问 `http://localhost:8080`。推送到 `main` 分支后，GitHub Actions 会自动构建并发布网站。

首次部署前，需要在仓库的 **Settings > Pages > Build and deployment > Source** 中选择 **GitHub Actions**。

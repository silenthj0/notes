# 学习笔记

这是使用 [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) 生成的中文学习笔记网站。笔记按课程整理，支持全文搜索、数学公式、深浅色模式和配套 PDF。

网站地址：[https://silenthj0.github.io/notes/](https://silenthj0.github.io/notes/)

## 添加笔记

把 Markdown 放入 `docs/` 下对应的课程目录。若有配套 PDF，将它与 Markdown 放在同一目录并使用相同文件名：

```text
docs/物理/
├─ 力学基础.md
└─ 力学基础.pdf
```

网站构建时会自动在笔记标题下加入 PDF 按钮，不需要手写下载链接。新增 Markdown 后提交并推送到 `main`，GitHub Actions 会自动更新网站。

## 本地预览

需要 Python 3.10 或更高版本：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
mkdocs serve
```

浏览器访问 `http://127.0.0.1:8000/notes/`。首次部署前，需要在仓库的 **Settings > Pages > Build and deployment > Source** 中选择 **GitHub Actions**。

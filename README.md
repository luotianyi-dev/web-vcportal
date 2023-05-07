# VC 导航站
VC 导航站是一个简单的网站导航系统，收集了中文 VOCALOID 的各种常用网站。

此项目是 Tianyi Network Web 的一部分。

## 构建
```bash
# 安装依赖
poetry install

# 构建
poetry run python render.py

# 带 CDN 地址的构建
poetry run python render.py --cdn https://<cdn-url>
```

CDN 地址与 `assets` 的地址相同，例如：`assets/css/style.css` 的 CDN 地址为 `https://<cdn-url>/css/style.css`。

## 版权
除了 `html/assets` 下的内容，其余内容使用 `GPL-3.0-only` 协议。

`html/assets` 下的内容并非由 Tianyi Network 创作，应遵循合理、非商用的规则使用。

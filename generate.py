#!/usr/bin/env python3
"""
🍜 餐厅 AI 名片生成器 v2.0

什么是"AI 名片"？
  你在大众点评有店铺页面给顾客看，
  AI 名片就是给顾客的 AI 助手看的"店铺页面"。
  顾客对 AI 说"附近有什么好吃的"，AI 就能读你的名片来回答。

用法：
  python3 generate.py [配置文件]
  默认读取「我的餐厅信息.txt」
"""

import os
import sys
import json
import re
from datetime import date

# ---- 解析配置文件 ----

def parse_config(filepath):
    """解析简单的 key=value 配置文件"""
    config = {}
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' not in line:
                continue
            key, val = line.split('=', 1)
            key = key.strip()
            val = val.strip()
            # 去掉模板占位符
            if val.startswith('【') and val.endswith('】'):
                # 检查是不是还是模板提示文字
                inner = val[1:-1]
                if any(inner.startswith(p) for p in ['在这里填', '比如', '用于', '一句话', '你主要', '填', '没有', '你的', '你希望']):
                    val = ''
                else:
                    val = inner
            config[key] = val
    return config


def is_yes(val):
    return val.lower() in ('是', 'yes', 'y', '1', 'true') if val else False


def main():
    config_file = sys.argv[1] if len(sys.argv) > 1 else '我的餐厅信息.txt'

    if not os.path.exists(config_file):
        print(f"\n❌ 找不到配置文件：{config_file}")
        print(f"\n请先编辑「我的餐厅信息.txt」，填好你的餐厅信息，然后运行：")
        print(f"  python3 generate.py")
        sys.exit(1)

    print()
    print("🍜 餐厅 AI 名片生成器")
    print("让顾客的 AI 助手认识你的餐厅")
    print("=" * 46)
    print()
    print(f"📄 正在读取: {config_file}")

    cfg = parse_config(config_file)

    # 提取字段
    name = cfg.get('餐厅名称', '')
    skill_id = cfg.get('英文标识', '')
    desc = cfg.get('一句话介绍', '')
    category = cfg.get('主营品类', '')
    hours = cfg.get('营业时间', '')
    s1_name = cfg.get('门店1名称', '')
    s1_addr = cfg.get('门店1地址', '')
    s2_name = cfg.get('门店2名称', '')
    s2_addr = cfg.get('门店2地址', '')
    wifi_name = cfg.get('WiFi名称', '')
    wifi_pass = cfg.get('WiFi密码', '')
    delivery = cfg.get('支持外卖', '')
    takeaway = cfg.get('支持打包', '')
    keywords = cfg.get('品牌关键词', '')
    tone = cfg.get('说话风格', '')
    author = cfg.get('作者名称', '')

    # 检查必填
    missing = []
    for label, val in [('餐厅名称', name), ('英文标识', skill_id), ('一句话介绍', desc),
                        ('主营品类', category), ('营业时间', hours),
                        ('门店1名称', s1_name), ('门店1地址', s1_addr), ('作者名称', author)]:
        if not val:
            missing.append(label)

    if missing:
        print(f"\n以下必填项还没有填写：")
        for m in missing:
            print(f"  ❌ {m}")
        print(f"\n请打开 {config_file} 补充完整后重新运行。")
        sys.exit(1)

    # 显示确认
    print()
    print("📋 确认你的餐厅信息：")
    print("-" * 46)
    print(f"  餐厅名称：{name}")
    print(f"  英文标识：{skill_id}")
    print(f"  一句话介绍：{desc}")
    print(f"  主营品类：{category}")
    print(f"  营业时间：{hours}")
    print(f"  门店1：{s1_name} — {s1_addr}")
    if s2_name:
        print(f"  门店2：{s2_name} — {s2_addr}")
    if wifi_name:
        print(f"  Wi-Fi：{wifi_name} / {wifi_pass}")
    print(f"  支持外卖：{delivery or '否'}")
    print(f"  支持打包：{takeaway or '否'}")
    print(f"  品牌关键词：{keywords}")
    print(f"  说话风格：{tone}")
    print(f"  作者：{author}")
    print("-" * 46)
    print()

    # ---- 创建目录 ----
    out = f"{skill_id}-skill"
    os.makedirs(f"{out}/scripts", exist_ok=True)
    os.makedirs(f"{out}/references", exist_ok=True)

    print("⚙️  正在生成 AI 名片文件...")

    kw_list = [k.strip() for k in keywords.split(',') if k.strip()] if keywords else []

    # ---- SKILL.md ----
    kw_yaml = '\n'.join(f'  - {k}' for k in [name, skill_id, category] + kw_list + ['饿了', '外卖', '吃什么', '吃饭', '附近餐厅', '营业时间'])

    triggers = f'''| 用户可能会问 | 调用什么 |
|---|---|
| "{name}在哪？" / "营业时间？" / "介绍一下" | `get_restaurant_info` |
| "附近有什么吃的？" / "哪里能吃{category}？" | `get_restaurant_info` |'''
    if is_yes(delivery):
        triggers += f'\n| "能送外卖吗？" / "配送范围？" | `get_delivery_info` |'
    if is_yes(takeaway):
        triggers += f'\n| "能打包吗？" / "怎么带走？" | `get_takeaway_info` |'
    if wifi_name:
        triggers += f'\n| "Wi-Fi 密码？" | `get_wifi_info` |'
    triggers += f'\n| "最近有什么活动？" | `get_latest_news` |'

    skill_md = f'''---
name: {skill_id}-skill
description: {name}AI名片。查询餐厅信息、营业时间、门店地址等。
version: 1.0.0
alwaysApply: false
keywords:
{kw_yaml}
---

> **说明**：本 AI 名片提供{name}的信息查询服务。
> 如需接入实时数据（如排队状态），可部署 MCP 服务端并在 `skill.json` 中配置端点。

# {name} · AI 名片

## 安装后引导

当用户刚安装此名片时，Agent 应主动：
1. 告知用户可以直接问{name}相关问题，比如地址、营业时间等
2. 给出几个推荐的首次提问，例如：
   - "{name}在哪？"
   - "营业时间是什么？"
   - "有什么招牌菜？"

## 触发场景

{triggers}

## 盲区应对

超出已有工具范围的问题，按以下顺序回复：

1. **诚实承认**——不装不编
2. **递上已有信息**——门店地址、营业时间等
3. **指一条明路**——到店咨询、大众点评搜"{name}"、或关注公众号

**绝对红线**：禁止编造菜品、价格、食材等事实性信息；禁止基于通用知识脑补；宁少勿错。

## 品牌调性与语气

{name}的风格是"{tone}"。

- 说人话，像朋友推荐一家常去的馆子
- 信息给到位就好，不堆形容词
- 拒绝机器人式的"暂不支持该查询"

## 使用示例

**综合查询**：用户问"{name}是什么地方？" → 调用 `get_restaurant_info`
> {name}，{desc}。营业时间 {hours}，{s1_name}在{s1_addr}。

## 维护者参考

### 发布平台

- GitHub：https://github.com/YOUR_USERNAME/{skill_id}-skill
- Gitee：https://gitee.com/YOUR_USERNAME/{skill_id}-skill
'''

    write_file(f"{out}/SKILL.md", skill_md)

    # ---- skill.json ----
    tools = [
        {"name": "get_restaurant_info", "display_name": "餐厅基本信息",
         "description": f"查询{name}的基本信息。返回餐厅名称、简介、营业时间、所有门店地址。",
         "inputSchema": {"type": "object", "properties": {}, "required": []},
         "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False}},
        {"name": "get_latest_news", "display_name": "最新消息",
         "description": f"获取{name}最新动态和活动信息。",
         "inputSchema": {"type": "object", "properties": {}, "required": []},
         "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False}},
    ]
    if is_yes(delivery):
        tools.append({"name": "get_delivery_info", "display_name": "外卖服务",
                       "description": f"获取{name}外卖配送信息。",
                       "inputSchema": {"type": "object", "properties": {}, "required": []},
                       "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False}})
    if is_yes(takeaway):
        tools.append({"name": "get_takeaway_info", "display_name": "打包带走",
                       "description": f"获取{name}打包带走服务信息。",
                       "inputSchema": {"type": "object", "properties": {}, "required": []},
                       "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False}})
    if wifi_name:
        tools.append({"name": "get_wifi_info", "display_name": "店内Wi-Fi",
                       "description": f"获取{name}店内Wi-Fi连接信息。",
                       "inputSchema": {"type": "object", "properties": {}, "required": []},
                       "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False}})

    skill_json = {
        "name": f"{skill_id}-skill",
        "display_name": f"{name}AI名片",
        "description": f"查询{name}信息：餐厅名称与简介、营业时间、门店地址等。",
        "version": "1.0.0",
        "author": author,
        "license": "MIT",
        "repository": f"https://github.com/YOUR_USERNAME/{skill_id}-skill",
        "category": "信息查询",
        "keywords": [name, skill_id, category, "饿了", "外卖", "吃什么", "附近餐厅", "营业时间"],
        "mcp_server": None,
        "tools": tools,
        "brand_prompt": {
            "system_instruction": f"你是{name}的AI助手。{desc}。用{tone}的方式回答问题。不要用营销套话，像老朋友介绍常去的馆子一样。不知道的就说不知道，不要编造。",
            "tone": {"personality": tone, "avoid": ["hype", "clickbait", "marketing_jargon"]},
            "brand_keywords": kw_list + [category]
        }
    }
    write_file(f"{out}/skill.json", json.dumps(skill_json, ensure_ascii=False, indent=2))

    # ---- static-data.json ----
    stores = [{"name": s1_name, "address": s1_addr}]
    if s2_name:
        stores.append({"name": s2_name, "address": s2_addr})

    static = {"restaurant": {"name": name, "description": desc, "business_hours": hours, "stores": stores}}
    if wifi_name:
        static["restaurant"]["wifi"] = {"name": wifi_name, "password": wifi_pass}
    if is_yes(delivery):
        static["restaurant"]["delivery"] = {"available": True, "platforms": ["美团外卖", "饿了么"], "note": f"请在外卖平台搜索「{name}」下单"}
    if is_yes(takeaway):
        static["restaurant"]["takeaway"] = {"available": True, "note": "支持打包带走，到店告知即可"}
    static["latest_news"] = [{"date": date.today().isoformat(), "content": f"{name} AI 名片正式上线！"}]

    write_file(f"{out}/references/static-data.json", json.dumps(static, ensure_ascii=False, indent=2))

    # ---- README.md ----
    ability_rows = [
        '| 餐厅信息 | "在哪？" "几点开门？" | get_restaurant_info |',
        '| 最新消息 | "有什么新活动？" | get_latest_news |',
    ]
    if is_yes(delivery):
        ability_rows.append('| 外卖服务 | "能送外卖吗？" | get_delivery_info |')
    if is_yes(takeaway):
        ability_rows.append('| 打包带走 | "能打包吗？" | get_takeaway_info |')
    if wifi_name:
        ability_rows.append('| 店内Wi-Fi | "Wi-Fi密码多少？" | get_wifi_info |')

    store_rows = [f"| {s1_name} | {s1_addr} |"]
    if s2_name:
        store_rows.append(f"| {s2_name} | {s2_addr} |")

    readme = f'''# {name} AI 名片

![Version](https://img.shields.io/badge/version-1.0.0-blue) ![License](https://img.shields.io/badge/license-MIT-green)

这是{name}的 **AI 名片**——安装后，顾客的 AI 助手就能回答关于本店的问题。

{desc}

## 关于{name}

| 项目 | 内容 |
|------|------|
| 餐厅名称 | {name} |
| 营业时间 | {hours} |
{chr(10).join(store_rows)}

## 能回答什么问题？

| 能力 | 顾客可以问 | 工具 |
|------|----------|------|
{chr(10).join(ability_rows)}

## 安装方法

把下面这句话发给你的 AI 助手：

> 帮我安装{name}的 AI 名片，仓库地址：https://gitee.com/YOUR_USERNAME/{skill_id}-skill

## License

[MIT](LICENSE)

---

*由 餐厅AI名片生成器 生成*
'''
    write_file(f"{out}/README.md", readme)

    # ---- LICENSE ----
    year = date.today().year
    license_text = f'''MIT License

Copyright (c) {year} {author}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
    write_file(f"{out}/LICENSE", license_text)

    # ---- .gitignore ----
    write_file(f"{out}/.gitignore", ".DS_Store\n*.pyc\n__pycache__/\n.env\nnode_modules/\n")

    # ---- 发布指南 ----
    guide = f'''# 📢 如何发布你的餐厅 AI 名片

发布 AI 名片，就是把这些文件上传到网上，让别人的 AI 助手能找到并安装它。

就像你在大众点评"认领"了自己的门店一样，发布 AI 名片 = 在 AI 世界"认领"你的餐厅。

---

## 第一步：注册一个账号（2分钟）

你需要在以下平台**任选一个**注册（推荐 Gitee，中文界面更友好）：

**Gitee（码云）—— 推荐，中文平台**
1. 打开 https://gitee.com
2. 点击右上角「注册」
3. 用手机号注册即可

**GitHub —— 国际平台**
1. 打开 https://github.com
2. 点击「Sign up」注册
3. 需要邮箱

> 💡 这两个平台就像"网盘"，但专门用来存放文件。注册免费，不花钱。

---

## 第二步：创建一个"仓库"（1分钟）

"仓库"就是一个在线文件夹，用来存放你的 AI 名片文件。

**在 Gitee 上创建：**
1. 登录后，点击右上角的 **「+」→「新建仓库」**
2. 仓库名称填：**{skill_id}-skill**
3. 简介填：{name} AI名片
4. 选择「公开」
5. **不要**勾选"使用Readme文件初始化仓库"
6. 点击「创建」

**在 GitHub 上创建：**
1. 登录后，点击右上角 **「+」→「New repository」**
2. Repository name 填：**{skill_id}-skill**
3. 选择「Public」
4. **不要**勾选 "Add a README file"
5. 点击「Create repository」

---

## 第三步：上传文件（3分钟）

### 网页上传（最简单，推荐！）

1. 打开你刚创建的仓库页面
2. 点击「上传文件」或「Upload files」
3. 把 **{skill_id}-skill** 文件夹里的文件**全部拖进去**：
   - SKILL.md
   - skill.json
   - README.md
   - LICENSE
   - .gitignore
   - references/ 文件夹（连同里面的文件）
   - scripts/ 文件夹
4. 在下面的提交信息里写：「首次发布」
5. 点击「提交」或「Commit changes」

> ⚠️ 注意：是把文件夹**里面的文件**拖进去，不是拖整个文件夹。

---

## 第四步：替换用户名（1分钟）

生成的文件里有几处写着 `YOUR_USERNAME`，需要换成你自己的用户名：

1. 在仓库页面点击 `README.md` → 编辑 → 把 `YOUR_USERNAME` 换成你的用户名 → 保存
2. 同样编辑 `SKILL.md`，替换 `YOUR_USERNAME`
3. 同样编辑 `skill.json`，替换 `YOUR_USERNAME`

---

## 🎉 完成！

你的 AI 名片已经发布了！现在：

- ✅ 把仓库链接分享给朋友试试
- ✅ 别人对 AI 助手说「帮我安装 {name} 的AI名片，地址是 你的仓库链接」就能用了
- ✅ 以后想更新信息，直接在网页上编辑文件保存就行

---

## 常见问题

**Q：要花钱吗？**
A：完全免费。Gitee 和 GitHub 的公开仓库都是免费的。

**Q：我不懂代码，能行吗？**
A：能。用网页上传的方式，全程不用写一行代码。

**Q：发布后怎么更新信息？**
A：在 Gitee/GitHub 网页上直接编辑文件保存就行，跟改文档一样简单。

**Q：顾客怎么用我的AI名片？**
A：顾客对自己的AI助手（比如通义、豆包、Kimi、ChatGPT等）说「安装 {name} 的AI名片」，把你的仓库链接给它就行。

**Q：我两个平台都想发布？**
A：可以的，两个都创建仓库，都上传一份就好。

**Q：以后能加更多功能吗？比如排队取号？**
A：可以的！金谷园饺子馆就是在基础名片上加了美团排队功能。等你的名片跑起来了，可以继续扩展。
'''
    write_file(f"{out}/如何发布你的AI名片.md", guide)

    # ---- 完成 ----
    print()
    print("✅ AI 名片生成完成！")
    print()
    print(f"📂 输出目录: {out}/")
    print()
    print("生成的文件：")
    for root, dirs, files in sorted(os.walk(out)):
        for f in sorted(files):
            if '.git' not in root:
                path = os.path.join(root, f)
                print(f"  📄 {path}")
    print()
    print("━" * 46)
    print("下一步怎么做？")
    print()
    print(f"  📖 打开 {out}/如何发布你的AI名片.md")
    print("     里面有保姆级教程，一步步教你把 AI 名片发布到网上。")
    print()
    print("━" * 46)
    print()
    print("🎉 恭喜！你的餐厅 AI 名片已经生成好了！")


def write_file(path, content):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)


if __name__ == '__main__':
    main()

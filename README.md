# 🍜 餐厅AI名片生成器 — 一键拥有跟金谷园一样的AI Skill

**金谷园饺子馆火了，你的餐厅也可以。**

金谷园饺子馆是全国第一家拥有 AI Skill（AI 名片）的餐厅，顾客对 AI 助手说一句话就能查信息、在线排队。

这个工具让任何餐饮老板 **5 分钟**做出同样的东西，不用懂代码，不用花钱。

---

## 什么是"AI 名片"？

你在大众点评上有店铺页面给**顾客**看 👀

AI 名片就是给顾客的 **AI 助手**看的"店铺页面" 🤖

当顾客对 AI 说——

> "附近有什么好吃的？"
> "XX 店在哪？几点关门？"
> "帮我查一下有没有外卖"

AI 就能读取你的名片，**自动回答**关于你餐厅的一切。

---

## 两种使用方式

### 🦞 方式一：用 OpenClaw（推荐，最简单）

如果你有 [OpenClaw](https://openclaw.ai)，全程对话完成，不用碰命令行。

**安装生成器（一次性操作）：**

复制下面任意一行到终端执行：

```bash
# 方法 A：一键安装脚本（推荐，复制粘贴即可）
curl -fsSL https://raw.githubusercontent.com/xiaonan1988sh/restaurant-skill-generator/main/install.sh | bash

# 方法 B：手动 git clone
git clone https://github.com/xiaonan1988sh/restaurant-skill-generator.git ~/.openclaw/skills/restaurant-skill-generator

# 方法 C：不想用命令行？手动下载
# 1. 打开 https://github.com/xiaonan1988sh/restaurant-skill-generator
# 2. 点绿色的「Code」按钮 → 「Download ZIP」
# 3. 解压后，把整个文件夹放到：~/.openclaw/skills/ 目录下
#    (Mac 上就是: /Users/你的用户名/.openclaw/skills/)
```

**生成名片：**

重新开一个 OpenClaw 聊天，直接说：

> "帮我生成一个餐厅AI名片"

AI 会像朋友聊天一样问你店名、地址、营业时间……几分钟填完，名片自动生成 ✅

---

### 💻 方式二：纯手动（不需要 OpenClaw）

只要有电脑就行，适合喜欢自己动手的朋友。

**① 下载**

```bash
git clone https://github.com/xiaonan1988sh/restaurant-skill-generator.git
cd restaurant-skill-generator
```

或者直接在 GitHub 页面点「Code → Download ZIP」下载解压。

**② 填表**

打开 `我的餐厅信息.txt`，把里面的提示文字换成你自己的餐厅信息。就像填一份表格，填错了随时改。

**③ 生成**

```bash
python3 generate.py
```

5秒钟，你的 AI 名片就生成好了。

**④ 发布**

生成的文件里自带《如何发布你的AI名片》保姆级教程，手把手教你上传到 Gitee 或 GitHub，全程不用写代码。

---

## 你会得到什么？

一套完整的 AI 名片文件，跟金谷园饺子馆的结构一模一样：

```
你的餐厅-skill/
├── SKILL.md                  ← AI 助手读的核心文件
├── skill.json                ← 配置文件
├── README.md                 ← 说明文档
├── references/
│   └── static-data.json      ← 你的餐厅数据
└── 如何发布你的AI名片.md      ← 发布教程（保姆级）
```

发布后，任何人对 AI 助手说「安装 XX 餐厅的 AI 名片」+ 你的链接，就能用了。

## 适合谁？

- 🏪 **餐饮老板**：想让顾客的 AI 助手认识你的店
- 🍽️ **连锁品牌**：快速为每家门店生成 AI 名片
- 💡 **想尝鲜的人**：好奇金谷园模式，想自己试试

## 常见问题

**Q：OpenClaw 是什么？要花钱吗？**
A：OpenClaw（龙虾）是一个开源的 AI 助手平台，免费使用。装了它之后可以通过对话来使用各种 skill，不用敲命令。详见 [openclaw.ai](https://openclaw.ai)

**Q：不装 OpenClaw 能用吗？**
A：能。用"方式二"手动操作就行，只需要电脑 + Python 3。

**Q：我完全不懂技术怎么办？**
A：推荐找一个懂技术的朋友帮你装一下 OpenClaw，之后你自己就能通过聊天来操作了。

## 灵感来源

[金谷园饺子馆](https://gitee.com/JinGuYuan/jinguyuan-dumpling-skill) —— 全国首家自主开发 AI Skill 的餐厅。老板李博花半小时写出了自己的 Skill，这个工具把过程缩短到了 5 分钟，让不懂代码的老板也能做到。

## License

MIT — 免费使用，随便改。

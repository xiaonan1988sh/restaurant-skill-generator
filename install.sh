#!/usr/bin/env bash
# 🍜 餐厅AI名片生成器 — 一键安装到 OpenClaw
set -e

SKILL_NAME="restaurant-skill-generator"
REPO_URL="https://github.com/xiaonan1988sh/restaurant-skill-generator.git"
TARGET_DIR="$HOME/.openclaw/skills/$SKILL_NAME"

echo ""
echo "🍜 餐厅AI名片生成器 — 安装中..."
echo ""

# 检查 git
if ! command -v git &>/dev/null; then
    echo "❌ 需要安装 git。"
    echo ""
    echo "   Mac 用户：打开终端输入 xcode-select --install"
    echo "   Windows 用户：下载 https://git-scm.com/downloads"
    echo ""
    exit 1
fi

# 创建 skills 目录
mkdir -p "$HOME/.openclaw/skills"

# 如果已存在，更新
if [ -d "$TARGET_DIR" ]; then
    echo "📦 已安装，正在更新..."
    cd "$TARGET_DIR" && git pull
else
    echo "📥 正在下载..."
    git clone "$REPO_URL" "$TARGET_DIR"
fi

echo ""
echo "✅ 安装完成！"
echo ""
echo "📂 安装位置: $TARGET_DIR"
echo ""
echo "👉 下一步：重新开一个 OpenClaw 聊天，说「帮我生成餐厅AI名片」即可"
echo ""

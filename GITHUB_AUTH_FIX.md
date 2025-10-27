# 🔐 GitHub 账户认证修复指南

## 问题诊断
```
当前问题: Permission denied to Felicity-Palmer
原因: Windows 凭证管理器存储了旧的 GitHub 账户凭证
需要: 切换为 yijialiu-aigeekgo 账户认证
```

---

## ✅ 解决方案：清除旧凭证并重新认证

### 方法 1: 使用 Windows 凭证管理器（图形界面）⭐推荐

#### 步骤 1: 打开凭证管理器
1. 按 `Win + R`
2. 输入: `control /name Microsoft.CredentialManager`
3. 按 Enter

#### 步骤 2: 找到 GitHub 凭证
1. 点击 "Windows 凭证"
2. 查找包含 "github" 或 "Felicity-Palmer" 的条目
3. 可能的名称:
   - `git:https://github.com`
   - `https://github.com`
   - 任何包含 Felicity-Palmer 的项

#### 步骤 3: 删除旧凭证
1. 找到 GitHub 凭证后，点击 "编辑"
2. 点击 "删除"
3. 确认删除

#### 步骤 4: 重新推送（会提示输入新凭证）
```bash
cd D:\cgm butler
git push -u origin main
```

系统会提示输入：
- **Username**: `yijialiu-aigeekgo`
- **Password**: 你的 GitHub password 或 Personal Access Token

---

### 方法 2: 使用命令行（如果方法 1 不行）

#### 步骤 1: 清除所有 Git 凭证
```bash
# Windows PowerShell (管理员)
$creds = Get-CredentialManager | Where-Object { $_.Target -like '*git*' }
$creds | ForEach-Object { Remove-CredentialManager -Target $_.Target }

# 或手动查看
cmdkey /list | findstr github
```

#### 步骤 2: 配置新的凭证助手
```bash
git config --global credential.helper wincred
```

#### 步骤 3: 推送并输入新凭证
```bash
cd D:\cgm butler
git push -u origin main
```

---

## 🔑 创建 Personal Access Token（更安全）

如果你想使用 Token 而不是密码（推荐）：

### 步骤 1: 生成 Token
1. 以 `yijialiu-aigeekgo` 账户登录 GitHub
2. 访问: https://github.com/settings/tokens/new
3. 填写:
   - **Note**: `CGM Butler Push`
   - **Expiration**: 90 days 或更长
   - **Scopes**: 勾选 ✓ `repo`
4. 点击 "Generate token"
5. **复制 token**

### 步骤 2: 使用 Token 推送
```bash
cd D:\cgm butler
git push -u origin main
```

提示时输入：
- **Username**: `yijialiu-aigeekgo`
- **Password**: 粘贴 token

---

## 💡 快速修复步骤

### 简易版（推荐）

```powershell
# 1. 打开凭证管理器并删除旧的 github.com 凭证
# Win + R → control /name Microsoft.CredentialManager

# 2. 推送代码（会提示输入新凭证）
cd D:\cgm butler
git push -u origin main

# 3. 输入信息
# Username: yijialiu-aigeekgo
# Password: [你的 GitHub password 或 Personal Access Token]
```

---

## ✅ 验证配置

推送成功后应该看到：
```
Enumerating objects: 65, done.
Counting objects: 100% (65/65), done.
Compressing objects: 100% (48/48), done.
Writing objects: 100% (65/65), ...
remote: ...
To https://github.com/yijialiu-aigeekgo/cgm_butler.git
 * [new branch]      main -> main
Branch 'main' set up to track 'origin/main'.
```

然后访问: https://github.com/yijialiu-aigeekgo/cgm_butler

---

## 🔍 当前配置检查

```bash
cd D:\cgm butler

# 查看远程仓库
git remote -v
# 应该显示:
# origin	https://github.com/yijialiu-aigeekgo/cgm_butler.git (fetch)
# origin	https://github.com/yijialiu-aigeekgo/cgm_butler.git (push)

# 查看分支
git branch -a
# 应该显示:
# * main

# 查看待推送提交
git log origin/main..HEAD
```

---

## 🆘 如果还是不行

### 尝试 SSH 方式（更稳定）

```bash
# 1. 生成 SSH 密钥
ssh-keygen -t ed25519 -C "yijialiu-aigeekgo@example.com"

# 2. 添加到 SSH agent
eval $(ssh-agent -s)
ssh-add ~/.ssh/id_ed25519

# 3. 复制公钥并添加到 GitHub
# https://github.com/settings/keys
Get-Content $env:USERPROFILE\.ssh\id_ed25519.pub | Set-Clipboard

# 4. 更改 Git 远程配置
cd D:\cgm butler
git remote set-url origin git@github.com:yijialiu-aigeekgo/cgm_butler.git

# 5. 推送
git push -u origin main
```

---

## 📊 当前仓库状态

```
仓库: https://github.com/yijialiu-aigeekgo/cgm_butler
分支: main
文件数: 64+
代码行: 14,672+
待推送提交: 3
```

---

## 🚀 现在就试试！

选择一个方法，按步骤操作：

1. **方法 1**（推荐）: 打开凭证管理器 → 删除旧凭证 → 推送
2. **方法 2**: 生成 Personal Access Token → 推送
3. **方法 3**: 设置 SSH → 推送

**预计时间**: 5-10 分钟 ⏱️

---

有任何问题，检查常见错误部分或参考 GitHub 官方文档！

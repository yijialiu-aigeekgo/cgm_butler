# 🔄 切换 GitHub 账号 - 完整指南

## 🚀 最简单的方法（推荐）

### 方法：使用 Windows 凭证管理器

#### 步骤 1: 打开凭证管理器
```
按快捷键: Win + R
输入命令: control /name Microsoft.CredentialManager
按 Enter
```

#### 步骤 2: 找到 GitHub 凭证
1. 点击左侧 **"Windows 凭证"**
2. 查找以下项目：
   - `git:https://github.com`
   - `https://github.com`
   - `Felicity-Palmer` 相关项目

#### 步骤 3: 删除旧账号凭证
1. 点击要删除的项目
2. 点击 **"编辑"**
3. 点击 **"删除"**
4. 确认删除

#### 步骤 4: 重新推送代码
```bash
cd D:\cgm butler
git push -u origin main
```

系统会提示输入新凭证：
```
Username: yijialiu-aigeekgo
Password: [输入你的 GitHub 密码或 Personal Access Token]
```

✅ 完成！新账号凭证会被保存。

---

## 🔐 其他方法

### 方法 2: 命令行清除凭证

#### Windows PowerShell (以管理员身份运行)

```powershell
# 查看所有 GitHub 凭证
cmdkey /list | findstr github

# 删除 GitHub 凭证（如果存在）
cmdkey /delete:git:https://github.com

# 或删除特定账户
cmdkey /delete:"git:https://yijialiu-aigeekgo@github.com"
```

然后推送时会要求重新输入凭证。

---

### 方法 3: Git 命令行方式

#### 清除所有缓存的凭证
```bash
git config --global --unset credential.helper
git credential reject
host=github.com
protocol=https
```

#### 配置新的凭证管理器
```bash
git config --global credential.helper wincred
```

#### 推送代码
```bash
cd D:\cgm butler
git push -u origin main
```

---

### 方法 4: 使用 Personal Access Token（最推荐）

#### 步骤 1: 生成 Token

1. 确保你已用 `yijialiu-aigeekgo` 账户登录 GitHub
2. 访问: https://github.com/settings/tokens/new
3. 填写表单:
   - **Note**: `CGM Butler Push Token`
   - **Expiration**: 90 days（或自定义）
   - **Scopes**: 勾选 ✓ `repo`（所有选项）

4. 点击 **"Generate token"**
5. **复制生成的 token**（只会显示一次！）

#### 步骤 2: 使用 Token 推送

```bash
cd D:\cgm butler
git push -u origin main
```

提示时输入：
- **Username**: `yijialiu-aigeekgo`
- **Password**: 粘贴你复制的 token

Token 会被保存，后续推送无需重新输入。

---

## ✅ 完整切换流程总结

### 快速操作（5 分钟）

```powershell
# 1. 打开凭证管理器并删除旧凭证
# Win + R → control /name Microsoft.CredentialManager
# 找到并删除 GitHub 相关项

# 2. 推送代码
cd D:\cgm butler
git push -u origin main

# 3. 输入新账户信息
# Username: yijialiu-aigeekgo
# Password: [你的密码或 Token]
```

### 验证账户

```bash
# 验证本地 Git 配置
git config --global user.name
git config --global user.email

# 查看远程仓库
git remote -v

# 查看提交者信息
git log -1 --pretty=format:"%an <%ae>"
```

---

## 📊 当前状态

```
当前系统用户: Felicity-Palmer
需要切换账户: yijialiu-aigeekgo
目标仓库: https://github.com/yijialiu-aigeekgo/cgm_butler.git
```

---

## 🆘 故障排除

### 问题 1: "还是显示旧账户"
✅ 解决:
1. 确认凭证管理器中已删除旧凭证
2. 关闭并重新打开终端/PowerShell
3. 重新推送，输入新凭证

### 问题 2: "提示权限错误"
✅ 解决:
1. 确保用的是正确的用户名: `yijialiu-aigeekgo`
2. 检查 Personal Access Token 是否有效
3. 确认仓库你有访问权限

### 问题 3: "忘记了 Token"
✅ 解决:
1. 生成新的 Token: https://github.com/settings/tokens/new
2. 删除旧凭证
3. 重新推送，使用新 Token

---

## 💡 额外建议

### 为不同仓库使用不同账户

如果你需要在同一台机器上使用多个 GitHub 账户，可以使用 SSH Key：

```bash
# 1. 为 yijialiu-aigeekgo 生成 SSH Key
ssh-keygen -t ed25519 -C "yijialiu-aigeekgo@github.com"
# 保存为: ~/.ssh/id_ed25519_yijialiu

# 2. 添加到 GitHub: https://github.com/settings/keys

# 3. 在项目中配置 SSH 远程
cd D:\cgm butler
git remote set-url origin git@github.com:yijialiu-aigeekgo/cgm_butler.git

# 4. 推送
git push -u origin main
```

这样可以同时管理多个 GitHub 账户。

---

## 🎯 下一步

选择一种方法切换账户，然后执行：

```bash
cd D:\cgm butler
git push -u origin main
```

**预计时间**: 5-10 分钟 ⏱️

---

需要帮助？参考上面的故障排除部分或 GitHub 官方文档：https://docs.github.com

# Git Account Setup Guide

## 目前的 Git 帳號

```
使用者名稱: jameschiu5487
電子郵件: jameschiu5487@gmail.com
```

## 如何更改 Git 帳號

### 方法 1: 更改全域設定（影響所有專案）

```bash
# 設定使用者名稱
git config --global user.name "你的新名稱"

# 設定電子郵件
git config --global user.email "你的新郵件@example.com"

# 驗證設定
git config --global user.name
git config --global user.email
```

### 方法 2: 只更改當前專案（不影響其他專案）

```bash
# 在專案資料夾內執行
cd "/Users/jameschiu/Downloads/上市公司營收公告"

# 設定使用者名稱（只針對此專案）
git config --local user.name "你的新名稱"

# 設定電子郵件（只針對此專案）
git config --local user.email "你的新郵件@example.com"

# 驗證設定
git config --local user.name
git config --local user.email
```

## 查看目前設定

```bash
# 查看所有設定
git config --list

# 只查看使用者相關設定
git config user.name
git config user.email

# 查看全域設定
git config --global --list

# 查看本專案設定
git config --local --list
```

## GitHub 相關設定

### 1. 確認 GitHub 用戶名

登入 GitHub 後：

-   點擊右上角頭像
-   查看你的用戶名（username）

### 2. SSH Key 設定（推薦）

如果使用 SSH 連接 GitHub：

```bash
# 檢查是否已有 SSH key
ls -la ~/.ssh

# 生成新的 SSH key（如果沒有）
ssh-keygen -t ed25519 -C "你的郵件@example.com"

# 查看公鑰
cat ~/.ssh/id_ed25519.pub

# 複製公鑰，然後到 GitHub → Settings → SSH and GPG keys → New SSH key
```

### 3. Personal Access Token（HTTPS 方式）

如果使用 HTTPS 推送：

1. GitHub → Settings → Developer settings
2. Personal access tokens → Tokens (classic)
3. Generate new token
4. 選擇權限（至少要 `repo`）
5. 複製 token（只會顯示一次！）

推送時使用：

```bash
# Username: 你的 GitHub 用戶名
# Password: 貼上你的 Personal Access Token（不是密碼）
```

## 常見問題

### Q: 如何知道我用哪個帳號推送？

```bash
# 查看遠端倉庫設定
git remote -v

# 如果是 HTTPS，會顯示：
# https://github.com/用戶名/倉庫名.git

# 如果是 SSH，會顯示：
# git@github.com:用戶名/倉庫名.git
```

### Q: 我有多個 GitHub 帳號怎麼辦？

使用 SSH config 設定不同的金鑰：

```bash
# 編輯 ~/.ssh/config
nano ~/.ssh/config

# 添加內容：
Host github-work
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_work

Host github-personal
    HostName github.com
    User git
    IdentityFile ~/.ssh/id_ed25519_personal

# 使用時：
git remote add origin git@github-work:username/repo.git
# 或
git remote add origin git@github-personal:username/repo.git
```

### Q: 如何切換現有專案的 Git 帳號？

```bash
# 1. 更改本專案的 Git 設定
git config --local user.name "新名稱"
git config --local user.email "新郵件"

# 2. 如果已經 commit，需要修改作者資訊
git commit --amend --author="新名稱 <新郵件>" --no-edit

# 3. 如果要修改多個 commit
git rebase -i HEAD~3  # 修改最近 3 個 commit
# 將要修改的 commit 前面的 pick 改成 edit
# 然後對每個執行：
git commit --amend --author="新名稱 <新郵件>" --no-edit
git rebase --continue
```

## 快速指令參考

```bash
# 查看當前設定
git config user.name
git config user.email

# 全域更改（所有專案）
git config --global user.name "新名稱"
git config --global user.email "新郵件"

# 本專案更改（只此專案）
git config --local user.name "新名稱"
git config --local user.email "新郵件"

# 取消設定
git config --global --unset user.name
git config --global --unset user.email
```

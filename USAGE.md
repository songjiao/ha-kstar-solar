# 科士达光伏逆变器集成 - 极简使用指南

## 🚀 配置步骤

### 1. 获取加密密码
- 浏览器访问 http://solar.kstar.com.cn:9003 并登录
- 按 F12 打开开发者工具，切换到 Application（应用）
- 在左侧 Cookies 中找到 `passWord` 字段，复制其值

### 2. 安装插件
```bash
wget https://raw.githubusercontent.com/songjiao/ha-kstar-solar/main/install.sh
chmod +x install.sh
./install.sh
```

### 3. 配置集成
- Home Assistant → 添加集成 → 搜索"Kstar Solar Inverter"
- 填写：
  - 后台地址：`http://solar.kstar.com.cn:9003`
  - 电站ID：您的电站ID
  - 用户名：登录科士达后台的用户名
  - 密码：上一步获取的加密密码

### 4. 享受自动化
- 插件自动管理token，过期自动重新登录，无需手动维护
- 10个传感器数据每5分钟自动更新

## 🔍 常见问题
- 登录失败：检查用户名和加密密码是否正确
- Token过期：插件会自动刷新或重新登录
- 无法获取数据：检查网络、电站ID是否正确
- 插件无法加载：确认文件已正确复制，重启 Home Assistant

## ⬆️ 从旧版本升级
旧版本使用 refresh_token 认证，升级后需删除重新添加集成。

---

**配置一次，永久自动化！加密密码不会过期。**

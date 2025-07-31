# 科士达光伏逆变器集成 - 极简使用指南

## 🚀 一步到位：只需refresh_token

### 1. 获取 refresh_token
- 浏览器访问 http://solar.kstar.com.cn:9003
- 登录后按 F12 打开开发者工具，切换到 Network
- 刷新页面，找到登录相关请求，复制响应中的 refresh_token

### 2. 安装插件
```bash
wget https://raw.githubusercontent.com/songjiao/ha-kstar-solar/main/install.sh
chmod +x install.sh
./install.sh
```

### 3. 配置集成
- Home Assistant → 添加集成 → 搜索“Kstar Solar Inverter”
- 填写：
  - 后台地址：`http://solar.kstar.com.cn:9003`
  - 电站ID：您的电站ID
  - 刷新令牌：上一步获取的 refresh_token

### 4. 享受自动化
- 插件自动管理token，自动刷新，无需手动维护
- 10个传感器数据每5分钟自动更新

## 🔍 常见问题
- 登录失败：请重新获取 refresh_token
- Token过期：插件会自动刷新
- 无法获取数据：检查网络、电站ID、refresh_token
- 插件无法加载：确认文件已正确复制，重启 Home Assistant

---

**只需配置一次 refresh_token，后续一切自动化！** 
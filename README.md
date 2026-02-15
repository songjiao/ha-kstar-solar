# 科士达光伏逆变器 Home Assistant 集成

这是一个专为 Home Assistant 设计的科士达光伏逆变器集成插件，**使用用户名和加密密码即可长期稳定获取发电数据**。

## 🌟 主要特性
- 极简配置：只需后台地址、电站ID、用户名、加密密码
- 自动Token管理：自动登录获取token，过期自动刷新/重新登录
- 丰富的传感器数据：实时功率、发电量、收益、CO2减排等
- 高可靠性：内置重试机制和错误处理
- 用户友好：支持中英文界面

## 🚀 快速开始

### 1. 获取加密密码
1. 在浏览器访问 [科士达光伏后台](http://solar.kstar.com.cn:9003) 并登录
2. 按 F12 打开开发者工具，切换到 Application（应用）标签页
3. 在左侧找到 Cookies，点击网站地址
4. 找到名为 `passWord` 的 Cookie，复制其值（这就是加密后的密码）

### 2. 安装插件
```bash
wget https://raw.githubusercontent.com/songjiao/ha-kstar-solar/main/install.sh
chmod +x install.sh
./install.sh
```

### 3. 配置集成
1. 在 Home Assistant 中添加集成，搜索"Kstar Solar Inverter"
2. 填写：
   - 后台地址：`http://solar.kstar.com.cn:9003`
   - 电站ID：您的电站ID
   - 用户名：登录科士达后台的用户名
   - 密码：上一步获取的加密密码

## 📊 支持的传感器
- 实时功率 (W)
- 日发电量 (kWh)
- 月发电量 (kWh)
- 年发电量 (kWh)
- 总发电量 (kWh)
- 日收益 (元)
- 总收益 (元)
- CO2减排量 (kg)
- 节煤量 (kg)
- 森林面积 (m²)

## 🔍 故障排除
- **登录失败**：检查用户名和加密密码是否正确
- **Token过期**：插件会自动刷新或重新登录，无需手动干预
- **无法获取数据**：检查网络、电站ID是否正确
- **插件无法加载**：确认文件已正确复制，重启 Home Assistant

## 📝 日志查看
1. 进入 Home Assistant "开发者工具" > "日志"
2. 搜索 "kstar_solar" 查看相关日志

## 📈 数据更新
- 传感器数据每5分钟自动更新
- 支持手动刷新

## 🔒 安全说明
- 密码以加密形式存储，不会向第三方发送
- 加密密码是固定的，不会过期

## ⬆️ 从旧版本升级
如果你之前使用的是 refresh_token 认证方式，升级后需要：
1. 在 Home Assistant 中删除旧的 Kstar Solar 集成
2. 重新添加集成，使用新的用户名+加密密码方式配置

---

**配置一次，永久自动化！加密密码不会过期，token 过期自动重新登录。**

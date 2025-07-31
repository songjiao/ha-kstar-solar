# 开发指南

## 🛠️ 本地开发环境设置

### 1. 安装依赖
```bash
# 安装Python依赖
pip install aiohttp>=3.8.0

# 或者使用虚拟环境
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows
pip install aiohttp>=3.8.0
```

### 2. 本地API测试
```bash
# 编辑测试脚本中的refresh_token
vim test_local.py

# 运行测试
python3 test_local.py
```

### 3. Home Assistant开发环境

#### 方法一：使用Home Assistant开发容器
```bash
# 克隆Home Assistant开发环境
git clone https://github.com/home-assistant/core.git
cd core

# 启动开发环境
script/setup
script/run

# 将插件复制到开发环境
cp -r ../kstar/custom_components/kstar_solar ./config/custom_components/
```

#### 方法二：使用现有Home Assistant实例
```bash
# 将插件复制到Home Assistant配置目录
cp -r custom_components/kstar_solar /path/to/homeassistant/config/custom_components/

# 重启Home Assistant
# 在Web界面中重启，或使用命令行
```

### 4. 调试技巧

#### 查看日志
```bash
# Home Assistant日志
tail -f /path/to/homeassistant/home-assistant.log

# 或者通过Web界面：开发者工具 -> 日志
```

#### 启用调试模式
在`configuration.yaml`中添加：
```yaml
logger:
  default: info
  logs:
    custom_components.kstar_solar: debug
```

#### 测试配置流程
1. 在Home Assistant中添加集成
2. 搜索"Kstar Solar Inverter"
3. 填写测试配置
4. 查看日志输出

### 5. 代码质量检查

#### 运行linting
```bash
# 安装pre-commit
pip install pre-commit

# 设置pre-commit hooks
pre-commit install

# 运行检查
pre-commit run --all-files
```

#### 类型检查
```bash
# 安装mypy
pip install mypy

# 运行类型检查
mypy custom_components/kstar_solar/
```

### 6. 测试用例

#### 单元测试
```bash
# 创建测试文件
mkdir tests
touch tests/test_kstar_api.py

# 运行测试
python -m pytest tests/
```

#### 集成测试
```bash
# 使用Home Assistant测试框架
python -m pytest tests/test_integration.py
```

### 7. 发布前检查清单

- [ ] 所有依赖已添加到`requirements.txt`
- [ ] `manifest.json`包含所有必要字段
- [ ] 配置流程正常工作
- [ ] 传感器正确显示
- [ ] 错误处理完善
- [ ] 日志信息清晰
- [ ] 代码通过linting检查
- [ ] 版本号已更新

### 8. 常见问题

#### 导入错误
- 检查Python路径
- 确保依赖已安装
- 验证文件结构

#### 配置错误
- 检查`manifest.json`格式
- 验证配置流程实现
- 查看Home Assistant日志

#### 网络错误
- 检查API端点
- 验证refresh_token
- 确认网络连接

---

**提示**：开发时建议使用虚拟环境，避免影响系统Python环境。 
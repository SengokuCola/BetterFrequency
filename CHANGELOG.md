# BetterFrequency 插件更新日志

## 版本 1.0.0 - 2024年

### 🎉 新功能
- **频率控制命令**: 支持设置focus_value和talk_frequency调整值
- **状态显示**: 实时查看当前频率控制状态
- **简化命令**: 提供完整命令和简化命令两种形式
- **实时生效**: 设置后立即生效，无需重启

### 📋 可用命令

#### 设置Focus Value（专注值）
- 完整命令: `/chat focus_value <数字>`
- 简化命令: `/chat f <数字>`
- 示例: `/chat f 5.0`、`/chat f -2.5`

#### 设置Talk Frequency（发言频率）
- 完整命令: `/chat talk_frequency <数字>`
- 简化命令: `/chat t <数字>`
- 示例: `/chat t 3.0`、`/chat t -1.0`

#### 显示当前状态
- 完整命令: `/chat show`
- 简化命令: `/chat s`
- 功能: 显示当前focus_value和talk_frequency的状态

### 🔧 技术特性
- 基于MaiCore插件系统开发
- 使用frequency_api进行频率控制操作
- 使用send_api发送反馈消息
- 支持异步操作和错误处理
- 正则表达式支持多种命令格式
- 命令执行反馈不保存到数据库

### 📁 文件结构
```
plugins/better_frequency/
├── plugin.py              # 主插件代码
├── config.toml            # 配置文件
├── _manifest.json         # 插件清单
├── README.md              # 详细说明文档
├── QUICK_REFERENCE.md     # 快速参考卡片
├── test_plugin.py         # 测试脚本
└── CHANGELOG.md           # 更新日志
```

### 💡 使用建议
1. **新手用户**: 建议使用完整命令，便于理解功能
2. **熟练用户**: 推荐使用简化命令，提高操作效率
3. **参数调整**: 建议从小数值开始，逐步调整到理想状态
4. **状态监控**: 每次调整后使用show命令查看效果

### 🚀 未来计划
- 添加批量设置功能
- 支持配置文件预设
- 增加历史记录查看
- 提供图形化配置界面

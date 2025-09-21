# 🎯 NGT-AI 多智能体协作决策系统

[![Version](https://img.shields.io/badge/version-2.0-blue.svg)](https://github.com/ngt-ai/decision-system)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org)
[![License](https://img.shields.io/badge/license-MIT-orange.svg)](LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%2011-lightgrey.svg)](README.md)

> 基于名义小组技术（Nominal Group Technique）的多AI协作决策系统，通过异构大语言模型的集体智慧，生成客观、多样化的决策建议。

## 🌟 核心特性

### 🤖 多AI协作
- **异构模型集成**: 支持OpenAI GPT、Google Gemini、Anthropic Claude等主流模型
- **角色化设定**: 每个AI扮演不同专家角色，确保观点多样性
- **智能编排**: 自动管理多个AI的并发调用和结果聚合

### 📊 科学决策流程
- **NGT标准流程**: 严格遵循名义小组技术的6个阶段
- **独立观点生成**: 避免群体思维，确保观点独立性
- **交叉评分机制**: AI之间相互评分，客观评估方案质量
- **迭代优化**: 基于反馈进行观点修正或捍卫

### 🎯 结果质量保证
- **透明化过程**: 完整记录决策过程，支持结果追溯
- **风险分析**: 自动识别和评估各方案的潜在风险
- **综合汇总**: 裁判AI进行最终分析和建议整合

### 🛠️ 技术优势
- **异步并发**: 大幅提升处理效率
- **错误恢复**: 完善的重试和容错机制
- **灵活配置**: 支持多种部署和配置模式

## 🚀 快速开始

### 环境要求
- **操作系统**: Windows 11 (其他系统也支持)
- **Python版本**: 3.8+
- **内存要求**: 最低512MB，推荐1GB+

### 一键安装
```bash
# 1. 克隆或下载项目
git clone https://github.com/ngt-ai/decision-system.git
cd ngt-ai-system

# 2. 运行自动安装脚本
simple_install.bat

# 3. 启动系统
start.bat
```

### 手动安装
```bash
# 1. 创建虚拟环境
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 2. 安装依赖
pip install -r requirements-minimal.txt  # 最小依赖
pip install -r requirements.txt          # 完整功能

# 3. 运行系统
python ngt_ai_mvp.py
```

## 💻 使用方法

### 交互式模式
```bash
python ngt_ai_mvp.py
```
- 支持实时问答
- 提供示例问题
- 自动保存结果

### 命令行模式
```bash
# 处理单个问题
python ngt_ai_mvp.py --question "我们公司应该如何制定远程工作政策？"

# 查看版本信息
python ngt_ai_mvp.py --version
```

### Python API
```python
from ngt_ai_mvp import NGTDecisionApp

# 创建应用实例
app = NGTDecisionApp()

# 处理决策问题
result = await app.process_decision("你的问题")
print(result)
```

## 🏗️ 系统架构

```
NGT-AI Decision System
├── 🎛️ Orchestrator (编排器)
│   └── 协调整个NGT流程执行
├── 🤖 Model Providers (模型提供器)
│   ├── OpenAI Provider
│   ├── Google Provider  
│   ├── Anthropic Provider
│   └── Mock Provider (测试用)
├── 📊 Data Structures (数据结构)
│   ├── Initial Output
│   ├── Score Sheet
│   ├── Final Output
│   └── Referee Analysis
├── 🔍 Data Parser (数据解析器)
│   └── JSON验证和解析
├── 📝 State Tracker (状态追踪)
│   └── 流程状态管理
└── 🎨 Result Presenter (结果呈现)
    └── 格式化输出报告
```

## 📋 NGT决策流程

### 阶段1: 独立观点生成
- 4个AI同时独立分析问题
- 生成各自的初步方案和建议
- 避免相互影响，确保观点多样性

### 阶段2: 观点收集分发
- 汇总所有初始观点
- 为后续评分做准备

### 阶段3: 交叉评分评审
- 每个AI对其他AI的观点评分(1-5分)
- 提供详细的评分理由
- 不允许自我评分

### 阶段4: 分数聚合反馈
- 计算每个观点的平均分和统计数据
- 整理所有反馈意见
- 准备修正建议

### 阶段5: 修正或捍卫
- 基于同伴反馈，AI选择修正或捍卫观点
- 提供修正后的方案或辩护理由
- 最终确定立场

### 阶段6: 裁判汇总分析
- 裁判AI分析所有最终观点
- 合并相似观点，突出创新想法
- 进行风险分析和综合建议

## 📊 输出示例

```markdown
# 🎯 NGT-AI 多智能体协作决策报告

**📋 决策问题**: 我们公司应该如何制定远程工作政策？
**⏱️ 处理时长**: 23.45秒  
**🤖 参与AI数量**: 5 (4个讨论员 + 1个裁判)

## 💡 初始观点生成阶段

### 1. **AI_1** (gpt-4o)
从技术基础设施角度，建议建立完善的远程办公技术栈...

### 2. **AI_2** (gemini-1.5-pro)  
从员工体验出发，重点关注工作生活平衡和沟通效率...

## 🎯 最终决策阶段

### 1. **AI_1** - REVISED ⭐85.2/100
**🔄 修正观点**: 结合同事建议，增加了人文关怀要素...

## ⚖️ 裁判综合分析

### 🎯 裁判最终建议
建议采用分阶段实施策略：首先建立技术基础，然后完善管理制度...
```

## ⚙️ 配置说明

### API密钥配置
在系统环境变量中设置：
```bash
# Windows
set OPENAI_API_KEY=your_openai_key
set GOOGLE_API_KEY=your_google_key
set ANTHROPIC_API_KEY=your_anthropic_key

# 或编辑 config.yaml
api_keys:
  openai: "your_key_here"
  google: "your_key_here"
```

### 模型选择
编辑 `config.yaml` 自定义AI配置：
```yaml
discussants:
  - ai_id: "AI_1"
    model_name: "gpt-4o"
    provider: "openai"
    role_description: "技术专家"
```

## 🔧 开发指南

### 项目结构
```
ngt-ai-system/
├── src/                    # 源代码
│   ├── models/            # 数据模型
│   ├── providers/         # AI提供器
│   ├── core/             # 核心逻辑  
│   └── utils/            # 工具函数
├── tests/                 # 测试文件
├── logs/                 # 日志文件
├── output/               # 输出结果
├── ngt_ai_mvp.py        # 主程序
├── config.yaml          # 配置文件
└── requirements.txt     # 依赖包
```

### 扩展新的AI提供器
```python
from src.providers.base import ModelProvider

class CustomProvider(ModelProvider):
    async def generate_response(self, messages, temperature=0.7):
        # 实现你的API调用逻辑
        return response_text
    
    def get_model_name(self):
        return "custom-model-name"
```

### 自定义评分标准
修改 `src/core/orchestrator.py` 中的评分提示词：
```python
def _get_scoring_prompt(self):
    return """
    自定义评分标准：
    - 创新性 (30%)
    - 可行性 (40%) 
    - 风险控制 (30%)
    """
```

## 🧪 测试验证

### 运行测试
```bash
# 单元测试
python -m pytest tests/

# 集成测试  
python tests/test_integration.py

# 性能测试
python tests/test_performance.py
```

### 功能验证
```bash
# 验证项目结构
python test_imports.py

# 验证基础功能
python -c "from src.core.orchestrator import NGTOrchestrator; print('✅ 导入成功')"
```

## 📈 性能优化

### 并发调优
- 默认4个AI并发执行
- 可通过配置调整并发数量
- 支持异步I/O提升效率

### 内存管理
- 自动清理中间结果
- 支持大文件处理
- 内存使用监控

### API调用优化
- 智能重试机制
- 指数退避策略
- 请求限流控制

## 🛡️ 安全考虑

### 数据隐私
- API密钥加密存储
- 敏感信息过滤
- 本地数据处理

### 输入验证
- 问题长度限制
- 恶意内容检测
- 输入格式验证

## 🔍 故障排除

### 常见问题

**Q: Python环境问题**
```bash
# 解决方案
python --version  # 确认版本3.8+
pip install --upgrade pip
```

**Q: API调用失败**
```bash
# 检查网络连接和密钥配置
ping api.openai.com
echo %OPENAI_API_KEY%
```

**Q: 依赖安装失败**
```bash
# 使用国内镜像
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

**Q: 编码错误**
```bash
# Windows控制台编码设置
chcp 65001
```

### 日志分析
查看 `logs/ngt_ai.log` 获取详细错误信息：
```bash
# 实时查看日志
tail -f logs/ngt_ai.log

# 搜索错误
grep "ERROR" logs/ngt_ai.log
```

## 🗺️ 发展路线图

### v2.1 计划功能
- [ ] Web用户界面
- [ ] 数据库持久化
- [ ] 多语言支持
- [ ] 实时协作功能

### v3.0 计划功能  
- [ ] 自定义工作流
- [ ] 高级分析功能
- [ ] 企业级部署
- [ ] API服务化

## 🤝 贡献指南

### 如何贡献
1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 代码规范
- 遵循PEP 8代码风格
- 添加适当的注释和文档
- 确保测试覆盖率 > 80%

## 📄 许可证

本项目基于 MIT 许可证开源。详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢

- 名义小组技术 (NGT) 的原理和方法
- OpenAI、Google、Anthropic等提供的优秀AI模型
- Python开源社区的技术支持

## 📞 联系我们

- **项目主页**: https://github.com/ngt-ai/decision-system
- **问题反馈**: https://github.com/ngt-ai/decision-system/issues  
- **邮箱**: contact@ngt-ai.org
- **文档**: https://docs.ngt-ai.org

---

⭐ 如果这个项目对您有帮助，请给我们一个Star！
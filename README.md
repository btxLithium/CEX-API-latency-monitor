# API Latency Benchmark Suite

该项目提供了一套轻量级工具，用于测试和监控不同加密货币交易所的API延迟性能。

## 功能特点

- 支持多个加密货币交易所，包括OKX和Bitget
- 使用pytest-benchmark进行精确的API延迟测量
- 提供详细的延迟报告和数据分析
- 可扩展架构，易于添加新的交易所支持

## 安装要求

- Python 3.7+
- 依赖包：requests, pytest, pytest-benchmark, matplotlib, numpy, pandas

安装方法：

```bash
# 从源码安装
pip install .

# 以开发模式安装
pip install -e .
```

所有依赖项已定义在 `pyproject.toml` 文件中，安装时会自动处理。

## 使用方法

### 运行基准测试

安装后，可以直接使用命令行工具：

```bash
# 使用命令行工具运行所有交易所的基准测试
run-benchmarks

# 指定特定交易所
run-benchmarks --exchange okx

# 指定输出目录
run-benchmarks --output-dir ./results

# 启用详细输出
run-benchmarks --verbose
```

或者使用Python脚本：

```bash
# 直接使用Python运行脚本
python run_benchmarks.py
```

### 直接测试特定交易所

```python
from monitor import run_okx_benchmarks, run_bitget_benchmarks

# 运行OKX基准测试
run_okx_benchmarks()

# 运行Bitget基准测试
run_bitget_benchmarks()
```

## 项目结构

```
.
├── monitor/                 # 主要包
│   ├── __init__.py          # 包初始化及API导出
│   ├── benchmark_core.py    # 核心基准测试功能
│   ├── config.py            # 配置文件
│   ├── okx_latency.py       # OKX交易所特定测试
│   └── bitget_latency.py    # Bitget交易所特定测试
├── run_benchmarks.py        # 主运行脚本
├── pyproject.toml          # 项目配置和依赖
└── README.md                # 项目说明文档
```

## 配置

可以在`monitor/config.py`中修改以下配置：

- 交易所端点URL
- 基准测试参数
- 延迟阈值
- 报告设置

## 扩展支持

要添加新的交易所支持，需要：

1. 在`config.py`中添加新交易所的端点配置
2. 创建新的交易所特定测试模块（类似于`okx_latency.py`）
3. 在`__init__.py`中导出新的测试函数
4. 在`run_benchmarks.py`中添加新交易所的基准测试运行支持

## 许可证

MIT



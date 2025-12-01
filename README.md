# Alpha Dashboard

## 🎯 概览
本仓库提供用于 WorldQuant Brain 平台的因子挖掘与管理工具集合，涵盖脚本、服务与可视化仪表板。主工程位于 `WQOS/` 目录，包含核心挖掘流程、重构后的相关性检查器以及 Web 仪表板。

- 📖 子项目详解：`WQOS/README.md`
- 🧭 仪表板入口：`WQOS/digging-dashboard/`（`frontend/` React、`backend/` FastAPI）
- 🧪 核心脚本：`WQOS/src/`
- 🐳 Docker 使用：`WQOS/docker/README.md`

## 🚀 快速开始
- 🪟 Windows 启动指南：`WQOS/digging-dashboard/Windows启动指南.md`
- 🐳 使用 Docker 一键启动：`WQOS/docker/README.md`
- 📚 技术文档与重构指南：`WQOS/docs/`

## 🧩 功能模块地图
- 🔄 因子挖掘调度与执行：`WQOS/src/digging/`
- 🧠 相关性检查器（重构版）：`WQOS/src/correlation/`
- 🎛️ 模拟执行框架：`WQOS/src/lib/simulation/`
- 🗃️ 数据库与脚本工具：`WQOS/database/`、`WQOS/scripts/`
- 🔐 会话与记录管理：`WQOS/src/sessions/`

## 📚 文档索引
- 🧭 仓库总览（含详细结构与使用）：`WQOS/README.md`
- 📝 更新日志：`WQOS/docs/更新日志.md`
- 🔧 调度器重构指南：`WQOS/docs/DIGGING_SCHEDULER_REFACTOR_GUIDE.md`
- 🔎 相关性检查器重构指南：`WQOS/docs/CORRELATION_CHECKER_REFACTOR_GUIDE.md`

## 📁 目录结构
```
WQOS/
├── src/                          # 核心脚本（挖掘、相关性、模拟框架等）
├── digging-dashboard/            # Web 仪表板（前端/后端）
├── database/                     # 数据库与管理脚本
├── docker/                       # Docker 化使用
├── docs/                         # 技术文档与重构指南
└── README.md                     # 子项目说明
```

## 📄 许可与注意
- 许可证：`WQOS/LICENSE`
- ⚠️ 请勿以任何形式打包售卖本项目代码。

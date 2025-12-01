# Alpha Dashboard

## 简介
本仓库提供用于 WorldQuant Brain 平台的因子挖掘与管理工具集合，包括脚本、服务以及可视化仪表板。项目主体位于 `WQOS/` 目录，包含核心挖掘流程、重构后的相关性检查器以及 Web 仪表板。

## 子项目
- `WQOS/README.md` 项目详细说明、结构与文档索引
- `WQOS/digging-dashboard/` Web 仪表板（前后端）
  - `frontend/` React 前端
  - `backend/` FastAPI 后端
- `WQOS/src/` 因子挖掘与相关性检查的核心脚本
- `WQOS/docker/` Docker 化部署与使用说明

## 快速开始
- 查看 Windows 启动指南：`WQOS/digging-dashboard/Windows启动指南.md`
- 使用 Docker 启动：`WQOS/docker/README.md`
- 详细技术文档与重构指南：见 `WQOS/docs/`

## 目录导航
- 因子挖掘调度与执行：`WQOS/src/digging/`
- 相关性检查器（重构版）：`WQOS/src/correlation/`
- 模拟执行框架：`WQOS/src/lib/simulation/`
- 脚本工具与数据库管理：`WQOS/database/`、`WQOS/scripts/`

## 许可与注意
- 许可证：`WQOS/LICENSE`
- 请勿以任何形式打包售卖本项目代码。

## 指南
- 更新日志：`WQOS/docs/更新日志.md`
- 调度器重构：`WQOS/docs/DIGGING_SCHEDULER_REFACTOR_GUIDE.md`
- 相关性检查器重构：`WQOS/docs/CORRELATION_CHECKER_REFACTOR_GUIDE.md`


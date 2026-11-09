# Agent instructions

<!-- agent-docs:start -->
## Agent documentation

Follow [the documentation standard](.agents/skills/doc-maintenance/references/standard.md) for affected docs. Current behavior, procedures, decision rationale, and incident history each have one owner. Update only documents affected by the requested work; never infer historical rationale from code.

Before authoring or reviewing initialization output, explicitly open [.agents/skills/doc-maintenance/SKILL.md](.agents/skills/doc-maintenance/SKILL.md), [prose-standard](.agents/skills/prose-standard/SKILL.md), and [trim-session-residue](.agents/skills/trim-session-residue/SKILL.md), including their required references, even if absent from the skill catalog. For decisions also read [archive-agent-notes](.agents/skills/archive-agent-notes/SKILL.md). Copying is not loading. Complete the review in the same turn; do not wait for discovery refresh.

Project paths and checks: [.agents/docs-config.json](.agents/docs-config.json). Use the configured decision format and preserve existing instructions. Frozen archives are historical evidence, not current authority.
<!-- agent-docs:end -->

## 本项目维护

与用户交流及项目使用文档使用中文。分发材料以 `agent-docs/assets/project/` 为源；先修改源，再有选择地同步根目录 `.agents/` 副本，并运行 `python3 scripts/check_project.py`。修改正在使用的规则后，重新激活对应部分再复核。详见 [架构与归属](docs/architecture.md) 和 [开发流程](docs/development.md)。

历史试用目录、一次性提取脚本及含本机路径的验收记录仅作本地证据，排除在版本控制之外；维护性测试与可移植检查留在 `tests/` 和 `scripts/`。

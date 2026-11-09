# agent-docs

为现有项目建立可独立使用的 Agent 文档体系：保留已有规则和 ADR，明确文档归属，生成有源码依据的使用与维护说明，并管理决策记录的生命周期。项目内附带四套维护工作流；新复制的技能在当前会话中也必须显式读取并实际应用。

本仓库使用自己的技能维护文档。分发入口是 [agent-docs/SKILL.md](agent-docs/SKILL.md)，维护项目自身的入口是 [AGENTS.md](AGENTS.md)。

## 安装与使用

需要能够读取本地技能文件的 Agent；辅助脚本需要 Python 3.10 或更新版本，仅使用标准库。Git 用于仓库操作和可选的归档基线比较。

从仓库根目录运行下面的命令，将完整技能目录安装到 Codex 全局技能目录。目标已存在时会停止，避免覆盖自己的修改：

```sh
python3 - <<'PY'
import os
from pathlib import Path
import shutil

source = Path('agent-docs')
destination = Path(os.environ.get('CODEX_HOME', str(Path.home() / '.codex'))) / 'skills' / 'agent-docs'
if destination.exists():
    raise SystemExit(f'目标已存在，请先比较现有版本：{destination}')
destination.parent.mkdir(parents=True, exist_ok=True)
shutil.copytree(source, destination, ignore=shutil.ignore_patterns('__pycache__', '*.pyc'))
print(destination)
PY
```

在目标项目中向 Agent 发出请求：

> 使用 `$agent-docs` 初始化当前项目的 Agent 文档体系，沿用已有文档和约定，完成内容编写与验收。

也可以要求只梳理设计、维护指定变更涉及的文档、审查文档，或清理指定决策记录。尚未刷新技能列表时，提供安装目录中 `SKILL.md` 的实际路径，让 Agent 直接读取。

## 初始化产物

技能根据项目实际情况选择文档位置，优先沿用已有目录。常见产物包括根目录和文档目录的指令入口、`.agents/docs-config.json`、项目内维护技能、决策记录规则，以及基于现有代码编写或改进的 README、架构说明和开发指南。

已有 ADR 保留其命名、状态和内容；没有决策依据时只建立维护规则，不补造历史。单语言项目不增加翻译义务。复制材料后仍须由 Agent 读取规则、编写内容并完成语义复核，运行脚本本身不会自动生成可信的项目说明。

## 使用边界

辅助脚本会预检路径和文件冲突，拒绝通过符号链接写入共享位置。重复初始化保留已有配置和人工编辑；更新技能需要比较版本并有选择地同步。检查器能验证部分结构、链接文件目标和归档哈希，不能证明文字正确、Agent 已理解规则或 Markdown 锚点有效。

激活记录只证明规则内容已被输出；当前轮次的实际阅读和应用仍由 Agent 负责。具体流程和验收要求由 [初始化指南](agent-docs/references/initialize.md) 维护。

## 项目维护

- [架构与事实归属](docs/architecture.md)：分发源、项目副本、运行记录和检查范围。
- [开发与验证](docs/development.md)：修改、同步、测试和重新安装步骤。
- [自管理验收](docs/validation.md)：可复现检查与语义复核的边界。

## 来源与许可

文档管理和写作流程改编自 DeepSeek Harness，保留了完整命题、事实归属、会话独立可读性和决策保留标准。来源版本及文件摘要记录在 [upstream.json](agent-docs/assets/project/.agents/doc-tools/upstream.json)，使用时不需要上游仓库。代码与材料采用 [MIT 许可](LICENSE)，上游声明随分发包和项目副本保留。

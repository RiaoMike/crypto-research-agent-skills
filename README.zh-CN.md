# 密码学科研 Agent Skills

[English](README.md) · [快速开始](docs/getting-started.md) · [能力清单](docs/capabilities.md) · [架构](docs/architecture.md)

这是一套面向密码学、零知识证明和格密码研究的可移植 Agent Skills。项目包含一个技能创建元技能，以及覆盖研究构思、文献、novelty、形式化审查、参数、实验、论文写作、顶会写作风格和对抗性预审的十五个科研技能。

套件以密码学和安全顶会所需的研究纪律为目标，但**不保证**全局新颖性、证明正确性、协议安全、在未测试环境中的可复现性、论文录用、作者资格或自动投稿。任何技能都不得伪造引用、证明步骤、实验或审稿结论。

## 快速安装

需要 Git 和 Python 3.10 或更高版本；安装器仅使用 Python 标准库。

```bash
git clone https://github.com/RiaoMike/crypto-research-agent-skills.git
cd crypto-research-agent-skills
python scripts/validate.py skills
```

根据 Agent 安装全部技能：

```bash
# Codex
python scripts/install.py --target codex

# Claude Code
python scripts/install.py --target claude

# 通用 .agents/skills 目录
python scripts/install.py --target agents

# DeepSeek 或其他自定义 Harness
python scripts/install.py --target custom --dest /path/to/your/harness/skills
```

默认拒绝覆盖同名技能。先用 `--dry-run` 查看操作；确实需要替换时才使用 `--force`。可重复传入 `--skill NAME` 只安装指定技能。

## 从 Idea 开始科研

安装后开启新的 Agent 会话，输入：

```text
使用 crypto-research-pipeline，把下面的 ZKP/lattice idea 作为证据门控的科研项目推进。
先检索并验证 prior art，再讨论 novelty；严格区分定义、定理、证明、归约、协议安全声称、
参数、估计、测量和独立复现结果。如果证据否定原始 idea，就停止或提出 pivot。
维护 research-state ledger，给出下一项可证伪行动，只撰写证据支持的论文内容。

[在此填写 idea、已知材料和约束]
```

总控技能会调用适合的专项技能，并把未解决问题向后传播。伦理、披露、作者资格、最终声称和外部投稿必须由负责任的人类研究者确认。

## 技能组成

- **元技能：** `crypto-research-skill-creator`
- **总控：** `crypto-research-pipeline`
- **发现与综述：** `crypto-idea-evaluator`、`crypto-literature-search`、`crypto-paper-reader`、`crypto-related-work-synthesis`、`crypto-novelty-check`
- **理论与领域审查：** `crypto-theorem-review`、`zkp-security-review`、`lattice-parameter-audit`
- **证据与投稿准备：** `crypto-experiment-reproducibility`、`crypto-paper-writing`、`crypto-paper-review`
- **顶会写作风格：** `crypto-venue-paper-writing`、`ccs-writing-style`、`usenixsec-writing-style`

这三个写作风格技能针对两类相反缺陷：把必须凝练的地方（摘要、贡献列表）压缩，把必须详写的地方（技术概览、具体方案）展开——单靠字数上限无法发现这两类缺陷。每个阈值都是已发表顶会论文冻结语料的中位数或四分位数，以 `file:line` 标注并自带样本量与测量口径；随技能发布的两个计数工具负责按这些阈值实测稿件。

- **密码学与 LNCS**（CRYPTO、EUROCRYPT、ASIACRYPT）：`crypto-venue-paper-writing` 拥有该家族以及两族共用的语料校准规则。
- **安全四会**（ACM CCS、IEEE S&P、NDSS）：`ccs-writing-style` 拥有其语域与全族门控。
- **USENIX Security：** `usenixsec-writing-style` 只补充该会独有的检查，并按名称调用上述门控。

规则只写一次、其余位置引用，因此同一条规则句子不会出现在两个技能里。

完整输出能力和边界见[能力清单](docs/capabilities.md)。

## 不同 Agent 的使用说明

- [Codex](docs/codex.md)
- [Claude Code](docs/claude-code.md)
- [DeepSeek Harness](docs/deepseek-harness.md)
- [通用 Agent Skills 客户端](docs/generic-agent-skills.md)

核心目录遵循开放的 [Agent Skills 规范](https://agentskills.io/specification)。Claude Code 的个人和项目技能位置以其[官方技能文档](https://code.claude.com/docs/en/skills)为准。

## 验证

```bash
python -m unittest discover -s tests -v
python scripts/validate.py skills
python scripts/install.py --target custom --dest .install-smoke --dry-run
```

创建或重构科研技能时使用 `crypto-research-skill-creator`。每个技能都应具有明确的触发条件、范围、输入、成功标准、失败模式、工作流、输出契约、科研诚信约束和评测场景。

## 许可证

MIT，详见 [LICENSE](LICENSE)。


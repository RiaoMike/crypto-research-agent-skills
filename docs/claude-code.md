# Using the Skills with Claude Code

Claude Code documents personal skills at `~/.claude/skills/<skill-name>/SKILL.md` and project skills at `.claude/skills/<skill-name>/SKILL.md`. See Anthropic's [official skills guide](https://code.claude.com/docs/en/skills).

## Personal Installation

```bash
python scripts/install.py --target claude --dry-run
python scripts/install.py --target claude
```

If `~/.claude/skills` did not exist when Claude Code started, restart Claude Code after installation so it can watch the new top-level directory.

## Project Installation

To commit the skills with one research repository:

```bash
python scripts/install.py --target custom --dest .claude/skills
```

Review the copied files before committing them into that project. Personal skills override project skills with the same name in Claude Code's documented precedence.

## Invocation

Claude Code may load a skill automatically from its description, or you may invoke it directly:

```text
/crypto-paper-review
```

Follow with the manuscript location, intended venue, claimed contributions, and desired review depth. For orchestration:

```text
/crypto-research-pipeline
Treat this idea as a gated project. Verify literature and novelty claims, audit
formal/security/parameter evidence, and stop at human submission review.
```

The shared skill core does not add Claude-specific frontmatter such as `context: fork`; this preserves portability. A project may add Claude-specific wrappers separately without changing the canonical skill.


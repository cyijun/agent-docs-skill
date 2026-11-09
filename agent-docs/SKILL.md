---
name: agent-docs
description: Initialize, adapt, review, and maintain an existing project’s agent documentation system, with scoped instructions, source-backed guides, durable decision records, and portable writing workflows. Use for documentation governance or explicit project initialization, not ordinary unrelated code edits.
---

# Agent documentation

Establish a project-owned documentation system that another agent can use without this global skill or the upstream repository. Preserve existing instructions, ADR conventions, documentation routes, language, and user edits. Each fact has one owner; active decisions preserve rationale and tradeoffs; frozen history is never current authority.

## Choose the requested scope

- **Design:** read-only inventory and adaptation plan. Do not initialize files.
- **Initialize:** follow [initialization](references/initialize.md), including same-turn instruction loading and semantic acceptance.
- **Maintain:** read the project’s `.agents/docs-config.json`, applicable instructions, and the copied doc-maintenance/prose-standard workflows directly. Update only owners affected by the requested work.
- **Audit:** use those workflows to report evidence-backed findings; fix only when requested. Session-residue probes find candidates, not automatic deletions.
- **Archive:** read the project’s archive-agent-notes workflow and actual decision owners. Retention depends on future decision value, not age, length, or quotas. Respect frozen records.

Use the user’s directory or current project when unambiguous. Discover existing documentation before asking questions. Infer routine layout choices from evidence, and state material assumptions. Authorization to initialize includes scoped reversible integration; do not add a separate approval ceremony for every file. Ambiguous conflicting project policies need a narrow question after independent preparation.

## Same-turn loading is mandatory

Copying a skill does not load it into the current agent. Newly copied skills may be absent from the skill catalog until a later turn. Never rely on discovery refresh, invoke an unavailable skill by name, or postpone quality work to another turn.

For initialization, after copying and before writing project-specific prose, run the project’s `docs.py activate` for **each** of `docs`, `prose`, `trim`, and `archive`, and read all returned content. Run parts separately with sufficient output budgets; if truncated, open every omitted file directly. Apply the instructions to the current work immediately. Root/subtree instructions and sibling references must be read as well. The command records delivery hashes only; it cannot prove comprehension.

Before completion, re-read the generated documents against source evidence and apply the actual prose rules. Record specific applications of fact ownership, complete propositions, session-independent language, and preservation of existing content. A scaffold, a path list, an activation receipt, or a passing structural checker is insufficient. Complete `finish` as described in the initialization reference, and report semantic review and machine checks separately.

## Portable materials

The [project assets](assets/project/.agents/skills/doc-maintenance/SKILL.md) contain adapted documentation maintenance, [prose-standard](assets/project/.agents/skills/prose-standard/SKILL.md), [session-residue review](assets/project/.agents/skills/trim-session-residue/SKILL.md), and [archival](assets/project/.agents/skills/archive-agent-notes/SKILL.md). These are the canonical distributable workflows; copy them intact, then read the project copies. Do not create another paraphrased policy that competes with them.

The bootstrap helper uses Python 3.10+ and the standard library. It only copies policies and integrates entry points; the agent authors actual project content. If that runtime is unavailable, perform the same scoped copying and explicit reads with available file tools, record unrun mechanical checks, and do not claim machine-validated completion. Do not install a runtime without an appropriate task reason.

Package sources and adaptation notes are recorded in [upstream.json](assets/project/.agents/doc-tools/upstream.json); the accompanying [license](LICENSE-DeepSeek) must travel with redistributed material. These are attribution, not runtime dependencies. No upstream checkout, account, network access, or other global skill is required.

## Validation and reporting

Use the copied checker for managed-note structure, local target existence, explicit standing-doc budgets, and archive seals. Existing ADR grammar and semantic accuracy require project checks/review. CI can supply a trusted local Git baseline to detect rewriting both an archive and its manifest. Link fragments, renderer-specific routes, generated-reference freshness, translation semantics, and code examples require applicable project tooling; do not overstate the basic checker.

Report created/adapted owners, preserved conventions, loaded local workflows, operations actually run, and remaining evidence limits. Do not fabricate decision history, alternatives, test results, or successful operation claims. Do not create empty architecture inventories, speculative notes, mandatory translations, or a website pipeline.

# Initialize an existing project

## Inventory and adaptation

Read project instructions, README/navigation, manifests, launch/build/test entry points, relevant source, and existing decisions. Distinguish configured commands from observed execution. Keep package contracts local and cross-package explanations at their current owner. Retain ADR names, dates, and status conventions; do not derive historical motivation from current code. If the project has no relevant recorded decisions, create policy only, not fabricated decision examples.

Use existing docs/doc/documentation and ADR/decisions roots when suitable. The bootstrap auto-detects common paths; inspect the printed mapping and supply `--docs` or `--notes` for other conventions. Managed notes use stable English structural keys with prose in the project language. Native ADRs retain their original grammar. The tool does not translate or rewrite native decisions.

Default to the project’s existing prose language, or the user’s stated language for a new corpus. Agent-only policies are distributed in English; user-facing output uses the selected project language. Mixed-language projects can keep existing conventions; bilingual parity is not automatically introduced.

## Copy safely

Run the bundled helper, with the actual global skill location substituted:

```sh
python3 <skill-directory>/scripts/bootstrap.py --root <project-directory>
python3 <skill-directory>/scripts/bootstrap.py --root <project-directory> --apply
```

Optional flags: `--docs path`, `--notes path`, `--language zh` (or another project language). The first invocation is a read-only plan, not an approval requirement. After checking the mapping, apply within the user’s authorized scope.

The helper preflights destinations, refuses unrelated skill collisions and symlinked write targets, appends bounded integration blocks to existing instructions, and preserves existing content. Adapt a collision narrowly rather than overriding the whole file. Re-running with an existing configuration preserves material and reports next steps; it is not an upgrade or proof of completion. For upgrades, compare current files with the adapted source and preserve project changes; do not force-copy the package.

The result is **scaffold pending content**. Empty directories, copied rules, and a successful helper exit are not initialization success.

## Explicit activation before drafting

From the project root, execute and read all four parts separately:

```sh
python3 .agents/doc-tools/docs.py activate --root . --part docs
python3 .agents/doc-tools/docs.py activate --root . --part prose
python3 .agents/doc-tools/docs.py activate --root . --part trim
python3 .agents/doc-tools/docs.py activate --root . --part archive
```

Each part prints the copied files and required references in full. Choose an output budget large enough for the part, inspect the result, and read missing sections directly if the tool truncates. Do not redirect output to a file you never read. These reads are mandatory even when the newly copied skills are not registered in the current catalog. Announce their use briefly, then apply them in this turn. Do not spawn another agent merely to defer loading.

The local activation receipt is ignored working state. It detects missing or changed instruction deliveries but does not verify that a model read or understood them. If you modify a loaded policy, reactivate that part and re-review affected content. A prior-turn receipt does not satisfy the instruction to read in the current turn.

## Materialize project content

Produce or improve the smallest set of useful owners, usually the existing architecture/overview and development/usage documents. For a tiny project, one existing README with clear purpose, use, failure behavior, and maintenance sections is sufficient. Never create a parallel architecture page when an existing page owns it.

Ground prose in actual entry points and representative source paths. Explain user-visible outcomes, ownership/data flow, likely failures, limitations, and how to verify them at an appropriate level. Execute only safe, authorized operations; label unavailable or unrun checks. An operation documented as configured is different from one observed passing.

Preserve user instructions and maintained content. Apply complete-proposition preservation while trimming repetition. Keep current facts free of authoring-session references. Only record a historical decision when a durable source supplies its rationale, options, and date; otherwise retain the observed fact in a current reference and name the missing historical evidence if relevant.

Do not introduce arbitrary word ceilings. If a project wants budgets, use `budgets` in `.agents/docs-config.json`; the checker counts CJK characters plus non-CJK whitespace words. Extend `extra_docs` for relevant package READMEs outside the configured docs roots. Adjust `exclude` to actual ownership rather than assuming all vendor-named files are third-party.

## Review and complete

Read the complete materialized output, compare material claims with sources, and apply the copied workflows. Then run:

```sh
python3 .agents/doc-tools/docs.py check --root .
```

Run any additional existing project checks justified by the output. Avoid adding dependencies solely for initialization. If old unrelated documents fail checks, repair within authorized scope or report the remaining failure; do not silently exclude defects just to pass.

Create `.agents/doc-tools/.local/review.json` with this structure, populated with actual files and specific findings (the following is a schema illustration, not text to copy as evidence):

```json
{
  "outputs": [
    {"path": "docs/development.md", "sources": ["package.json", "src/main.ts"]}
  ],
  "reviews": [
    {"principle": "fact-ownership", "path": "docs/development.md", "finding": "Describe a specific ownership decision applied in this document."},
    {"principle": "complete-propositions", "path": "docs/development.md", "finding": "Identify a concrete condition, failure, ordering or ownership guarantee preserved."},
    {"principle": "session-independent", "path": "docs/development.md", "finding": "Identify how the text is independently understandable and its references resolve."},
    {"principle": "existing-content-preserved", "path": "docs/development.md", "finding": "Identify original instructions or content retained and the scope of the edits."}
  ],
  "verification": ["Exact operation and observed outcome, or an explicit unverified claim and reason."],
  "native_decision_review": "Required only for native ADRs: explain preserved conventions and the actual semantic review."
}
```

Every output requires file evidence. The validator rejects copied policies as project-specific output, absent review categories, missing/stale instruction deliveries, missing source files, unfinished scaffolds, and structural defects. It cannot verify whether a finding is true; the author/reviewer must do that.

```sh
python3 .agents/doc-tools/docs.py finish --root . --report .agents/doc-tools/.local/review.json
```

Completion records are ignored local working state, not a new authoritative document inventory. Final reporting distinguishes substantive output, semantic review, machine checks, and any unverified operation. A clean rerun must preserve human edits and existing ADRs.

## Archive and baseline checks

Archival is a separate scoped action. After semantic classification and authorized moves, `seal` appends new hashes only after checking all existing seals. Archived bodies and outbound links are not modernized. For native ADRs, establish their equivalent archival metadata through project policy before sealing.

```sh
python3 .agents/doc-tools/docs.py seal --root .
python3 .agents/doc-tools/docs.py check --root . --baseline <trusted-local-git-revision>
```

The baseline should be supplied by the project’s CI or review context. Local hash checks alone cannot detect a coordinated rewrite of content and its manifest. No CI workflow is installed automatically.

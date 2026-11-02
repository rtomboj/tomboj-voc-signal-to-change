# Instructions for coding agents

## Project context

Tomboj VOC Signal-to-Change is maintained by Rachel Wilde / Tomboj. It contains portable AI-guided VOC skills, documentation, synthetic examples, validation scripts, and classification evaluations. Follow the existing structure and keep user-facing guidance clear and practical.

## Scope and collaboration

- Make only the changes requested. Inspect the working tree first and preserve existing user changes.
- Explain material findings, changes, and validation results. Distinguish checks actually run from recommendations.
- Keep synthetic examples clearly labeled. Do not describe saved model runs as proof of production readiness or a general model ranking.

## Protected evaluation files

- Do not edit `evals/classification/answer_key.csv`, `evals/classification/RUBRIC.md`, or files under `evals/classification/runs/` without Rachel's explicit approval for those changes.
- Report suspected label or rubric problems as suggestions. If a task requires a protected change, stop and ask before making it.
- Publish label changes through a new key version; preserve prior evaluation results.

## Validation

Use Python 3.10+ from the repository root. On Windows, use `python`; use `python3` or `py -3` if that is the available Python 3 command.

For repository changes, run:

```text
python scripts/check_repository.py
python scripts/validate_loop_registers.py examples/closed-loop/registers
```

For changes affecting classification behavior, inputs, or scoring instructions, also run:

```text
python evals/classification/score.py evals/classification/runs/2026-11-02_haiku_rubric-v1.0.csv evals/classification/runs/2026-11-02_sonnet_rubric-v1.0.csv
```

The saved v1.0 runs should score Haiku 25/25 and Sonnet 24/25, with 8/8 escalations caught for both. Sonnet's only mismatch should be E07's `operational_impact` (expected `High`, predicted `Medium`). A successful scorer exit does not mean every label matched; inspect the output.

Stop and report failed checks or unexpected saved-run scores before publishing changes. Run other existing checks when relevant to the requested change. Do not add tests that merely repeat a trivial documentation edit.

## Git and review

- Never push directly to `main`, force-push, or delete branches.
- When asked to publish changes, use a separate branch and open a pull request into `main` with a concrete description and validation results.
- Do not merge pull requests; Rachel reviews and merges them.
- Do not rewrite existing commit history to add attribution.

## Attribution and provenance

- Preserve Rachel Wilde / Tomboj's authorship and the repository's licensing notices.
- Accurately acknowledge AI assistance in new commits and pull request descriptions when creating them. For Codex-assisted commits, include `Co-authored-by: Codex <noreply@openai.com>` in the commit message.
- Credit only tools and contributors that actually assisted. Do not imply their endorsement or independent human review.
- Follow `ATTRIBUTIONS.md` when adding copied, adapted, or consulted third-party material.

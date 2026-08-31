# Contributing

Contributions that improve trigger precision, cryptographic rigor, portability, validation, or evaluation coverage are welcome.

## Before Opening a Pull Request

1. Use `crypto-research-skill-creator` for a new or materially changed research skill.
2. Add or revise evaluation scenarios before changing skill behavior.
3. Keep `SKILL.md` focused; move detailed material into `references/` and deterministic work into `scripts/`.
4. Verify every citation and distinguish reported, derived, estimated, measured, and independently reproduced evidence.
5. Do not claim global novelty, proof correctness, security, or reproducibility without the corresponding evidence boundary.
6. Run:

```bash
python -m unittest discover -s tests -v
python scripts/validate.py skills
```

## Pull Request Content

Explain the triggering problem, the failure or gap being addressed, the tests or evaluation scenarios used, and any harness-specific limitations. Never include private manuscripts, unpublished third-party data, credentials, or personally identifying research records without authorization.


# Dependency Compass

A Python dependency-manifest hygiene checker. Detect duplicate package names, missing exact versions, invalid package names and non-pinned constraints. Runs without external dependencies.

## Usage

```bash
python app.py examples/manifest.json
python -m unittest discover -s tests -v
```

Input is a JSON object with a `packages` array of `{"name":"requests","version":"2.32.0"}` records. Output is JSON with `healthy`, `packages`, and `issues`. Exit codes: 0 clean, 1 issues, 2 invalid input.

This tool checks manifest hygiene, **not** security advisories, package authenticity, transitive dependencies, or full PEP 440 semantics.

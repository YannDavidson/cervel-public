# Error Envelope Fixture Expectations

- `valid-minimal.json` — valid minimal `0.1-draft` Error Envelope with required `version` and non-empty `code`.
- `invalid-missing-code.json` — invalid because required `code` is absent.
- `invalid-empty-code.json` — invalid because `code` must be a non-empty string.

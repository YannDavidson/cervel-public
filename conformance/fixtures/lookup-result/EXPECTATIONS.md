# Lookup Result Fixture Expectations

- `valid-minimal.json` — valid minimal `0.1-draft` Lookup Result containing a valid minimal Knowledge Reference.
- `invalid-missing-items.json` — invalid because required `items` is absent.
- `invalid-empty-reference.json` — invalid because `{}` does not satisfy the incorporated Knowledge Reference contract; required `version` and `id` are absent.

The empty-reference fixture is specifically intended to guard the schema-composition boundary between Lookup Result and Knowledge Reference.

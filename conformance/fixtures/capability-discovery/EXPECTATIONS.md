# Capability Discovery Fixture Expectations

- `valid-minimal.json` — valid minimal `0.1-draft` Capability Discovery document with an empty public contract list.
- `valid-declared-contract.json` — valid document declaring one public contract/version pair.
- `invalid-missing-contracts.json` — invalid because required `contracts` is absent.
- `invalid-empty-name.json` — invalid because each declared contract `name` must be a non-empty string.

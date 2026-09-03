# Developer Certificate of Origin Sign-off Policy

CERVEL Public uses a Developer Certificate of Origin (DCO) style sign-off for external contributions.

By adding a `Signed-off-by` trailer to a commit, the contributor certifies that they have the right to submit the contribution for inclusion under the repository's applicable license and contribution terms, and that the contribution is not knowingly derived from material they are not authorized to disclose or contribute.

Use Git's sign-off option when creating commits:

```bash
git commit -s -m "Describe the change"
```

The resulting commit message should contain a trailer in this form:

```text
Signed-off-by: Contributor Name <contributor@example.com>
```

The name and email should identify the contributor who is making the certification. A cryptographic commit signature is separate from DCO sign-off and does not replace the `Signed-off-by` trailer.

## What the sign-off means for this repository

The contributor certifies that, to the best of their knowledge:

1. they created the contribution, or otherwise have the right to submit it under the applicable open-source terms;
2. any third-party material included in the contribution is compatible with those terms and is properly identified where required;
3. they are not knowingly publishing confidential, proprietary, embargoed, security-sensitive, personal, customer, or non-public CERVEL information without authorization;
4. they understand that a contribution accepted into this public repository becomes publicly accessible and may be redistributed under the repository license;
5. the sign-off does not grant access to, disclose, or change the status of non-public CERVEL technology.

## Checking strategy

`governance/check_dco.py` provides the repository-owned parser used to detect a valid `Signed-off-by: Name <email>` trailer in commit messages. Its behavior is covered by unit tests in `governance/tests/`.

This foundation PR intentionally does **not** enforce DCO against its own bootstrap commits. The next enforcement rollout can wire the tested checker to pull-request commit metadata and make that status check required for external contribution branches. Until automated enforcement is enabled, maintainers should require sign-off during review for external contributions.

This policy supplements, and does not replace, `LICENSE`, `LICENSING.md`, `CONTRIBUTING.md`, `SECURITY.md`, or the repository's disclosure-review requirements.

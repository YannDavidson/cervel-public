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

## Automated checking

`governance/check_dco.py` provides the repository-owned parser used to detect a valid `Signed-off-by: Name <email>` trailer in commit messages. `governance/check_pr_dco.py` obtains the commit metadata for the active pull request and requires every commit in that pull request to contain a valid sign-off. Both behaviors are covered by deterministic tests in `governance/tests/`.

The dedicated `DCO sign-off` status check runs from `.github/workflows/dco.yml` using the `pull_request_target` event. The workflow checks out only the trusted base revision and reads pull-request commit metadata through the GitHub API; it does not check out or execute contributor code. Its token is explicitly limited to `contents: read` and `pull-requests: read`.

The gate fails closed if commit metadata cannot be retrieved completely and rejects pull requests above GitHub's 250-commit pull-request commit limit. Contributors should split unusually large changes into smaller pull requests.

Because the workflow is evaluated from the trusted base branch, a pull request cannot weaken its own required DCO status by modifying `.github/workflows/dco.yml` or the governance checker in that same pull request. Changes to the enforcement implementation take effect only after they are separately reviewed and merged into the base branch.

This status is designed to be suitable for branch-protection or ruleset enforcement as a required check. Repository protection configuration is a separate administrative control from the workflow itself.

This policy supplements, and does not replace, `LICENSE`, `LICENSING.md`, `CONTRIBUTING.md`, `SECURITY.md`, or the repository's disclosure-review requirements.

# Releasing aiofastnet

This document describes the maintainer workflow for publishing aiofastnet to PyPI and creating the corresponding GitHub Release.

## Set release version and prepare changelog

1. Create a branch `release/1.2.0`.
2. Ensure every user-visible change has a news fragment in `docs/changelog.d/`. Fragment names use the form
   `<issue-or-pr>.<type>.md`; the available types are defined in `towncrier.toml`.
3. Choose the new version (1.2.0) and update `__version__` in `aiofastnet/_version.py`.
4. Install Towncrier and preview the release notes:

   ```console
   $ python -m pip install towncrier
   $ python -m towncrier build --draft
   ```

   Correct the fragments if the rendered notes need changes. Do not edit the generated section in `CHANGELOG.md` by hand.
5. Finalize the changelog using the same version:

   ```console
   $ python -m towncrier build --yes
   ```

   The command adds a new `## 1.2.0` section to `CHANGELOG.md` and removes the consumed fragments.
6. Review and commit the version, changelog, and removed fragments. Create a PR, wait for its required checks to pass, and merge it.

## Publish the release

Create an annotated tag from the merged release commit and push it:

```console
$ git switch master
$ git pull --ff-only
$ git tag -a v1.2.0 -m "Release 1.2.0"
$ git push origin v1.2.0
```

The tag version must match both `aiofastnet/_version.py` and the finalized heading in `CHANGELOG.md`.

Pushing a `v*` tag starts `.github/workflows/release.yml`. The workflow:

1. Extracts the Towncrier-generated version section from `CHANGELOG.md`. Missing or empty notes prevent publishing.
2. Builds the source distribution and platform wheels.
3. Publishes all distributions to PyPI through the `pypi` environment and Trusted Publishing.
4. Signs the distributions with Sigstore after PyPI publishing succeeds.
5. Creates the GitHub Release.
6. Uses the extracted changelog section verbatim as the GitHub Release description and attaches all distributions and Sigstore bundles to the
   release.

PyPI generates Sigstore-backed attestations for the published distributions automatically.

## Verify the release

After the workflow completes:

- Confirm that the expected version and distributions are present on PyPI.
- Confirm that the GitHub Release contains the same notes as `CHANGELOG.md` and includes the source distribution, all wheels, and their Sigstore
  bundles.
- Install the new version in a clean environment and verify that `aiofastnet.__version__` reports the expected value.

## Failed releases

- For a transient workflow failure, rerun the failed job.
- If PyPI publishing succeeded but GitHub Release creation failed, rerun the `github-release` job. Do not create a new tag.
- If any distribution reached PyPI, do not move or reuse the version tag. Correct the problem in a new release because published PyPI files are
  immutable.
- If publishing did not begin and the release commit itself is wrong, correct the release commit before publishing. Avoid changing a tag that users
  may already have fetched.

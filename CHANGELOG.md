# Changelog

All notable changes to this project are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/).
Versioning: `v0.1.0` pilot · `v0.9.0` release candidate · `v1.0.0` public release.

## [Unreleased]

### Added
- Initial repository structure (Phase 0)
- Metadata schema and validation script
- Issue and pull request templates
- Contribution workflow documentation
- `note` field on chunk records (`docs/schema.md` section 2). Records why a chunk was flagged `rejected`, or why its `token_count` sits outside the 180-320 range. Section 7.4 requires a documented reason for token count deviations, and this field is where that reason lives.
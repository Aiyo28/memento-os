# Security Policy

## Scope

Memento OS is a Claude Code plugin that reads and writes markdown files. It does not:
- Execute arbitrary code
- Make network requests
- Access credentials or secrets
- Modify system files outside the configured memory path

## Reporting

If you discover a security issue, please report it via [GitHub Security Advisories](https://github.com/ayalnogovitsyn/memento-os/security/advisories/new).

Do not open public issues for security vulnerabilities.

## Threat Model

The primary risk vectors for a memory plugin:
- **Prompt injection via stored artifacts** — a malicious artifact could influence future sessions. Mitigation: artifacts are user-confirmed before storage (except in `--compact` mode where auto-defaults to `settled` priority).
- **Sensitive data in artifacts** — decisions about API keys, credentials, or secrets could be stored as `[D]` artifacts. Mitigation: the Stop hook's prompt instructs not to store secrets. Users should review artifacts before committing to version control.

## Supported Versions

| Version | Supported |
|---------|-----------|
| 0.4.x | Yes |
| < 0.4 | No |

# Security Rule Catalogue
## Secure Code Review Framework

### 1. Purpose
This catalogue documents the security checks supported by the Secure Code Review Framework. It maps detected vulnerabilities to relevant CWE classifications, OWASP Top 10 categories and secure-coding practices.

### 2. Security Rule Catalogue

| No. | Vulnerability | Detection Tool / Rule | CWE | OWASP Top 10 (2021) | Status |
|---|---|---|---|---|---|
| 1 | SQL Injection | Semgrep custom rule – sql-injection.yaml | CWE-89 | A03 – Injection | Custom rule implemented |
| 2 | Weak MD5 Hashing | Semgrep – weak-hash-md5 | CWE-328 | A02 – Cryptographic Failures | Custom rule implemented |
| 3 | Weak SHA-1 Hashing | Semgrep – weak-hash-sha1 | CWE-328 | A02 – Cryptographic Failures | Custom rule implemented |
| 4 | Command Injection | Semgrep built-in rules and Bandit B602 | CWE-78 | A03 – Injection | Built-in detection tested |
| 5 | Hardcoded Credentials / Secret Exposure | Gitleaks | CWE-798 (context-dependent) | A07 – Identification and Authentication Failures | Scanner integrated |
| 6 | Vulnerable Dependencies | OWASP Dependency-Check | Depends on associated CVE | A06 – Vulnerable and Outdated Components | Scanner integrated |
| 7 | Path Traversal | Remediation knowledge base | CWE-22 | A01 – Broken Access Control | Guidance documented |

### 3. Secure Coding and CERT Alignment

The framework promotes the following secure-coding practices:

- Use parameterized queries instead of dynamically constructed SQL.
- Avoid weak hashing algorithms such as MD5 and SHA-1 for security-sensitive purposes.
- Use secure password-hashing algorithms such as Argon2id, scrypt or bcrypt.
- Avoid shell execution with untrusted input.
- Never store API keys, passwords or credentials directly in source code.
- Regularly identify and update vulnerable third-party dependencies.
- Validate file paths and restrict access to authorized directories.

These practices align with relevant CERT secure-coding principles. They are practice-level mappings, not claims of exact CERT rule-ID coverage.

### 4. Remediation Process

1. Identify the security finding from the scanner output.
2. Review the associated CWE and OWASP category.
3. Examine the affected source code or dependency.
4. Apply the recommended secure-coding practice.
5. Commit the corrected code to a separate branch.
6. Create a pull request.
7. Run the security workflow again.
8. Merge only after the required checks pass.

### 5. Framework Coverage

**Currently implemented:**
- Semgrep static analysis.
- Bandit Python security scanning.
- Gitleaks secret detection.
- OWASP Dependency-Check.
- Custom SQL injection and weak cryptography rules.
- GitHub Actions pull-request security checks.

**Documented or planned enhancements:**
- Expanded SANS/CWE and CERT rule coverage.
- Additional language-specific scanning rules.
- Centralized security dashboards.
- Extended vulnerability tracking and compliance reporting.

### 6. Important Note

The presence of a vulnerability in this catalogue does not necessarily mean an active automated detection rule exists for it. The status column distinguishes implemented scanner coverage from documented remediation guidance.

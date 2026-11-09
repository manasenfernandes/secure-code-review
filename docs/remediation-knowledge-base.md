# Secure Coding Remediation Knowledge Base

## 1. Purpose

This knowledge base provides developers with vulnerability
identification, severity classification, standards mapping,
remediation steps and secure coding examples.

## 2. Command Injection

- Severity: High
- CWE: CWE-78
- OWASP: A03:2021 – Injection
- Detection: Bandit / Semgrep

### Vulnerable code

    subprocess.call(command, shell=True)

### Remediation

1. Avoid executing operating-system commands when unnecessary.
2. Never pass untrusted input directly to a shell.
3. Use an argument list instead of a shell command string.
4. Set shell=False.
5. Validate input against an allowlist.

### Secure example

    subprocess.run(["ls", "-l"], shell=False, check=True)

---

## 3. SQL Injection

- Severity: High
- CWE: CWE-89
- OWASP: A03:2021 – Injection
- Detection: Custom Semgrep rules

### Vulnerable code

    query = "SELECT * FROM users WHERE name = '" + username + "'"

### Remediation

1. Avoid constructing SQL queries through string concatenation.
2. Use parameterized queries.
3. Validate user input.
4. Apply least-privilege database permissions.

### Secure example

    cursor.execute(
        "SELECT * FROM users WHERE name = ?",
        (username,)
    )

Note: Placeholder syntax depends on the database driver.

---

## 4. Weak Cryptographic Hashing

- Severity: High
- CWE: CWE-328
- OWASP: A02:2021 – Cryptographic Failures
- Detection: Semgrep built-in and custom rules

### Vulnerable code

    hashlib.md5(password.encode())
    hashlib.sha1(password.encode())

### Remediation

1. Avoid MD5 and SHA-1 for security-sensitive hashing.
2. Use a dedicated password hashing algorithm.
3. Prefer Argon2id, scrypt or bcrypt.
4. Use unique salts.
5. Follow current password-storage recommendations.

### Secure example

    import hashlib
    import os

    salt = os.urandom(16)

    password_hash = hashlib.scrypt(
        b"example-password",
        salt=salt,
        n=2**14,
        r=8,
        p=1
    )

Production parameters must be reviewed and tuned.

---

## 5. Hardcoded Credentials and Secrets

- Severity: Critical
- CWE: CWE-798
- OWASP: A07:2021 – Identification and Authentication Failures
- Detection: Gitleaks

### Vulnerable code

    API_KEY = "hardcoded-secret-value"

### Remediation

1. Never store credentials directly in source code.
2. Use environment variables or an approved secrets manager.
3. Rotate exposed credentials immediately.
4. Restrict secret access.
5. Scan repository history for accidentally committed secrets.

### Secure example

    import os

    API_KEY = os.environ.get("API_KEY")

    if not API_KEY:
        raise RuntimeError("API_KEY is not configured")

---

## 6. Vulnerable Dependencies

- Severity: Depends on vulnerability and exploitability
- CWE: CWE-1035 / relevant vulnerability-specific CWE
- OWASP: A06:2021 – Vulnerable and Outdated Components
- Detection: OWASP Dependency-Check

### Remediation

1. Review the dependency vulnerability report.
2. Identify the affected package and version.
3. Check the CVE and CVSS information.
4. Upgrade to a patched version.
5. Test application compatibility.
6. Rescan after updating dependencies.

---

## 7. Path Traversal

- Severity: High
- CWE: CWE-22
- OWASP: A01:2021 – Broken Access Control

### Remediation

1. Avoid trusting user-supplied file paths.
2. Restrict file access to an approved directory.
3. Resolve and validate canonical paths.
4. Reject paths that escape the permitted directory.
5. Apply least-privilege file permissions.

---

## 8. Security Standards Mapping

| Vulnerability | CWE | OWASP |
|---|---|---|
| Command Injection | CWE-78 | A03 |
| SQL Injection | CWE-89 | A03 |
| Weak Hashing | CWE-328 | A02 |
| Hardcoded Credentials | CWE-798 | A07 |
| Vulnerable Dependencies | Relevant CWE | A06 |
| Path Traversal | CWE-22 | A01 |

### SANS / CWE alignment

The knowledge base uses Common Weakness Enumeration identifiers
to classify weaknesses and support alignment with SANS CWE
Top 25 guidance.

### CERT secure coding alignment

The remediation principles promote:

- Input validation.
- Safe API usage.
- Secure cryptographic practices.
- Proper error handling.
- Secure resource and file handling.
- Protection of credentials.
- Dependency maintenance.

Formal CERT rule compliance must be validated against the
specific programming language and applicable CERT standard.

---

## 9. Remediation Workflow

1. Scanner identifies a vulnerability.
2. Finding is classified by severity.
3. CWE and OWASP mappings are identified.
4. Developer reviews remediation guidance.
5. Developer implements the secure fix.
6. Code is submitted through a pull request.
7. Automated security scans run again.
8. Reviewer verifies the fix before merging.

## 10. Important Note

This knowledge base is intended to support secure coding
and vulnerability remediation. It complements automated
security scanners and does not replace manual security review.

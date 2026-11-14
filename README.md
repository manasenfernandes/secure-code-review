# Secure Code Review Framework

An automated security code review framework designed to identify vulnerabilities, detect insecure coding practices, and improve software security through integrated static analysis, secret detection, and dependency scanning tools.

## 1. Project Overview

The Secure Code Review Framework integrates multiple security tools into a GitHub Actions workflow to automate security assessments during software development.

The framework helps developers identify potential security weaknesses, receive actionable security feedback, and follow secure coding practices before changes are merged into the main branch.

The project focuses on Python application security and demonstrates how automated security testing can be integrated into a GitHub-based development workflow.

## 2. Project Objectives

- Develop a modular framework for automated code security reviews.
- Integrate Static Application Security Testing (SAST) tools.
- Identify common vulnerabilities using OWASP security guidelines.
- Implement custom security rules for additional vulnerability detection.
- Detect accidentally committed secrets and credentials.
- Scan Python dependencies for known vulnerabilities.
- Integrate automated security checks with GitHub Pull Requests.
- Demonstrate vulnerability detection and remediation through sample applications.
- Explore authentication, authorization, and application security controls.

## 3. Security Tools Integrated

| Tool | Purpose |
|---|---|
| Semgrep | Static code analysis and detection of insecure coding practices. |
| Bandit | Identifies common security issues in Python code. |
| Gitleaks | Detects exposed secrets and sensitive information in repositories. |
| OWASP Dependency-Check | Identifies known vulnerabilities in third-party dependencies. |
| pip-audit | Audits Python dependencies against known vulnerability databases. |

### Semgrep

Used for static application security testing with OWASP Top 10 rules and custom security rules.

### Bandit

Scans Python source code for common security issues, including potentially unsafe functions and insecure coding patterns.

### Gitleaks

Scans repository changes and Git history for accidentally committed secrets and credentials.

### OWASP Dependency-Check

Analyzes project dependencies against known vulnerability databases to identify potentially vulnerable components.

### pip-audit

Checks installed and declared Python dependencies against known security advisories and identifies packages that require updates.

## 4. Custom Security Rules

The framework includes custom Semgrep rules under the `rules/` directory.

Implemented rules include:

- **SQL Injection Detection:** Identifies potentially unsafe SQL query construction using string concatenation.
- **Weak Cryptography Detection:** Identifies the use of weak cryptographic algorithms and insecure practices.

These rules supplement the standard security rules used by Semgrep.

## 5. Project Architecture and Structure

The framework follows a modular architecture consisting of:

1. **Source Code:** Python sample applications containing vulnerable and corrected coding examples.
2. **Custom Security Rules:** Semgrep rules for identifying additional security weaknesses.
3. **Security Scanning Pipeline:** GitHub Actions workflow coordinating automated security tools.
4. **Dependency Auditing:** Tools that identify known vulnerabilities in third-party packages.
5. **Authentication and Authorization:** Flask-based authentication and RBAC implementation currently under verification.
6. **Testing and Evaluation:** Automated tests and planned performance measurements.

### Repository Structure

```text
secure-code-review/
│
├── .github/
│   └── workflows/
│       └── security-scan.yml
│
├── docs/
│   └── Security documentation
│
├── rules/
│   ├── sql-injection.yaml
│   └── weak-cryptography.yaml
│
├── sample-app/
│   ├── app.py
│   ├── app_fixed.py
│   ├── bad_example.py
│   └── requirements.txt
│
├── .gitignore
├── compose.yaml
└── README.md
```

Additional authentication and testing files are being integrated through PR #28. The repository structure should be updated after that implementation is merged.

## 6. Automated Security Workflow

The framework uses GitHub Actions to automate security scanning.

The workflow is configured to execute when:

- A Pull Request is created or updated.
- Changes are pushed to the `main` branch.

The security workflow includes the following checks:

1. **Semgrep:** Scans source code using OWASP Top 10 and custom security rules.
2. **Bandit:** Checks Python files for common security vulnerabilities.
3. **Gitleaks:** Checks for exposed secrets and credentials.
4. **OWASP Dependency-Check:** Scans third-party dependencies against known vulnerability databases.
5. **pip-audit:** Audits Python dependencies for known security vulnerabilities.
6. **Authentication and RBAC Tests:** Validates authentication-related functionality through automated tests as part of the authentication implementation.

Each security tool provides an individual result in GitHub Actions, allowing developers to investigate and remediate identified issues before merging changes.

## 7. Vulnerability Detection and Remediation

The sample application demonstrates common insecure coding practices and their corresponding remediation approaches.

### 7.1 SQL Injection

**Vulnerable approach:**

Building SQL queries through string concatenation can expose applications to SQL injection attacks.

**Secure approach:**

Using parameterized SQL queries helps prevent untrusted input from being interpreted as executable SQL.

Example:

```python
conn.execute(
    "SELECT * FROM users WHERE name = ?",
    (name,)
)
```

### 7.2 Command Injection

**Vulnerable approach:**

Executing user-controlled commands through shell execution can introduce command injection vulnerabilities.

**Secure approach:**

Using argument lists and avoiding unnecessary shell execution reduces this risk.

### 7.3 Hardcoded Secrets

**Vulnerable approach:**

Storing API keys or credentials directly in source code can expose sensitive information.

**Secure approach:**

Use environment variables or an appropriate secrets-management solution to manage credentials.

### 7.4 Weak Cryptography

**Vulnerable approach:**

Using weak hashing algorithms such as MD5 for security-sensitive purposes can expose applications to cryptographic attacks.

**Secure approach:**

Use appropriate modern cryptographic algorithms. For password storage, use dedicated password-hashing functions such as Werkzeug's password hashing utilities rather than general-purpose hashes.

The project demonstrates how insecure coding patterns can be identified through automated scanning and how developers can apply safer alternatives.

## 8. Authentication and Access Control

Authentication and Role-Based Access Control (RBAC) are being integrated into the Flask application.

The implementation includes:

- User registration and login.
- Password hashing.
- Session-based authentication.
- Role-based access restrictions.
- Administrative access controls.
- CSRF protection.
- Login attempt tracking and rate limiting.
- Secure session cookie configuration.

These controls are currently part of PR #28 and will be considered fully integrated after the pull request is merged and its checks are verified.

## 9. How to Use the Framework

1. Clone or fork the repository.
2. Open the repository in GitHub.
3. Review the sample application and custom security rules.
4. Create a new branch for code changes.
5. Submit a Pull Request targeting the `main` branch.
6. GitHub Actions automatically initiates the configured security scans.
7. Review the results of each security tool.
8. Investigate and remediate identified vulnerabilities.
9. Submit the corrected changes for another security assessment.

**Note:** OWASP Dependency-Check may require an NVD API key for vulnerability database access. Configure it as a GitHub Actions repository secret named `NVD_API_KEY` if required by the workflow configuration.

## 10. Current Implementation Status

| Component | Status |
|---|---|
| GitHub Actions integration | Implemented |
| Semgrep static analysis | Implemented |
| Bandit Python security scanning | Implemented |
| Gitleaks secret detection | Implemented |
| OWASP Dependency-Check integration | Implemented |
| pip-audit dependency scanning | Integrated through merged PR #23 |
| Custom SQL injection rule | Implemented and tested |
| Custom weak cryptography rule | Implemented |
| Vulnerability remediation demonstration | Implemented |
| Authentication and RBAC | In progress – PR #28 |
| CSRF protection | In progress – PR #28 |
| Login rate limiting | In progress – PR #28 |
| Automated authentication tests | In progress – PR #28 |
| Performance evaluation | Pending |
| Centralized security dashboard | Future enhancement |
| Compliance reporting enhancements | Future enhancement |

## 11. Limitations and Future Enhancements

Potential future improvements include:

- Developing a centralized security reporting dashboard.
- Extending support to additional programming languages.
- Integrating additional security standards such as SANS and CERT guidelines.
- Improving vulnerability remediation recommendations.
- Optimizing dependency scanning performance through caching.
- Introducing enhanced compliance tracking and reporting.
- Expanding automated security testing and performance evaluation.

## 12. Technologies Used

- Python
- Flask
- SQLite
- Git and GitHub
- GitHub Actions
- Docker
- Semgrep
- Bandit
- Gitleaks
- OWASP Dependency-Check
- pip-audit
- YAML
- Pytest

## 13. Disclaimer

This project is developed for educational and demonstration purposes as part of a cybersecurity project.

Automated security scanning helps identify potential vulnerabilities but does not guarantee that an application is completely secure. Manual security reviews, additional testing, and appropriate security practices are recommended.

---

**Project:** Implementing a Secure Framework for a Code Review Tool  
**Repository:** `manasenfernandes/secure-code-review`

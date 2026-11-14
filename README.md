# Secure Code Review Framework

An automated security code review framework designed to identify vulnerabilities, detect insecure coding practices, and improve software security through integrated static analysis and dependency scanning tools.

## 1. Project Overview

The Secure Code Review Framework integrates multiple security tools into a GitHub Actions workflow to automate code security assessments.

The framework helps developers identify potential security weaknesses during the development process, receive actionable security feedback, and follow secure coding practices.

The project focuses on Python application security and demonstrates how automated security checks can be integrated into a GitHub-based development workflow.

## 2. Project Objectives

- Develop a modular framework for automated code security reviews.
- Integrate static application security testing (SAST) tools.
- Identify common vulnerabilities based on OWASP security guidelines.
- Implement custom security rules for additional vulnerability detection.
- Scan Python dependencies for known vulnerabilities.
- Integrate automated security checks with GitHub Pull Requests.
- Demonstrate vulnerability detection and remediation through sample applications.

## 3. Security Tools Integrated

| Tool | Purpose |
|---|---|
| Semgrep | Static code analysis and detection of insecure coding practices. |
| Bandit | Identifies common security issues in Python code. |
| Gitleaks | Detects exposed secrets and sensitive information in Git repositories. |
| OWASP Dependency-Check | Identifies known vulnerabilities in third-party dependencies. |

### Semgrep
Used for static analysis with OWASP Top 10 rules and custom security rules.

### Bandit
Scans Python source code for common security issues, including potentially unsafe functions and insecure coding patterns.

### Gitleaks
Scans repository history and changes for accidentally committed secrets and credentials.

### OWASP Dependency-Check
Analyzes project dependencies against known vulnerability databases to identify potentially vulnerable components.

## 4. Custom Security Rules

The framework includes custom Semgrep rules under the `rules/` directory.

Currently implemented rules include:

- **SQL Injection Detection:** Identifies potentially unsafe SQL query construction using string concatenation.
- **Weak Cryptography Detection:** Identifies the use of weak or insecure cryptographic practices.

These rules supplement the standard security rules used by Semgrep.

## 5. Project Structure

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

## 6. Automated Security Workflow

The framework uses GitHub Actions to automate security scanning.

The workflow is configured to execute when:

- A Pull Request is created or updated.
- Changes are pushed to the `main` branch.

The security workflow performs the following checks:

1. Semgrep scans the source code using OWASP Top 10 and custom rules.
2. Bandit checks Python files for security vulnerabilities.
3. Gitleaks checks for exposed secrets.
4. OWASP Dependency-Check scans third-party dependencies.

The workflow provides individual results for each security tool, allowing developers to identify and investigate potential issues before merging changes.

## 7. Vulnerability Detection and Remediation

The sample application demonstrates how insecure coding practices can be identified and corrected.

### SQL Injection

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

The project includes a demonstration of SQL injection detection using Semgrep and Bandit, followed by remediation and successful security checks.

## 8. How to Use the Framework

1. Clone or fork this repository.
2. Open the repository in GitHub.
3. Review the sample application and custom security rules.
4. Create a new branch for code changes.
5. Submit a Pull Request targeting the `main` branch.
6. GitHub Actions automatically initiates the configured security scans.
7. Review the results of each security tool.
8. Investigate and remediate identified vulnerabilities.
9. Submit the corrected changes for another security assessment.

**Note:** OWASP Dependency-Check requires an NVD API key for vulnerability database access. Configure it as a GitHub Actions repository secret named `NVD_API_KEY`.

## 9. Current Implementation Status

| Component | Status |
|---|---|
| GitHub Actions integration | Implemented |
| Semgrep static analysis | Implemented |
| Bandit Python security scanning | Implemented |
| Gitleaks secret detection | Implemented |
| OWASP Dependency-Check | Implemented |
| Custom SQL injection rule | Implemented and tested |
| Custom weak cryptography rule | Implemented |
| Vulnerability remediation demonstration | Implemented |
| Authentication and RBAC | Planned |
| Centralized security dashboard | Planned |
| Compliance reporting enhancements | Planned |
| Performance optimization | Under evaluation |

## 10. Limitations and Future Enhancements

Future development may include:

- Implementing authentication and role-based access control (RBAC).
- Developing a centralized security reporting dashboard.
- Extending support to additional programming languages.
- Integrating additional security standards such as SANS and CERT guidelines.
- Improving vulnerability remediation recommendations.
- Optimizing dependency scanning performance through caching.
- Introducing enhanced compliance tracking and reporting.

## 11. Technologies Used

- Python
- Git and GitHub
- GitHub Actions
- Docker
- Semgrep
- Bandit
- Gitleaks
- OWASP Dependency-Check
- YAML

## 12. Disclaimer

This project is developed for educational and demonstration purposes as part of a cybersecurity project.

Automated security scanning helps identify potential vulnerabilities but does not guarantee that an application is completely secure. Manual security reviews and additional testing are recommended.

---

**Project:** Implementing a Secure Framework for a Code Review Tool  
**Repository:** `manasenfernandes/secure-code-review`

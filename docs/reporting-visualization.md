# Reporting and Visualization Setup

## 1. Objective

The reporting component of the Secure Code Review Framework collects security scan results and makes them accessible to developers and security reviewers.

It helps identify vulnerabilities, understand scan outcomes and track remediation activities.

## 2. Reporting Architecture

The framework uses GitHub Actions to execute automated security scans.

The reporting workflow includes:

1. Code submission through GitHub.
2. Automated security scans through GitHub Actions.
3. Scan findings displayed in workflow logs.
4. Dependency vulnerability reports generated as downloadable artifacts.
5. Developers and reviewers examine findings and take corrective action.

## 3. Integrated Security Scanners

| Security Tool | Purpose | Reporting Method |
|---|---|---|
| Semgrep | OWASP Top Ten and custom rule detection | GitHub Actions logs |
| Bandit | Python security issue detection | GitHub Actions logs |
| Gitleaks | Hardcoded secret detection | GitHub Actions logs |
| OWASP Dependency-Check | Third-party dependency vulnerability detection | HTML report artifact |

## 4. Accessing Security Scan Results

### GitHub Actions

1. Open the project repository.
2. Select the Actions tab.
3. Open the Security Scan workflow.
4. Select the required workflow execution.
5. Examine individual job results.
6. Open the logs to review scan findings.

### Dependency-Check HTML Report

1. Open the successful workflow execution.
2. Scroll to the Artifacts section.
3. Download the dependency-check-report artifact.
4. Extract the downloaded ZIP file.
5. Open dependency-check-report.html in a browser.

The report provides information about identified dependency vulnerabilities.

## 5. Reporting and Analysis

Security reviewers can use scan results to:

- Identify vulnerable code patterns.
- Detect exposed credentials and secrets.
- Review vulnerable third-party dependencies.
- Identify the affected files and security rules.
- Prioritize remediation based on severity.
- Verify corrections through subsequent scans.

## 6. Compliance and Standards Mapping

Security findings can be reviewed against:

- OWASP Top Ten.
- Common Weakness Enumeration (CWE).
- Relevant CERT secure coding recommendations.
- Custom Semgrep security rules.

This mapping supports security review and compliance tracking. It does not represent formal certification or complete compliance with these standards.

## 7. Current Implementation and Future Enhancements

### Currently Implemented

- Automated security scanning through GitHub Actions.
- Semgrep, Bandit and Gitleaks scan execution.
- OWASP Dependency-Check integration.
- Downloadable HTML dependency vulnerability report.
- Pull Request security status checks.

### Future Enhancements

- Centralized security dashboard.
- Historical vulnerability tracking.
- Graphical vulnerability trend analysis.
- Exportable consolidated PDF and Excel reports.
- Integration with platforms such as DefectDojo or Grafana.

## 8. Conclusion

The framework currently provides automated security scan results through GitHub Actions and downloadable dependency vulnerability reports.

These reporting capabilities help developers and security reviewers identify, analyze and remediate security weaknesses. Centralized dashboards and advanced reporting can be introduced as future enhancements.

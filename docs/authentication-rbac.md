# Authentication and Role-Based Access Control (RBAC)

## 1. Objective

This document explains the authentication and authorization approach used in the Secure Code Review Framework. It covers repository-level access controls currently implemented through GitHub and the proposed application-level RBAC model for future expansion.

## 2. Authentication

### Current Implementation

GitHub provides authentication for users accessing the project repository.

Users must authenticate through their GitHub accounts before accessing private repository resources or performing permitted actions.

### Security Controls
- GitHub account authentication.
- Repository access permissions.
- Restricted access to protected branches.
- Pull Request-based changes to the main branch.

## 3. Authorization and RBAC

Role-Based Access Control (RBAC) assigns permissions according to a user's responsibilities.

### Proposed Application Roles

| Role | Permissions |
|---|---|
| Administrator | Manage users, roles, configurations and security rules |
| Security Reviewer | Review scan findings, validate vulnerabilities and approve remediation |
| Developer | Submit code, view findings and address vulnerabilities |
| Viewer | View reports and security dashboards without modifying configurations |

These roles represent the proposed application-level design. They are not yet implemented as a standalone application feature.

## 4. Current GitHub Repository Security

The repository uses GitHub branch protection through the active ruleset named Protect Main Branch.

The following controls are enabled:

- Pull Requests are required before merging changes.
- Required security status checks must pass.
- Force pushes are blocked.
- Main branch changes are reviewed through the pull request workflow.

### Required Security Checks

1. Bandit (Python)
2. Semgrep (OWASP + custom rules)
3. Gitleaks (Secret Detection)

OWASP Dependency-Check is integrated into the workflow and generates a downloadable report artifact. It is not currently a required branch-protection check.

## 5. Access Control Principles

The framework follows these security principles:

- Least Privilege: Users should receive only the permissions required for their responsibilities.
- Separation of Duties: Code development and security approval should be separate responsibilities where practical.
- Accountability: Changes should be traceable through commits and pull requests.
- Controlled Changes: Changes to the protected main branch must satisfy the configured repository rules.

## 6. Future Enhancements

The following features can be introduced when the framework is expanded into a standalone application:

- Application-level login and secure session management.
- Multi-factor authentication.
- Custom role and permission management.
- Audit logs for user activities.
- Account lockout and session-expiration controls.
- Integration with enterprise identity providers.

## 7. Conclusion

The current framework uses GitHub authentication, repository permissions and branch protection to control access to project code. A structured application-level RBAC model has also been documented as a future enhancement to support secure collaboration and controlled access as the framework evolves.

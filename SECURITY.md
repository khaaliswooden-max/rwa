# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of RWA seriously. If you believe you have found a security vulnerability, please report it to us as described below.

**Please do NOT report security vulnerabilities through public GitHub issues.**

Instead, please send an email to **security@visionblox.io** with:

1. **Description** of the vulnerability
2. **Steps to reproduce** the issue
3. **Potential impact** of the vulnerability
4. **Any suggested fixes** (optional but appreciated)

### What to Expect

- **Acknowledgment**: Within 48 hours of your report
- **Initial Assessment**: Within 5 business days
- **Resolution Timeline**: Depends on severity (critical: 7 days, high: 30 days, medium: 90 days)
- **Credit**: We will credit you in our security advisories (unless you prefer anonymity)

### Scope

The following are in scope:
- RWA application code
- API endpoints
- Authentication and authorization
- Data handling and storage
- Dependencies with known vulnerabilities

### Out of Scope

- Denial of service attacks
- Social engineering
- Physical security
- Third-party services we don't control

## Security Best Practices for Deployment

### Environment Variables
- Never commit `.env` files
- Use strong, unique secrets for `SECRET_KEY` and `JWT_SECRET_KEY`
- Rotate secrets periodically

### Database
- Use strong passwords
- Enable SSL/TLS connections
- Restrict network access
- Regular backups with encryption

### API Security
- Always use HTTPS in production
- Implement rate limiting
- Validate all inputs
- Keep dependencies updated

## Acknowledgments

We thank the following individuals for responsibly disclosing vulnerabilities:

*No reports yet - be the first!*


# Security Best Practices & Guidelines

This document outlines the security measures implemented in the LinkedIn Posts Pipeline and guidelines for safe operation.

---

## 🔒 Security Implementation Status

### ✅ Implemented & Verified

| Feature | Implementation | Status |
|---------|-----------------|--------|
| **Secret Management** | API keys stored in .env (git-ignored) | ✅ Active |
| **Input Validation** | All URLs, content lengths validated | ✅ Active |
| **Error Handling** | Graceful exception handling throughout | ✅ Active |
| **Logging Security** | No secrets/passwords/tokens logged | ✅ Active |
| **HTTPS Only** | All API calls use HTTPS | ✅ Active |
| **Retry Logic** | Exponential backoff prevents abuse | ✅ Active |
| **Duplicate Prevention** | 409 HTTP status handling | ✅ Active |
| **File Path Validation** | file:// → GitHub URL conversion | ✅ Active |

---

## 🔐 API Key Management

### DO ✅

```bash
# 1. Store keys in .env
ZERNIO_API_KEY=sk_live_xxxxx
OPENROUTER_API_KEY=sk-or-v1-xxxxx

# 2. Ensure .env is in .gitignore
echo ".env" >> .gitignore

# 3. Share .env.example instead (template)
# .env.example has placeholder values only

# 4. Rotate keys periodically
# Go to API provider dashboard and generate new keys

# 5. Use environment variables in CI/CD
# GitHub Actions: Settings → Secrets and variables → Actions
```

### DON'T ❌

```bash
# 1. Never hardcode API keys
ZERNIO_API_KEY = "sk_live_xxxxx"  # WRONG!

# 2. Never commit .env to git
git add .env  # WRONG!

# 3. Never paste keys in logs
logger.info(f"Key: {api_key}")  # WRONG!

# 4. Never share keys in emails/chat
# Share only through secure channels

# 5. Never log full HTTP headers
# They may contain Authorization tokens
```

---

## 🚨 Input Validation

### Implemented Checks

```python
# URL Validation
if not validate_url(image_url):
    logger.warning(f"Invalid URL: {image_url}")
    # Use fallback or skip

# Content Length Validation
if len(post_content) > 3000:
    logger.error("Post too long")
    return error

# JSON Parsing Validation
data = safe_json_load(file_path)
if not data:
    logger.error("Invalid JSON")
    return error
```

### Never Trust User Input

```python
# ✗ WRONG: Direct use
os.system(f"curl {user_provided_url}")

# ✓ CORRECT: Validate first
if validate_url(user_provided_url):
    requests.get(user_provided_url)
```

---

## 📝 Logging Security

### What TO Log

```python
# ✓ Operational details
logger.info(f"Posted successfully! ID: {post_id}")
logger.debug(f"Processing carousel with {num_slides} slides")
logger.warning(f"Retrying request (attempt 2/3)")
logger.error(f"Failed to fetch image: timeout")
```

### What NOT TO Log

```python
# ✗ NEVER log these:
logger.info(f"API Key: {api_key}")
logger.info(f"Authorization: Bearer {token}")
logger.debug(f"URL: {url_with_api_key}")
logger.error(f"Response: {response_with_token}")
logger.info(f"Password: {password}")

# ✗ NEVER log full requests with headers:
logger.debug(f"Request headers: {headers}")  # May contain Auth!

# ✓ SAFE alternative - log only non-sensitive parts:
logger.debug(f"Request headers (sanitized): {{'Content-Type': 'application/json', 'User-Agent': '...'}}")
```

---

## 🔗 HTTPS & TLS

### All APIs Use HTTPS

```python
# Zernio API
ZERNIO_BASE_URL = "https://zernio.com/api/v1"  # ✓ HTTPS

# OpenRouter API
OPENROUTER_BASE_URL = "https://openrouter.io/api/v1"  # ✓ HTTPS

# Unsplash API
UNSPLASH_BASE_URL = "https://source.unsplash.com/"  # ✓ HTTPS

# GitHub Raw URLs
GITHUB_IMAGES_BASE = "https://raw.githubusercontent.com/..."  # ✓ HTTPS
```

### Verify SSL Certificates

```python
# Default behavior: Verify SSL
requests.get(url)  # SSL verification ON by default

# Only disable SSL verification if necessary (NOT RECOMMENDED):
requests.get(url, verify=False)  # ⚠️  DANGEROUS - Only for testing!
```

---

## 🔄 Secure Retry Logic

### Exponential Backoff

Prevents brute-force and rate-limit attacks:

```python
# 1st attempt: immediate
# 2nd attempt: wait 1 second
# 3rd attempt: wait 2 seconds
# 4th attempt: wait 4 seconds
# Failed: give up after MAX_RETRIES

# Prevents hammering API with thousands of requests
```

### Configuration

```python
# config/constants.py
MAX_RETRIES = 3              # Don't retry endlessly
INITIAL_RETRY_DELAY = 1      # Start with 1 second
EXPONENTIAL_BASE = 2         # Double wait time each retry
```

---

## 🚫 Rate Limiting & Abuse Prevention

### API Rate Limits

| API | Limit | Action |
|-----|-------|--------|
| **Zernio** | 100 req/min | Retries with backoff |
| **OpenRouter** | Varies by tier | Retries with backoff |
| **Unsplash** | 50 req/hour | Retries with backoff |

### How Pipeline Protects

1. **One pipeline run per day** - Not hammering APIs
2. **Exponential backoff** - Respects rate limits
3. **Error handling** - Graceful degradation
4. **Caching** - Reuses fetched images
5. **Timeout** - Cuts off slow requests

---

## 🔍 Audit Trail & Logging

### What Gets Logged

```
logs/linkedin_pipeline_YYYYMMDD.log
├─ Timestamp of each operation
├─ Success/failure status
├─ Number of posts processed
├─ IDs of posted content
├─ Errors and warnings (no secrets)
└─ Total execution time
```

### Review Logs

```bash
# View today's logs
cat logs/linkedin_pipeline_$(date +%Y%m%d).log

# Search for errors
grep ERROR logs/linkedin_pipeline_*.log

# Monitor in real-time
tail -f logs/linkedin_pipeline_$(date +%Y%m%d).log
```

---

## 🔐 GitHub Actions Security

### Secrets Configuration

1. **Never log secrets in CI/CD**:
   ```yaml
   # .github/workflows/daily-posts.yml
   - run: python main.py
     env:
       ZERNIO_API_KEY: ${{ secrets.ZERNIO_API_KEY }}  # ✓ Safe
       LOG_LEVEL: INFO  # ✓ Safe (not a secret)
   ```

2. **GitHub masks secrets in logs** - They appear as `***`

3. **Rotate keys regularly**
   - GitHub Settings → Secrets
   - Regenerate in API provider dashboard

---

## 🚨 Incident Response

### If API Key is Compromised

1. **Immediately revoke the key**
   - Zernio dashboard → API settings → Revoke
   - OpenRouter dashboard → Settings → Revoke

2. **Generate new key**
   - Get new key from API provider
   - Update in .env (local)
   - Update in GitHub Secrets (CI/CD)

3. **Review logs for abuse**
   ```bash
   grep "ERROR\|409\|401\|403" logs/*.log
   ```

4. **Monitor API usage**
   - Check Zernio/OpenRouter dashboard for unusual activity

---

## 📋 Security Checklist

Before deploying to production:

- [ ] .env file created and populated with real keys
- [ ] .env added to .gitignore (never committed)
- [ ] .env.example has placeholder values only
- [ ] No hardcoded secrets in source code
- [ ] All API calls use HTTPS
- [ ] Logging doesn't contain secrets
- [ ] Input validation on all user input
- [ ] Error handling for all API calls
- [ ] Retries use exponential backoff
- [ ] GitHub Actions secrets configured
- [ ] .github/workflows/daily-posts.yml uses ${{ secrets.X }}
- [ ] README.md documents security best practices
- [ ] SECURITY.md (this file) reviewed

---

## 🔗 Security Resources

- [OWASP: API Security](https://owasp.org/www-project-api-security/)
- [GitHub: Secrets Management](https://docs.github.com/en/actions/security-guides/encrypted-secrets)
- [Python: Security Best Practices](https://python-patterns.guide/python/security/)

---

**Last Updated**: 2026-07-03  
**Security Review**: Complete ✅  
**Status**: Production Safe ✅

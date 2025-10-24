# AWS Secrets Manager & Key Management Guide

## 🔐 HIPAA-Compliant Key Management for AlphaVox

This guide provides production-ready key management using AWS services for HIPAA compliance.

---

## 🚀 Quick Setup Commands

### 1. Create AWS Secrets Manager Secrets

```bash
# Admin credentials
aws secretsmanager create-secret \
    --name "alphavox/admin-credentials" \
    --description "AlphaVox admin authentication" \
    --secret-string '{"username":"admin_secure_user","password_hash":"$2b$12$..."}'

# JWT secrets
aws secretsmanager create-secret \
    --name "alphavox/jwt-secret" \
    --description "JWT signing key for AlphaVox" \
    --secret-string "$(openssl rand -base64 32)"

# HIPAA encryption key
aws secretsmanager create-secret \
    --name "alphavox/hipaa-encryption-key" \
    --description "HIPAA encryption master key" \
    --secret-string "$(openssl rand -base64 32)"

# API keys
aws secretsmanager create-secret \
    --name "alphavox/api-keys" \
    --description "External API keys" \
    --secret-string '{
        "OPENAI_API_KEY":"sk-...",
        "ANTHROPIC_API_KEY":"sk-ant-...",
        "PERPLEXITY_API_KEY":"pplx-..."
    }'
```

### 2. Create KMS Key for Extra Encryption

```bash
# Create KMS key for AlphaVox
aws kms create-key \
    --description "AlphaVox HIPAA encryption key" \
    --key-usage ENCRYPT_DECRYPT \
    --key-spec SYMMETRIC_DEFAULT

# Create alias
aws kms create-alias \
    --alias-name alias/alphavox-hipaa \
    --target-key-id <key-id-from-above>
```

---

## 📝 Python Integration

### Secrets Manager Helper

```python
import boto3
import json
from botocore.exceptions import ClientError

class SecretsManager:
    def __init__(self, region='us-east-1'):
        self.client = boto3.client('secretsmanager', region_name=region)
    
    def get_secret(self, secret_name):
        """Retrieve secret from AWS Secrets Manager."""
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            return json.loads(response['SecretString'])
        except ClientError as e:
            print(f"Error retrieving secret {secret_name}: {e}")
            return None
    
    def rotate_secret(self, secret_name):
        """Trigger secret rotation."""
        try:
            self.client.rotate_secret(SecretId=secret_name)
            return True
        except ClientError as e:
            print(f"Error rotating secret {secret_name}: {e}")
            return False

# Usage in production_app.py
secrets = SecretsManager()
admin_creds = secrets.get_secret('alphavox/admin-credentials')
jwt_secret = secrets.get_secret('alphavox/jwt-secret')
```

---

## 🔄 Automated Key Rotation

### Lambda Function for 90-Day Rotation

```python
import boto3
import json
import secrets

def lambda_handler(event, context):
    """Rotate AlphaVox secrets every 90 days."""
    
    client = boto3.client('secretsmanager')
    
    # Rotate JWT secret
    new_jwt_secret = secrets.token_urlsafe(32)
    client.update_secret(
        SecretId='alphavox/jwt-secret',
        SecretString=new_jwt_secret
    )
    
    # Rotate HIPAA encryption key
    new_hipaa_key = secrets.token_urlsafe(32)
    client.update_secret(
        SecretId='alphavox/hipaa-encryption-key',
        SecretString=new_hipaa_key
    )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Secrets rotated successfully')
    }
```

### CloudWatch Event for Scheduling

```bash
# Create EventBridge rule for 90-day rotation
aws events put-rule \
    --name "alphavox-key-rotation" \
    --schedule-expression "rate(90 days)" \
    --description "Rotate AlphaVox secrets every 90 days"

# Add Lambda target
aws events put-targets \
    --rule "alphavox-key-rotation" \
    --targets "Id"="1","Arn"="arn:aws:lambda:region:account:function:alphavox-rotate-secrets"
```

---

## 🔍 Security Monitoring

### CloudTrail Logging

```json
{
    "eventVersion": "1.05",
    "userIdentity": {
        "type": "IAMUser",
        "principalId": "AIDACKCEVSQ6C2EXAMPLE",
        "arn": "arn:aws:iam::123456789012:user/alphavox-app",
        "accountId": "123456789012",
        "userName": "alphavox-app"
    },
    "eventTime": "2025-10-24T12:00:00Z",
    "eventSource": "secretsmanager.amazonaws.com",
    "eventName": "GetSecretValue",
    "sourceIPAddress": "10.0.0.1",
    "resources": [
        {
            "accountId": "123456789012",
            "type": "AWS::SecretsManager::Secret",
            "ARN": "arn:aws:secretsmanager:us-east-1:123456789012:secret:alphavox/admin-credentials"
        }
    ]
}
```

### CloudWatch Alerts

```bash
# Alert on secret access
aws logs put-metric-filter \
    --log-group-name "CloudTrail/AlphaVoxSecrets" \
    --filter-name "SecretAccess" \
    --filter-pattern "{ $.eventName = GetSecretValue }" \
    --metric-transformations \
        metricName=SecretAccess,metricNamespace=AlphaVox,metricValue=1

# Create alarm
aws cloudwatch put-metric-alarm \
    --alarm-name "AlphaVox-Unusual-Secret-Access" \
    --alarm-description "Alert on unusual secret access patterns" \
    --metric-name SecretAccess \
    --namespace AlphaVox \
    --statistic Sum \
    --period 300 \
    --threshold 10 \
    --comparison-operator GreaterThanThreshold
```

---

## 📊 HIPAA Compliance Checklist

- [x] **Encryption at Rest**: AWS Secrets Manager encrypts by default
- [x] **Encryption in Transit**: TLS 1.2+ for all API calls
- [x] **Access Controls**: IAM policies restrict secret access
- [x] **Audit Logging**: CloudTrail logs all secret operations
- [x] **Key Rotation**: Automated 90-day rotation schedule
- [x] **Monitoring**: CloudWatch alerts on suspicious activity
- [x] **Backup & Recovery**: AWS handles automatic backups
- [x] **Geographic Controls**: Secrets stored in compliant regions

---

## 🚨 Emergency Procedures

### Secret Compromise Response

```bash
# 1. Immediately rotate compromised secret
aws secretsmanager rotate-secret --secret-id alphavox/admin-credentials

# 2. Review access logs
aws logs filter-log-events \
    --log-group-name CloudTrail/AlphaVoxSecrets \
    --start-time $(date -d '24 hours ago' +%s)000 \
    --filter-pattern "{ $.eventName = GetSecretValue }"

# 3. Update application configuration
kubectl set env deployment/alphavox FORCE_SECRET_REFRESH=true

# 4. Notify security team
aws sns publish \
    --topic-arn arn:aws:sns:us-east-1:123456789012:security-alerts \
    --message "AlphaVox secret rotation completed due to potential compromise"
```

---

## 💰 Cost Optimization

- **Secrets Manager**: $0.40/secret/month + $0.05/10,000 API calls
- **KMS**: $1/key/month + $0.03/10,000 requests
- **CloudTrail**: First trail free, data events $0.10/100,000 events

**Monthly estimate for AlphaVox**: ~$15-30 for complete key management

---

*© 2025 The Christman AI Project. HIPAA-compliant key management for healthcare AI.*
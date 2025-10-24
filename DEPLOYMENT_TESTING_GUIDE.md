# AlphaVox Production Deployment & Testing Guide

## 🚀 PRODUCTION DEPLOYMENT CHECKLIST

When you deploy AlphaVox to your production environment, follow these steps:

### 1. Environment Setup
```bash
# Copy environment template
cp .env.production .env

# Edit with your actual production values:
nano .env
```

**CRITICAL: Set these production values in .env:**
```bash
# Security (Generate strong keys!)
HIPAA_ENCRYPTION_KEY=your_actual_32_character_encryption_key_here
JWT_SECRET_KEY=your_actual_jwt_secret_key_here
FLASK_SECRET_KEY=your_flask_secret_key

# Database (Use PostgreSQL in production)
DATABASE_URL=postgresql://user:password@localhost:5432/alphavox_production

# AI Services (Your actual API keys)
ANTHROPIC_API_KEY=your_anthropic_api_key
OPENAI_API_KEY=your_openai_api_key  
PERPLEXITY_API_KEY=your_perplexity_api_key

# AWS for Voice Synthesis
AWS_ACCESS_KEY_ID=your_aws_access_key
AWS_SECRET_ACCESS_KEY=your_aws_secret_key
AWS_REGION=us-east-1

# SSL Certificates (Get real certificates!)
SSL_CERT_FILE=/etc/ssl/certs/alphavox.crt
SSL_KEY_FILE=/etc/ssl/private/alphavox.key
```

### 2. Audio/Visual Testing Checklist

**YOU MUST TEST THESE YOURSELF with your hardware:**

#### Voice Synthesis Testing:
```bash
# Test AWS Polly (requires API keys)
python3 -c "from alphavox_ultimate_voice import alphavoxUltimateVoice; av = alphavoxUltimateVoice(); av.speak('Testing AWS Polly voice synthesis')"

# Test gTTS fallback
python3 -c "import gtts; import pygame; print('Audio modules available')"

# Test system TTS
espeak "Testing system text to speech" 2>/dev/null || say "Testing system TTS"
```

#### Speech Recognition Testing:
```bash
# Test microphone and speech recognition
python3 -c "
import speech_recognition as sr
r = sr.Recognizer()
m = sr.Microphone()
print('Say something...')
with m as source: audio = r.listen(source, timeout=5)
print('Recognized:', r.recognize_google(audio))
"
```

#### Full System Audio Test:
```bash
# Complete voice conversation test
python3 -c "
from alphavox_ultimate_voice import alphavoxUltimateVoice
av = alphavoxUltimateVoice()
av.speak('AlphaVox voice system test. Please respond.')
response = av.listen(timeout=10)
if response:
    reply = av.chat(response)
    av.speak(reply)
    print('✓ Full audio conversation test passed')
else:
    print('⚠️ No speech detected - check microphone')
"
```

### 3. Security Validation Testing

**Run these tests in your production environment:**

```bash
# Test HIPAA encryption with your keys
python3 -c "
from security_config import HIPAAEncryption
enc = HIPAAEncryption()
test_phi = 'Patient John Doe, DOB 1990-01-01, Condition: Nonverbal autism'
encrypted = enc.encrypt(test_phi)
decrypted = enc.decrypt(encrypted)
print('✓ PHI encryption test:', 'PASSED' if decrypted == test_phi else 'FAILED')
"

# Test authentication system
python3 -c "
from security_config import SecurityManager
sm = SecurityManager()
token = sm.generate_jwt_token('doctor123', 'physician', ['read', 'write'])
payload = sm.verify_jwt_token(token)
print('✓ JWT auth test:', 'PASSED' if payload['user_id'] == 'doctor123' else 'FAILED')
"

# Test database encryption
python3 -c "
from memory_engine_secure import MemoryEngine
me = MemoryEngine()
status = me.get_status()
print('✓ Encrypted database:', 'OPERATIONAL' if status['hipaa_compliant'] else 'FAILED')
"
```

### 4. Production Deployment

```bash
# Make deployment script executable
chmod +x deploy_production.sh

# Set production environment
export ENVIRONMENT=production

# Run deployment (requires sudo for system setup)
sudo ./deploy_production.sh
```

### 5. Health Check Testing

**After deployment, verify these endpoints:**

```bash
# Health check
curl -k https://localhost/health

# Authentication test
curl -X POST https://localhost/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"YourProductionPassword"}'

# Voice synthesis test (with valid token)
curl -X POST https://localhost/api/voice/synthesize \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text":"Testing AlphaVox voice synthesis","voice":"matthew"}'

# Chat conversation test
curl -X POST https://localhost/api/chat \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"What is your mission?","patient_id":"test_patient"}'
```

### 6. Hardware-Specific Testing

**Test these on your actual deployment hardware:**

#### Audio Output Testing:
- Test speakers/headphones are working
- Verify audio volume levels
- Test different voice models (Matthew, Joanna, etc.)
- Confirm AWS Polly vs gTTS fallback works

#### Microphone Testing: 
- Test microphone sensitivity
- Verify noise cancellation
- Test in different acoustic environments
- Confirm speech recognition accuracy

#### Network Testing:
- Test internet connectivity for AI APIs
- Verify firewall rules allow HTTPS
- Test rate limiting behavior
- Confirm SSL certificates work

### 7. Patient Data Testing

**With REAL patient data (use test patients first):**

```bash
# Test patient data storage and retrieval
python3 -c "
from memory_engine_secure import MemoryEngine
from security_config import hipaa_logger

me = MemoryEngine()

# Store test patient data
patient_data = {
    'name': 'Test Patient',
    'dob': '2010-01-01', 
    'condition': 'Nonverbal autism',
    'communication_level': 'Beginning AAC user',
    'preferences': ['visual_cues', 'voice_synthesis', 'predictable_routine']
}

stored = me.store_patient_data('test_001', patient_data, 'clinician_001')
print('✓ Patient data stored:', stored)

retrieved = me.get_patient_data('test_001', 'clinician_001')
print('✓ Patient data retrieved:', retrieved is not None)

# Verify audit logging
print('✓ HIPAA audit logs created')
"
```

### 8. Load Testing

**Test with multiple users:**

```bash
# Install load testing tool
pip install locust

# Run load test
locust -f load_test.py --host=https://localhost
```

### 9. Backup Testing

**Verify backups work:**

```bash
# Test backup script
/opt/alphavox/backup.sh

# Verify backup file created
ls -la /opt/alphavox/backups/

# Test backup restoration (in test environment!)
# DO NOT run this in production without proper planning
```

### 10. Documentation for Your Team

**Create these documents for your deployment:**

1. **API Documentation** - All endpoints and authentication
2. **User Manual** - How clinicians use the system  
3. **Admin Guide** - System administration and monitoring
4. **Incident Response** - What to do if something goes wrong
5. **HIPAA Compliance** - Audit trail and compliance verification

---

## 🎯 FINAL PRODUCTION VERIFICATION

Before going live with real patients:

- [ ] All audio/visual hardware tested and working
- [ ] Real API keys configured and tested
- [ ] SSL certificates properly installed
- [ ] Database encryption verified
- [ ] User authentication working
- [ ] Rate limiting configured
- [ ] Monitoring and alerting set up
- [ ] Backup and recovery tested
- [ ] HIPAA compliance documented
- [ ] Staff trained on the system

## ⚠️ REMEMBER

- **Audio/Visual components require actual hardware to test properly**
- **AI APIs require your actual API keys and credits**
- **Patient data must be handled according to HIPAA requirements**
- **Test everything in a staging environment first**
- **Have a rollback plan ready**

## 🆘 SUPPORT

If you encounter issues during deployment:

1. Check logs: `/var/log/alphavox/application.log`
2. Verify configuration: Environment variables set correctly
3. Test components individually: Each audio/AI service separately
4. Review HIPAA audit logs: `/var/log/alphavox/hipaa_audit.log`

The system is designed to degrade gracefully - core conversation features will work even if some audio/visual components aren't available.

**Mission: Give voice to the voiceless** ✨
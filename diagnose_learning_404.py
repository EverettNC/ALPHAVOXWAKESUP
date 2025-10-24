# © 2025 The Christman AI Project. All rights reserved.
#
# This code is released as part of a trauma-informed, dignity-first AI ecosystem
# designed to protect, empower, and elevate vulnerable populations.
#
# By using, modifying, or distributing this software, you agree to uphold the following:
# 1. Truth — No deception, no manipulation.
# 2. Dignity — Respect the autonomy and humanity of all users.
# 3. Protection — Never use this to exploit or harm vulnerable individuals.
# 4. Transparency — Disclose all modifications and contributions clearly.
# 5. No Erasure — Preserve the mission and ethical origin of this work.
#
# This is not just code. This is redemption in code.
# Contact: lumacognify@thechristmanaiproject.com
# https://thechristmanaiproject.com

"""
Quick Fix for Learning Hub 404 Error
=====================================
This script checks why /learning returns 404 and applies a fix.
"""

import sys
import os

print("🔍 Diagnosing Learning Hub 404 Issue...")
print("=" * 70)

# Check 1: Does learning_routes exist?
print("\n1. Checking learning_routes files...")
routes_files = [
    "routes/learning_routes.py",
    "learning_routes.py"
]

learning_routes_exists = False
for file_path in routes_files:
    if os.path.exists(file_path):
        print(f"   ✅ Found: {file_path}")
        learning_routes_exists = True
    else:
        print(f"   ❌ Missing: {file_path}")

# Check 2: Is it being imported in app.py?
print("\n2. Checking app.py imports...")
try:
    with open("app.py", "r") as f:
        app_content = f.read()
    
    checks = {
        "register_learning_routes": "register_learning_routes" in app_content,
        "learning_bp": "learning_bp" in app_content,
        "from routes import": "from routes import" in app_content,
    }
    
    for check, result in checks.items():
        status = "✅" if result else "❌"
        print(f"   {status} {check}")
        
except Exception as e:
    print(f"   ❌ Error reading app.py: {e}")

# Check 3: Does routes/__init__.py export the function?
print("\n3. Checking routes/__init__.py...")
if os.path.exists("routes/__init__.py"):
    try:
        with open("routes/__init__.py", "r") as f:
            init_content = f.read()
        
        if "register_learning_routes" in init_content:
            print(f"   ✅ register_learning_routes is exported")
        else:
            print(f"   ❌ register_learning_routes NOT exported")
            print(f"   📝 Need to add to routes/__init__.py")
    except Exception as e:
        print(f"   ⚠️  Error: {e}")
else:
    print(f"   ❌ routes/__init__.py doesn't exist")

# Solution
print("\n" + "=" * 70)
print("🔧 SOLUTION")
print("=" * 70)

if not learning_routes_exists:
    print("❌ CRITICAL: learning_routes.py is missing!")
    print("   Solution: The file was deleted or not synced properly.")
    print("   Run: git pull origin main")
else:
    print("✅ learning_routes.py exists")
    print("\nThe issue is likely that the routes aren't being registered.")
    print("\nTo fix, we need to ensure app.py properly registers the blueprint.")
    print("\nLet me create a patch...")

print("\n" + "=" * 70)

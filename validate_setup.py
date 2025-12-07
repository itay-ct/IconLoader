#!/usr/bin/env python
"""
Validation script to check if the environment is properly configured
before running IconLoader.py
"""

import os
import sys
from pathlib import Path

def check_file_exists(filepath, required=True):
    """Check if a file exists"""
    exists = Path(filepath).exists()
    status = "✓" if exists else "✗"
    req_str = "(required)" if required else "(optional)"
    print(f"{status} {filepath} {req_str}")
    return exists or not required

def check_env_var(var_name, required=True):
    """Check if an environment variable is set"""
    from dotenv import load_dotenv
    load_dotenv()
    
    value = os.getenv(var_name)
    exists = value is not None and value != ""
    status = "✓" if exists else "✗"
    req_str = "(required)" if required else "(optional)"
    
    if exists and var_name == "REDIS_URL":
        # Mask the password in Redis URL
        masked = value.split('@')[0].split(':')[:-1]
        masked_url = ':'.join(masked) + ':****@' + value.split('@')[1] if '@' in value else "****"
        print(f"{status} {var_name}={masked_url} {req_str}")
    elif exists:
        print(f"{status} {var_name}={value} {req_str}")
    else:
        print(f"{status} {var_name} not set {req_str}")
    
    return exists or not required

def check_dependencies():
    """Check if required Python packages are installed"""
    required_packages = [
        'sentence_transformers',
        'redisvl',
        'dotenv',
        'requests',
        'redis',
        'numpy'
    ]
    
    all_installed = True
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} (not installed)")
            all_installed = False
    
    return all_installed

def main():
    print("=" * 60)
    print("IconLoader Setup Validation")
    print("=" * 60)
    
    print("\n1. Checking required files...")
    files_ok = all([
        check_file_exists("IconLoader.py", required=True),
        check_file_exists("config.py", required=True),
        check_file_exists("icons.txt", required=True),
        check_file_exists(".env", required=True),
        check_file_exists("requirements.txt", required=True),
    ])
    
    print("\n2. Checking environment variables...")
    env_ok = all([
        check_env_var("REDIS_URL", required=True),
        check_env_var("ICONS_FILE_PATH", required=False),
    ])
    
    print("\n3. Checking Python dependencies...")
    deps_ok = check_dependencies()
    
    print("\n" + "=" * 60)
    if files_ok and env_ok and deps_ok:
        print("✓ All checks passed! You're ready to run IconLoader.py")
        print("=" * 60)
        return 0
    else:
        print("✗ Some checks failed. Please fix the issues above.")
        print("=" * 60)
        if not deps_ok:
            print("\nTo install dependencies, run:")
            print("  pip install -r requirements.txt")
        if not env_ok:
            print("\nTo configure environment variables:")
            print("  cp .env.example .env")
            print("  # Then edit .env and set REDIS_URL")
        return 1

if __name__ == "__main__":
    sys.exit(main())


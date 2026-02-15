"""
Validate unified dependency setup across all deployment targets
"""
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.12.x"""
    version = sys.version_info
    print(f"✓ Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major == 3 and version.minor == 12:
        print("  ✅ Python 3.12.x detected - compatible with all deployment targets")
        return True
    else:
        print(f"  ⚠️  Warning: Python 3.12.x recommended (you have {version.major}.{version.minor}.{version.micro})")
        return False

def check_file_exists(filepath, description):
    """Check if a required file exists"""
    path = Path(filepath)
    if path.exists():
        print(f"✓ {description}: {filepath}")
        print(f"  ✅ File exists")
        return True
    else:
        print(f"✗ {description}: {filepath}")
        print(f"  ❌ File missing")
        return False

def check_requirements_content():
    """Check if requirements.txt has all necessary dependencies"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'streamlit',
        'pandas',
        'numpy',
        'scikit-learn',
        'xgboost',
        'plotly'
    ]
    
    req_file = Path('requirements.txt')
    if not req_file.exists():
        print("❌ requirements.txt not found")
        return False
    
    content = req_file.read_text()
    missing = []
    
    for pkg in required_packages:
        if pkg not in content.lower():
            missing.append(pkg)
    
    if missing:
        print(f"  ⚠️  Missing packages: {', '.join(missing)}")
        return False
    else:
        print(f"  ✅ All core packages present: {', '.join(required_packages)}")
        return True

def main():
    print("=" * 70)
    print("🔍 UNIFIED DEPENDENCY VALIDATION")
    print("=" * 70)
    print()
    
    results = []
    
    # Check Python version
    print("1. Checking Python Version")
    results.append(check_python_version())
    print()
    
    # Check required files
    print("2. Checking Configuration Files")
    results.append(check_file_exists('requirements.txt', 'Main requirements'))
    results.append(check_file_exists('runtime.txt', 'Streamlit Cloud Python version'))
    results.append(check_file_exists('render.yaml', 'Render deployment config'))
    results.append(check_file_exists('setup.py', 'Package setup'))
    print()
    
    # Check requirements content
    print("3. Checking Requirements Content")
    results.append(check_requirements_content())
    print()
    
    # Summary
    print("=" * 70)
    if all(results):
        print("✅ ALL CHECKS PASSED - Unified dependency system ready!")
        print("\nYou can now:")
        print("  • Run API locally: uvicorn src.api.main:app --reload")
        print("  • Run Dashboard locally: streamlit run dashboard/app.py")
        print("  • Deploy to Render: Push to GitHub")
        print("  • Deploy to Streamlit Cloud: Push to GitHub")
    else:
        print("⚠️  SOME CHECKS FAILED - Review warnings above")
        print("\nRefer to DEPLOYMENT.md for troubleshooting")
    print("=" * 70)

if __name__ == "__main__":
    main()

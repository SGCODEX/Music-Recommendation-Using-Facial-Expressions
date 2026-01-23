"""
Comprehensive Error Check Script
Checks for all potential issues in the project
"""

import os
import sys
import subprocess

def print_header(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def check_syntax_errors():
    """Check for Python syntax errors in all Python files"""
    print_header("Checking Python Syntax Errors")
    
    python_files = []
    for root, dirs, files in os.walk('code'):
        # Skip __pycache__ directories
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    
    # Add root level Python files
    for file in ['test_music_apis.py', 'verify_installation.py']:
        if os.path.exists(file):
            python_files.append(file)
    
    errors_found = False
    for filepath in python_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                compile(f.read(), filepath, 'exec')
            print(f"✅ {filepath}")
        except SyntaxError as e:
            print(f"❌ {filepath}: Line {e.lineno}: {e.msg}")
            errors_found = True
        except Exception as e:
            print(f"⚠️  {filepath}: {str(e)}")
    
    if not errors_found:
        print("\n✅ No syntax errors found!")
    return not errors_found

def check_imports():
    """Check if all required modules can be imported"""
    print_header("Checking Module Imports")
    
    required_packages = [
        ('streamlit', 'streamlit'),
        ('cv2', 'opencv-python-headless'),
        ('keras', 'keras'),
        ('tensorflow', 'tensorflow'),
        ('numpy', 'numpy'),
        ('requests', 'requests'),
        ('spotipy', 'spotipy'),
        ('dotenv', 'python-dotenv'),
        ('googleapiclient', 'google-api-python-client'),
    ]
    
    all_good = True
    for module, package_name in required_packages:
        try:
            __import__(module)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name} - Not installed")
            all_good = False
    
    # Check custom modules
    print("\nChecking custom modules...")
    sys.path.insert(0, 'code')
    try:
        from music_apis import EmotionMapper, SpotifyMusicAPI, YouTubeMusicAPI
        print("✅ music_apis module")
    except ImportError as e:
        print(f"❌ music_apis module - {e}")
        all_good = False
    
    if all_good:
        print("\n✅ All required modules available!")
    return all_good

def check_file_structure():
    """Check if all required files exist"""
    print_header("Checking File Structure")
    
    required_files = [
        ('code/model/fer2013_mini_XCEPTION.102-0.66.hdf5', 'Emotion detection model'),
        ('code/music_apis/__init__.py', 'Music APIs module'),
        ('code/music_apis/emotion_mapper.py', 'Emotion mapper'),
        ('code/music_apis/spotify_api.py', 'Spotify API client'),
        ('code/music_apis/youtube_api.py', 'YouTube API client'),
        ('code/deployment/app.py', 'Original Streamlit app'),
        ('code/deployment/app_with_music_apis.py', 'Enhanced Streamlit app'),
        ('.env.example', 'Environment template'),
        ('requirements.txt', 'Dependencies'),
        ('API_SETUP_GUIDE.md', 'API setup guide'),
        ('MUSIC_API_INTEGRATION.md', 'Integration docs'),
        ('QUICK_START.md', 'Quick start guide'),
    ]
    
    all_good = True
    for filepath, description in required_files:
        if os.path.exists(filepath):
            print(f"✅ {description}: {filepath}")
        else:
            print(f"❌ {description}: {filepath} - NOT FOUND")
            all_good = False
    
    if all_good:
        print("\n✅ All required files present!")
    return all_good

def check_configuration():
    """Check configuration files"""
    print_header("Checking Configuration Files")
    
    all_good = True
    
    # Check .env.example
    if os.path.exists('.env.example'):
        with open('.env.example', 'r') as f:
            content = f.read()
            if '"""' in content or "'''" in content:
                print("⚠️  .env.example contains Python docstrings (should use # comments)")
                all_good = False
            else:
                print("✅ .env.example format correct")
    
    # Check pyrightconfig.json
    if os.path.exists('pyrightconfig.json'):
        print("✅ pyrightconfig.json exists")
    else:
        print("⚠️  pyrightconfig.json missing (Pylance may show import warnings)")
        all_good = False
    
    # Check VS Code settings
    if os.path.exists('.vscode/settings.json'):
        print("✅ .vscode/settings.json exists")
    else:
        print("⚠️  .vscode/settings.json missing (Pylance may show import warnings)")
        all_good = False
    
    return all_good

def check_code_quality():
    """Check for common code issues"""
    print_header("Checking Code Quality")
    
    issues = []
    
    # Check for hardcoded credentials
    print("Checking for hardcoded credentials...")
    for root, dirs, files in os.walk('code'):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    lines = content.split('\n')
                    for i, line in enumerate(lines, 1):
                        # Skip comments and lines with safe patterns
                        if line.strip().startswith('#'):
                            continue
                        if 'self.client_id = client_id' in line or 'self.api_key = api_key' in line:
                            continue
                        if 'os.getenv' in line or '= None' in line or '=""' in line or "=''" in line:
                            continue
                        
                        # Check for actual hardcoded credentials (long strings that look like API keys)
                        if ('api_key' in line.lower() or 'client_id' in line.lower() or 'client_secret' in line.lower()) and '=' in line:
                            # Look for suspicious patterns like long alphanumeric strings
                            import re
                            if re.search(r'["\'][A-Za-z0-9]{20,}["\']', line):
                                print(f"⚠️  Possible hardcoded credential: {filepath}:{i}")
                                issues.append(f"{filepath}:{i}")
    
    if not issues:
        print("✅ No hardcoded credentials found")
    
    # Check for type: ignore comments
    print("\nChecking for type ignore comments...")
    ignore_count = 0
    for root, dirs, files in os.walk('code'):
        dirs[:] = [d for d in dirs if d != '__pycache__']
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    if '# type: ignore' in f.read():
                        ignore_count += 1
    
    print(f"ℹ️  Found {ignore_count} files with type: ignore comments (this is fine)")
    
    return len(issues) == 0

def main():
    """Run all checks"""
    print("\n" + "="*70)
    print("  🔍 COMPREHENSIVE ERROR CHECK")
    print("="*70)
    print("\nThis script will check for:")
    print("  • Python syntax errors")
    print("  • Missing dependencies")
    print("  • Missing files")
    print("  • Configuration issues")
    print("  • Code quality issues")
    
    input("\nPress Enter to start...")
    
    results = []
    
    # Run all checks
    results.append(("Syntax Check", check_syntax_errors()))
    results.append(("Import Check", check_imports()))
    results.append(("File Structure", check_file_structure()))
    results.append(("Configuration", check_configuration()))
    results.append(("Code Quality", check_code_quality()))
    
    # Summary
    print_header("SUMMARY")
    
    all_passed = all(result[1] for result in results)
    
    for check_name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{check_name}: {status}")
    
    print("\n" + "="*70)
    
    if all_passed:
        print("  🎉 ALL CHECKS PASSED!")
        print("="*70)
        print("\n✅ Your project is ready to run!")
        print("\nNext steps:")
        print("  1. Set up API credentials (optional):")
        print("     cp .env.example .env")
        print("     # Edit .env with your credentials")
        print("\n  2. Run the enhanced app:")
        print("     streamlit run code/deployment/app_with_music_apis.py")
    else:
        print("  ⚠️  SOME CHECKS FAILED")
        print("="*70)
        print("\n❌ Please fix the issues above before running the app")
        print("\nCommon fixes:")
        print("  • Install missing packages: pip install -r requirements.txt")
        print("  • Check file paths are correct")
        print("  • Review configuration files")
    
    print("\n" + "="*70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Check cancelled by user\n")
    except Exception as e:
        print(f"\n\n❌ Error during check: {str(e)}\n")
        import traceback
        traceback.print_exc()

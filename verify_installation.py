"""
Quick Installation Verification Script
Run this after installing dependencies to verify everything is set up correctly
"""

import sys
import os

def check_package(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        __import__(import_name)
        print(f"✅ {package_name} is installed")
        return True
    except ImportError:
        print(f"❌ {package_name} is NOT installed")
        return False

def check_file(filepath, description):
    """Check if a file exists"""
    if os.path.exists(filepath):
        print(f"✅ {description} found")
        return True
    else:
        print(f"❌ {description} NOT found")
        return False

def main():
    print("\n" + "="*60)
    print("  🔍 Installation Verification")
    print("="*60 + "\n")
    
    all_good = True
    
    # Check core dependencies
    print("📦 Checking Core Dependencies...")
    print("-" * 60)
    all_good &= check_package("streamlit")
    all_good &= check_package("cv2", "cv2")
    all_good &= check_package("tensorflow")
    all_good &= check_package("keras")
    all_good &= check_package("numpy")
    all_good &= check_package("requests")
    
    # Check WebRTC
    print("\n📹 Checking WebRTC Dependencies...")
    print("-" * 60)
    all_good &= check_package("streamlit-webrtc", "streamlit_webrtc")
    
    # Check new API dependencies
    print("\n🎵 Checking Music API Dependencies...")
    print("-" * 60)
    all_good &= check_package("spotipy")
    all_good &= check_package("google-api-python-client", "googleapiclient")
    all_good &= check_package("python-dotenv", "dotenv")
    
    # Check music_apis module
    print("\n🎼 Checking Music API Modules...")
    print("-" * 60)
    
    base_path = os.path.dirname(os.path.abspath(__file__))
    
    all_good &= check_file(
        os.path.join(base_path, "code", "music_apis", "__init__.py"),
        "music_apis module"
    )
    all_good &= check_file(
        os.path.join(base_path, "code", "music_apis", "emotion_mapper.py"),
        "Emotion Mapper"
    )
    all_good &= check_file(
        os.path.join(base_path, "code", "music_apis", "spotify_api.py"),
        "Spotify API client"
    )
    all_good &= check_file(
        os.path.join(base_path, "code", "music_apis", "youtube_api.py"),
        "YouTube API client"
    )
    
    # Check model file
    print("\n🧠 Checking Model Files...")
    print("-" * 60)
    all_good &= check_file(
        os.path.join(base_path, "code", "model", "fer2013_mini_XCEPTION.102-0.66.hdf5"),
        "Emotion detection model"
    )
    
    # Check application files
    print("\n🖥️  Checking Application Files...")
    print("-" * 60)
    all_good &= check_file(
        os.path.join(base_path, "code", "deployment", "app.py"),
        "Original app"
    )
    all_good &= check_file(
        os.path.join(base_path, "code", "deployment", "app_with_music_apis.py"),
        "Enhanced app with Music APIs"
    )
    
    # Check documentation
    print("\n📚 Checking Documentation...")
    print("-" * 60)
    all_good &= check_file(
        os.path.join(base_path, "API_SETUP_GUIDE.md"),
        "API Setup Guide"
    )
    all_good &= check_file(
        os.path.join(base_path, "MUSIC_API_INTEGRATION.md"),
        "Music API Integration Docs"
    )
    all_good &= check_file(
        os.path.join(base_path, "QUICK_START.md"),
        "Quick Start Guide"
    )
    
    # Check configuration
    print("\n⚙️  Checking Configuration Files...")
    print("-" * 60)
    all_good &= check_file(
        os.path.join(base_path, ".env.example"),
        ".env.example template"
    )
    all_good &= check_file(
        os.path.join(base_path, "requirements.txt"),
        "requirements.txt"
    )
    
    # Check for .env file (optional)
    env_exists = check_file(
        os.path.join(base_path, ".env"),
        ".env file (optional)"
    )
    
    # Summary
    print("\n" + "="*60)
    if all_good:
        print("  ✅ All Required Components Verified!")
        print("="*60)
        print("\n🎉 Installation Complete! You're ready to go!\n")
        print("Next steps:")
        print("  1. Set up API credentials (optional but recommended):")
        print("     cp .env.example .env")
        print("     # Edit .env with your credentials")
        print("\n  2. Run the enhanced app:")
        print("     streamlit run code/deployment/app_with_music_apis.py")
        print("\n  3. Or test the APIs first:")
        print("     python test_music_apis.py")
        
        if not env_exists:
            print("\n💡 Tip: Create a .env file for easier credential management")
            print("   See API_SETUP_GUIDE.md for detailed instructions")
    else:
        print("  ⚠️  Some Components Missing")
        print("="*60)
        print("\n❌ Installation Incomplete\n")
        print("Please fix the issues above and try again:")
        print("  1. Install missing packages:")
        print("     pip install -r requirements.txt")
        print("\n  2. Make sure you're in the project root directory")
        print("\n  3. Check that all files were cloned correctly")
    
    print("\n" + "="*60 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Verification cancelled by user\n")
    except Exception as e:
        print(f"\n\n❌ Error during verification: {str(e)}\n")
        import traceback
        traceback.print_exc()

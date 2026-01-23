# 🔧 Troubleshooting Import Issues

If you're seeing Pylance errors like "Import 'music_apis' could not be resolved", this guide will help you fix them.

---

## ✅ Quick Fix

**For VS Code users**, the import issues should be automatically resolved by the configuration files:

- `.vscode/settings.json` - Pylance configuration
- `pyrightconfig.json` - Pyright configuration

If you still see errors after cloning:

1. **Reload VS Code Window**
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Reload Window" and press Enter
   - Or close and reopen VS Code

2. **Verify Configuration Files Exist**
   - Check that `.vscode/settings.json` exists
   - Check that `pyrightconfig.json` exists in the root

3. **Check Python Interpreter**
   - Press `Ctrl+Shift+P` and type "Python: Select Interpreter"
   - Choose the interpreter where you installed dependencies

---

## 🔍 Understanding the Issue

### Project Structure

```
Music-Recommendation-Using-Facial-Expressions/
├── code/
│   └── music_apis/          # Module is here
│       ├── __init__.py
│       ├── emotion_mapper.py
│       ├── spotify_api.py
│       └── youtube_api.py
├── test_music_apis.py       # Imports from root
└── verify_installation.py
```

### The Problem

Scripts in the root directory import `music_apis`, but the module is in `code/music_apis/`:

```python
from music_apis import EmotionMapper  # ❌ Pylance can't find this
```

### The Solution

We add `code/` to Python's import path:

**At Runtime** (in scripts):

```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))
```

**For Pylance** (in .vscode/settings.json):

```json
{
  "python.analysis.extraPaths": ["./code"]
}
```

---

## 🛠️ Manual Configuration

If the configuration files are missing or not working:

### Option 1: VS Code Settings (Recommended)

Create `.vscode/settings.json`:

```json
{
  "python.analysis.extraPaths": ["./code"],
  "python.autoComplete.extraPaths": ["./code"]
}
```

### Option 2: Pyrightconfig.json

Create `pyrightconfig.json` in the root:

```json
{
  "extraPaths": ["./code"],
  "include": ["code", "test_music_apis.py", "verify_installation.py"]
}
```

### Option 3: Python Path Environment Variable

Add to your shell profile (`.bashrc`, `.zshrc`, etc.):

```bash
export PYTHONPATH="${PYTHONPATH}:/path/to/project/code"
```

Or for Windows (PowerShell):

```powershell
$env:PYTHONPATH += ";C:\path\to\project\code"
```

---

## ✅ Verification

Test if imports work:

```bash
# Test from command line
python -c "import sys; sys.path.insert(0, 'code'); from music_apis import EmotionMapper; print('Success!')"

# Run the test script
python test_music_apis.py

# Run the verification script
python verify_installation.py
```

All should run without import errors.

---

## 🐛 Still Having Issues?

### Check Your Working Directory

Make sure you're in the project root:

```bash
cd Music-Recommendation-Using-Facial-Expressions
pwd  # Should end with .../Music-Recommendation-Using-Facial-Expressions
```

### Check File Structure

Verify the music_apis module exists:

```bash
ls -la code/music_apis/
# Should show: __init__.py, emotion_mapper.py, spotify_api.py, youtube_api.py
```

### Check Python Environment

```bash
which python  # or 'where python' on Windows
python --version
pip list | grep -i spotify  # Check if dependencies installed
```

### Reinstall Dependencies

```bash
pip install -r requirements.txt --force-reinstall
```

### Clear Python Cache

```bash
find . -type d -name "__pycache__" -exec rm -r {} +  # Unix/Mac
# Or manually delete __pycache__ folders on Windows
```

---

## 💡 For Different IDEs

### PyCharm

1. Right-click on `code` folder → "Mark Directory as" → "Sources Root"
2. Or go to Settings → Project → Project Structure → Add Content Root → Select `code/`

### Jupyter Notebook

Add at the top of your notebook:

```python
import sys
sys.path.insert(0, './code')
```

### Command Line / Scripts

The scripts already handle this automatically with:

```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'code'))
```

---

## 📚 Additional Resources

- [Pylance Import Resolution Guide](https://github.com/microsoft/pylance-release/blob/main/TROUBLESHOOTING.md)
- [Python Import System Documentation](https://docs.python.org/3/reference/import.html)
- [VS Code Python Path Settings](https://code.visualstudio.com/docs/python/environments)

---

## 🆘 Getting Help

If nothing works:

1. Check [GitHub Issues](https://github.com/SGCODEX/Music-Recommendation-Using-Facial-Expressions/issues)
2. Create a new issue with:
   - Your OS and Python version
   - Screenshot of the error
   - Output of `python verify_installation.py`
   - Your VS Code Python extension version

---

**Note**: Import warnings in the editor don't affect runtime execution. Your code will still work even if Pylance shows warnings!

# VS Code Configuration for Music Recommendation Project

This folder contains VS Code-specific settings to help with Python development.

## settings.json

Configures Pylance to correctly resolve imports from the `code/` directory.

### Key Settings:

- **`python.analysis.extraPaths`**: Tells Pylance where to find additional Python modules
- **`python.autoComplete.extraPaths`**: Enables autocomplete for modules in `code/` directory

This fixes import errors like:

```
Import "music_apis" could not be resolved
```

## Why This is Needed

The project structure has modules in the `code/` directory:

```
code/
  music_apis/
    __init__.py
    emotion_mapper.py
    spotify_api.py
    youtube_api.py
```

But scripts in the root (like `test_music_apis.py`) import them directly:

```python
from music_apis import EmotionMapper
```

The `sys.path` manipulation at runtime works, but Pylance needs explicit configuration to understand the import paths during editing.

## Pyrightconfig.json

The root `pyrightconfig.json` file also helps with this by configuring the Pyright type checker (which Pylance uses) to include the `code/` directory in its module resolution.

## Troubleshooting

If you still see import errors:

1. **Reload VS Code Window**: `Ctrl+Shift+P` → "Developer: Reload Window"
2. **Check Python Interpreter**: Make sure you're using the correct Python environment
3. **Verify File Paths**: Ensure `code/music_apis/` directory exists
4. **Install Dependencies**: Run `pip install -r requirements.txt`

## References

- [Pylance Import Resolution](https://github.com/microsoft/pylance-release/blob/main/TROUBLESHOOTING.md#import-resolution)
- [Python Path Configuration](https://code.visualstudio.com/docs/python/environments)

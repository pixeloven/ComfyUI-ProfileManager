# ComfyUI Profile Manager

A React-based ComfyUI extension for managing reproducible environments with specific models, extensions, and configurations.

## 🎯 What It Does

The Profile Manager solves the problem of **environment consistency** in ComfyUI by providing:
- **Reproducible Environments**: Define specific models, extensions, and configurations
- **Profile Inheritance**: Extend existing profiles to build upon common setups
- **Web Interface**: Easy management through a modern React UI
- **Validation**: Automatic checking of profile structure and dependencies

## 🚀 Quick Start

### Installation

1. **Clone the extension**:
   ```bash
   cd ComfyUI/custom_nodes
   git clone <repository-url> ComfyUI-ProfileManager
   ```

2. **Build the extension**:
   ```bash
   cd ComfyUI-ProfileManager/ui
   npm install
   npm run build
   ```

3. **Restart ComfyUI** and access: `http://localhost:8188/profile_manager/`

### Using Profiles

1. **View Available Profiles**: See all profiles with their dependencies and contents
2. **Create New Profile**: Click "Create New Profile" and specify name and extensions
3. **Validate Profiles**: Check profile structure and dependencies
4. **Apply Profiles**: Profiles automatically install required extensions and models

## 📦 Profile Examples

### Base Profile
Essential models and extensions for basic ComfyUI functionality.

### Anime Profile
Extends base profile with anime-specific models and extensions.

### Professional Profile
High-quality commercial models and professional-grade tools.

### IPAdapter Profile
Face control and manipulation with IPAdapter models and extensions.

## 🏗️ Profile Structure

Each profile consists of:

```
profiles/
├── profile-name/
│   ├── profile.yaml       # Main configuration
│   ├── requirements.txt   # Python dependencies
│   └── workflows/         # Example workflows (optional)
```

### Profile Configuration

```yaml
name: "my-profile"
version: "1.0.0"
description: "My custom workflow profile"
extends: ["base", "anime"]  # Inherit from other profiles

requirements:
  python: ">=3.10"
  gpu: ">=4GB"
  storage: ">=20GB"

models:
  - name: "my-model"
    type: "checkpoint"
    url: "https://example.com/model.safetensors"

extensions:
  git:
    - name: "ComfyUI-AnimateDiff-Evolved"
      url: "https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved"
  pip:
    - name: "external-package"
      version: "1.0.0"
```

## 🔧 Development

### Development Mode

```bash
cd ui
npm run dev
```

Access development server at `http://localhost:3000`.

### Building

```bash
cd ui
npm run build
```

### Testing

```bash
# Test profile structure
python test_profile_files.py

# Test profile system
python test_profiles.py
```

## 📡 API Endpoints

- `GET /profile_manager/api/profiles` - List all profiles
- `GET /profile_manager/api/profile/{name}` - Get profile details
- `POST /profile_manager/api/validate/{name}` - Validate profile
- `POST /profile_manager/api/create` - Create new profile

## 🎯 Key Benefits

### For Users
- **Consistent Environments**: Same setup across different machines
- **Easy Sharing**: Share complete configurations via profiles
- **Validation**: Automatic checking prevents configuration errors
- **Inheritance**: Build upon existing profiles instead of starting from scratch

### For Developers
- **TypeScript**: Full type safety and better development experience
- **React**: Modern, maintainable component architecture
- **Hot Reloading**: Fast development iteration
- **Testing**: Easy to test and validate profiles

## 🚨 Troubleshooting

### Common Issues

**Profile Not Found**
- Ensure profile directory exists in `profiles/`
- Check profile name matches directory name

**Validation Errors**
- Verify YAML syntax in `profile.yaml`
- Check that extended profiles exist
- Ensure no circular dependencies

**Extension Installation Fails**
- Check internet connectivity
- Verify Git repository URLs
- Review ComfyUI logs for specific errors

### Getting Help

- Check ComfyUI logs: `docker compose logs -f`
- Validate profile structure using the web interface
- Review [GitHub Issues](https://github.com/pixeloven/ComfyUI-ProfileManager/issues)

## 📚 Project Structure

```
ComfyUI-ProfileManager/
├── __init__.py                    # Python backend
├── README.md                     # This file
├── profiles/                     # Profile examples
│   ├── base/
│   ├── anime/
│   ├── professional/
│   └── ipadapter/
├── ui/                          # React frontend
│   ├── src/
│   ├── package.json
│   └── vite.config.ts
└── test_*.py                    # Test files
```

---

**[⬆ Back to Main Project](../../README.md)** | **[🐛 Report Issues](https://github.com/pixeloven/ComfyUI-ProfileManager/issues)** 
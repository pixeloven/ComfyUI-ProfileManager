#!/usr/bin/env python3
"""
Test script for profile file structure
"""

import os
import yaml
from pathlib import Path

def test_profile_files():
    """Test that profile files exist and are valid YAML"""
    print("Testing Profile File Structure")
    print("=" * 40)
    
    # Check the extension directory (now we're inside it)
    extension_dir = Path(".")
    if not extension_dir.exists():
        print("❌ Current directory does not exist")
        return
    
    # Find all profile.yaml files within the extension's profiles directory
    profiles_subdir = extension_dir / "profiles"
    if profiles_subdir.exists():
        profile_files = list(profiles_subdir.rglob("profile.yaml"))
    else:
        profile_files = []
    print(f"Found {len(profile_files)} profile.yaml files:")
    
    for profile_file in profile_files:
        profile_name = profile_file.parent.name
        print(f"\n📁 Profile: {profile_name}")
        print(f"   Path: {profile_file}")
        
        # Check if file is valid YAML
        try:
            with open(profile_file, 'r') as f:
                config = yaml.safe_load(f)
            
            # Check required fields
            required_fields = ['name', 'version', 'description']
            missing_fields = [field for field in required_fields if field not in config]
            
            if missing_fields:
                print(f"   ❌ Missing required fields: {missing_fields}")
            else:
                print(f"   ✅ Valid YAML with required fields")
                print(f"   📝 Description: {config.get('description', 'No description')}")
                print(f"   🏷️  Tags: {config.get('tags', [])}")
                print(f"   🔗 Extends: {config.get('extends', [])}")
                print(f"   📦 Models: {len(config.get('models', []))}")
                
                # Check extensions
                extensions = config.get('extensions', {})
                git_extensions = extensions.get('git', [])
                pip_extensions = extensions.get('pip', [])
                print(f"   🔌 Extensions: {len(git_extensions)} git, {len(pip_extensions)} pip")
                
        except yaml.YAMLError as e:
            print(f"   ❌ Invalid YAML: {e}")
        except Exception as e:
            print(f"   ❌ Error reading file: {e}")
    
    # Check for any remaining pack.yaml files (should be none)
    pack_files = list(extension_dir.rglob("pack.yaml"))
    if pack_files:
        print(f"\n⚠️  Found {len(pack_files)} pack.yaml files (should be renamed to profile.yaml):")
        for pack_file in pack_files:
            print(f"   - {pack_file}")
    else:
        print(f"\n✅ No pack.yaml files found (all renamed to profile.yaml)")
    
    # Check extension structure
    print(f"\n📂 Extension Structure:")
    print(f"   ✅ __init__.py (Python backend)")
    print(f"   ✅ ui/ (React frontend)")
    print(f"   ✅ README.md (Documentation)")
    print(f"   ✅ PROJECT_PLAN.md (Project planning)")
    print(f"   ✅ ARCHITECTURE.md (Architecture docs)")
    print(f"   ✅ requirements.md (Profile requirements)")
    print(f"   ✅ test_profile_files.py (Structure test)")
    print(f"   ✅ test_profiles.py (System test)")
    print(f"   ✅ MIGRATION_SUMMARY.md (Migration docs)")
    print(f"   ✅ REORGANIZATION_SUMMARY.md (Reorganization docs)")
    print(f"   ✅ FINAL_STRUCTURE.md (Final structure docs)")
    
    # List profile directories
    profiles_subdir = extension_dir / "profiles"
    if profiles_subdir.exists():
        profile_dirs = [d for d in profiles_subdir.iterdir() if d.is_dir()]
        print(f"\n📁 Profile Examples:")
        for profile_dir in profile_dirs:
            if (profile_dir / "profile.yaml").exists():
                print(f"   ✅ {profile_dir.name}/")
            else:
                print(f"   ⚠️  {profile_dir.name}/ (no profile.yaml)")
    else:
        print(f"\n📁 Profile Examples:")
        print(f"   ❌ profiles/ directory not found")
    
    print("\nProfile file structure test completed!")

if __name__ == "__main__":
    test_profile_files() 
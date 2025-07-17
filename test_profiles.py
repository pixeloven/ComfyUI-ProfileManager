#!/usr/bin/env python3
"""
Test script for the profile system
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'ComfyUI-PackManager-React'))

from __init__ import ProfileManager

def test_profile_system():
    """Test the profile management system"""
    print("Testing Profile Management System")
    print("=" * 40)
    
    # Initialize profile manager
    profile_manager = ProfileManager()
    print(f"Profile directory: {profile_manager.profiles_dir}")
    
    # List profiles
    print("\n1. Listing profiles:")
    profiles = profile_manager.list_profiles()
    for profile in profiles:
        print(f"  - {profile['name']}: {profile['config']['description']}")
    
    # Test profile validation
    print("\n2. Validating profiles:")
    for profile in profiles:
        errors = profile_manager.validate_profile(profile['name'])
        status = "✓ Valid" if len(errors) == 0 else f"✗ Invalid ({len(errors)} errors)"
        print(f"  - {profile['name']}: {status}")
        if errors:
            for error in errors:
                print(f"    Error: {error}")
    
    # Test dependency resolution
    print("\n3. Testing dependency resolution:")
    for profile in profiles:
        try:
            deps = profile_manager.resolve_dependencies(profile['name'])
            print(f"  - {profile['name']} dependencies: {list(deps)}")
        except Exception as e:
            print(f"  - {profile['name']} dependency error: {e}")
    
    print("\nProfile system test completed!")

if __name__ == "__main__":
    test_profile_system() 
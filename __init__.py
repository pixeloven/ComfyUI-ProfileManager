import os
import server
from aiohttp import web
import folder_paths
import nodes
import json
import yaml
from pathlib import Path
from typing import Dict, List, Set, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Pack Manager functionality
class ProfileManager:
    def __init__(self, profiles_dir: str = "./profiles"):
        self.profiles_dir = Path(profiles_dir)
        self.active_profiles: Set[str] = set()
        
        if not self.profiles_dir.exists():
            logger.warning(f"Profiles directory {profiles_dir} does not exist")
            self.profiles_dir.mkdir(parents=True, exist_ok=True)
    
    def load_profile_config(self, profile_name: str) -> Dict:
        """Load profile configuration from profile.yaml"""
        profile_path = self.profiles_dir / profile_name / "profile.yaml"
        if not profile_path.exists():
            raise ValueError(f"Profile '{profile_name}' not found at {profile_path}")
            
        try:
            with open(profile_path, 'r') as f:
                config = yaml.safe_load(f)
                logger.info(f"Loaded profile config: {profile_name}")
                return config
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in {profile_path}: {e}")
    
    def resolve_dependencies(self, profile_name: str) -> Set[str]:
        """Resolve all dependencies for a profile"""
        profile_config = self.load_profile_config(profile_name)
        resolved_profiles = set()
        
        # Recursively resolve dependencies
        for dependency in profile_config.get('extends', []):
            if dependency in resolved_profiles:
                logger.warning(f"Circular dependency detected: {dependency}")
                continue
            resolved_profiles.update(self.resolve_dependencies(dependency))
        
        resolved_profiles.add(profile_name)
        logger.info(f"Resolved dependencies for {profile_name}: {resolved_profiles}")
        return resolved_profiles
    
    def list_profiles(self) -> List[Dict]:
        """List all available profiles"""
        profiles = []
        
        if not self.profiles_dir.exists():
            return profiles
            
        for profile_dir in self.profiles_dir.iterdir():
            if profile_dir.is_dir():
                profile_config_file = profile_dir / "profile.yaml"
                if profile_config_file.exists():
                    try:
                        config = self.load_profile_config(profile_dir.name)
                        profiles.append({
                            'name': profile_dir.name,
                            'config': config
                        })
                    except Exception as e:
                        logger.error(f"Error loading profile {profile_dir.name}: {e}")
        
        return profiles
    
    def validate_profile(self, profile_name: str) -> List[str]:
        """Validate a profile and return list of errors"""
        errors = []
        profile_path = self.profiles_dir / profile_name
        
        if not profile_path.exists():
            errors.append(f"Profile directory does not exist: {profile_path}")
            return errors
        
        # Check required files (consolidated structure)
        required_files = ['profile.yaml']
        for required_file in required_files:
            if not (profile_path / required_file).exists():
                errors.append(f"Missing required file: {required_file}")
        
        # Validate YAML files
        for yaml_file in profile_path.glob('*.yaml'):
            try:
                with open(yaml_file, 'r') as f:
                    yaml.safe_load(f)
            except yaml.YAMLError as e:
                errors.append(f"Invalid YAML in {yaml_file.name}: {e}")
        
        # Check for circular dependencies
        try:
            deps = self.resolve_dependencies(profile_name)
            logger.info(f"Profile {profile_name} dependencies: {deps}")
        except Exception as e:
            errors.append(f"Dependency resolution failed: {e}")
        
        return errors
    
    def create_profile(self, profile_name: str, extends: Optional[List[str]] = None) -> bool:
        """Create a new profile with basic structure"""
        profile_path = self.profiles_dir / profile_name
        
        if profile_path.exists():
            logger.error(f"Profile {profile_name} already exists")
            return False
        
        try:
            profile_path.mkdir(parents=True)
            
            # Create profile.yaml
            profile_config = {
                'name': profile_name,
                'version': '1.0.0',
                'description': f'Custom profile: {profile_name}',
                'extends': extends or [],
                'tags': ['custom'],
                'comfyui_version': 'v0.3.43',
                'requirements': {
                    'python': '>=3.10',
                    'gpu': '>=4GB',
                    'storage': '>=20GB'
                },
                'author': 'User',
                'license': 'MIT',
                'created': '2024-01-01',
                'updated': '2024-01-01',
                'models': [],
                'extensions': {
                    'git': [],
                    'pip': []
                }
            }
            
            with open(profile_path / 'profile.yaml', 'w') as f:
                yaml.dump(profile_config, f, default_flow_style=False)
            
            # Create requirements.txt
            with open(profile_path / 'requirements.txt', 'w') as f:
                f.write(f"# Requirements for {profile_name} profile\n")
            
            # Create workflows directory
            (profile_path / 'workflows').mkdir()
            
            logger.info(f"Created profile: {profile_name}")
            return True
            
        except Exception as e:
            logger.error(f"Error creating profile {profile_name}: {e}")
            return False

# Global profile manager instance
profile_manager = ProfileManager()

# API endpoints
async def get_profiles_handler(request):
    """Get list of all available profiles"""
    try:
        profiles = profile_manager.list_profiles()
        return web.json_response({
            'success': True,
            'profiles': profiles
        })
    except Exception as e:
        return web.json_response({
            'success': False,
            'error': str(e)
        }, status=500)

async def get_profile_details_handler(request):
    """Get detailed information about a specific profile"""
    try:
        profile_name = request.match_info['profile_name']
        config = profile_manager.load_profile_config(profile_name)
        deps = profile_manager.resolve_dependencies(profile_name)
        errors = profile_manager.validate_profile(profile_name)
        
        return web.json_response({
            'success': True,
            'profile_name': profile_name,
            'config': config,
            'dependencies': list(deps),
            'valid': len(errors) == 0,
            'errors': errors
        })
    except Exception as e:
        return web.json_response({
            'success': False,
            'error': str(e)
        }, status=500)

async def validate_profile_handler(request):
    """Validate a specific profile"""
    try:
        profile_name = request.match_info['profile_name']
        errors = profile_manager.validate_profile(profile_name)
        return web.json_response({
            'success': True,
            'profile_name': profile_name,
            'valid': len(errors) == 0,
            'errors': errors
        })
    except Exception as e:
        return web.json_response({
            'success': False,
            'error': str(e)
        }, status=500)

async def create_profile_handler(request):
    """Create a new profile"""
    try:
        data = await request.json()
        profile_name = data.get('name')
        extends = data.get('extends', [])
        
        if not profile_name:
            return web.json_response({
                'success': False,
                'error': 'Profile name is required'
            }, status=400)
        
        success = profile_manager.create_profile(profile_name, extends=extends)
        return web.json_response({
            'success': success,
            'profile_name': profile_name,
            'message': f"Profile '{profile_name}' created successfully" if success else f"Failed to create profile '{profile_name}'"
        })
    except Exception as e:
        return web.json_response({
            'success': False,
            'error': str(e)
        }, status=500)

# ComfyUI Extension Setup
NODE_CLASS_MAPPINGS = {}
__all__ = ["NODE_CLASS_MAPPINGS"]

# Define the path to our extension
workspace_path = os.path.dirname(__file__)
dist_path = os.path.join(workspace_path, "dist/pack_manager")
dist_locales_path = os.path.join(workspace_path, "dist/locales")

# Print the current paths for debugging
print(f"ComfyUI Pack Manager workspace path: {workspace_path}")
print(f"Dist path: {dist_path}")
print(f"Dist locales path: {dist_locales_path}")
print(f"Locales exist: {os.path.exists(dist_locales_path)}")

# Register the static route for serving our React app assets
if os.path.exists(dist_path):
    # Add the routes for the extension
    server.PromptServer.instance.app.add_routes([
        web.static("/pack_manager/", dist_path),
    ])

    # Register the locale files route
    if os.path.exists(dist_locales_path):
        server.PromptServer.instance.app.add_routes([
            web.static("/locales/", dist_locales_path),
        ])
        print(f"Registered locale files route at /locales/")
    else:
        print("WARNING: Locale directory not found!")

    # Register API routes
    server.PromptServer.instance.app.add_routes([
        web.get("/pack_manager/api/profiles", get_profiles_handler),
        web.get("/pack_manager/api/profile/{profile_name}", get_profile_details_handler),
        web.post("/pack_manager/api/validate/{profile_name}", validate_profile_handler),
        web.post("/pack_manager/api/create", create_profile_handler),
    ])

    # Also register the standard ComfyUI extension web directory
    project_name = os.path.basename(workspace_path)

    try:
        # Method added in https://github.com/comfyanonymous/ComfyUI/pull/8357
        from comfy_config import config_parser

        project_config = config_parser.extract_node_configuration(workspace_path)
        project_name = project_config.project.name
        print(f"project name read from pyproject.toml: {project_name}")
    except Exception as e:
        print(f"Could not load project config, using default name '{project_name}': {e}")

    nodes.EXTENSION_WEB_DIRS[project_name] = os.path.join(workspace_path, "dist")
    print(f"✅ ComfyUI Pack Manager extension loaded successfully!")
    print(f"   Access the interface at: http://localhost:8188/pack_manager/")
else:
    print("❌ ComfyUI Pack Manager: Web directory not found. Please build the React app first.")
// Profile configuration interface
export interface ProfileConfig {
  name: string;
  version: string;
  description: string;
  extends: string[];
  tags: string[];
  comfyui_version: string;
  requirements: {
    python: string;
    gpu: string;
    storage: string;
  };
  author: string;
  license: string;
  created: string;
  updated: string;
  models: ProfileModel[];
  extensions: {
    git: ProfileGitExtension[];
    pip: ProfilePipExtension[];
  };
}

// Profile model interface
export interface ProfileModel {
  name: string;
  type: string;
  url: string;
  description?: string;
  size?: string;
  checksum?: string;
}

// Git extension interface
export interface ProfileGitExtension {
  name: string;
  url: string;
  branch?: string;
  commit?: string;
}

// Pip extension interface
export interface ProfilePipExtension {
  name: string;
  version: string;
  description?: string;
}

// Profile interface for list view
export interface Profile {
  name: string;
  config: ProfileConfig;
}

// Profile details interface for detailed view
export interface ProfileDetails {
  success: boolean;
  profile_name: string;
  config: ProfileConfig;
  dependencies: string[];
  valid: boolean;
  errors: string[];
}

// API response interfaces
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
}

export interface ProfilesResponse extends ApiResponse<Profile[]> {
  profiles: Profile[];
}

export interface ProfileValidationResponse extends ApiResponse<{
  profile_name: string;
  valid: boolean;
  errors: string[];
}> {
  profile_name: string;
  valid: boolean;
  errors: string[];
}

export interface ProfileCreationResponse extends ApiResponse<{
  profile_name: string;
  message: string;
}> {
  profile_name: string;
  message: string;
} 
import React from 'react';
import { Profile } from '../types';

interface ProfileListProps {
  profiles: Profile[];
  onProfileSelect: (profileName: string) => void;
  onProfileValidate: (profileName: string) => void;
}

const ProfileList: React.FC<ProfileListProps> = ({ profiles, onProfileSelect, onProfileValidate }) => {
  if (profiles.length === 0) {
    return (
      <div className="pack-list-empty">
        <p>No profiles found. Create your first profile!</p>
      </div>
    );
  }

  return (
    <div className="pack-list">
      {profiles.map((profile) => (
        <div key={profile.name} className="pack-item">
          <div className="pack-header">
            <h3>{profile.name}</h3>
            <div className="pack-actions">
              <button 
                className="btn btn-primary"
                onClick={() => onProfileSelect(profile.name)}
              >
                View
              </button>
              <button 
                className="btn btn-secondary"
                onClick={() => onProfileValidate(profile.name)}
              >
                Validate
              </button>
            </div>
          </div>
          <div className="pack-info">
            <p><strong>Description:</strong> {profile.config.description || 'No description'}</p>
            <p><strong>Version:</strong> {profile.config.version}</p>
            <p><strong>Tags:</strong> {profile.config.tags ? profile.config.tags.join(', ') : 'None'}</p>
            {profile.config.extends && profile.config.extends.length > 0 && (
              <p><strong>Extends:</strong> {profile.config.extends.join(', ')}</p>
            )}
          </div>
        </div>
      ))}
    </div>
  );
};

export default ProfileList; 
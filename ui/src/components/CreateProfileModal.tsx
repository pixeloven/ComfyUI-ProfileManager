import React, { useState } from 'react';

interface CreateProfileModalProps {
  onClose: () => void;
  onCreate: (profileName: string, extendsProfiles: string[]) => void;
  existingProfiles: string[];
}

const CreateProfileModal: React.FC<CreateProfileModalProps> = ({ onClose, onCreate, existingProfiles }) => {
  const [profileName, setProfileName] = useState('');
  const [extendsProfiles, setExtendsProfiles] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!profileName.trim()) {
      return;
    }

    const extendsList = extendsProfiles
      .split(',')
      .map(s => s.trim())
      .filter(s => s);

    onCreate(profileName.trim(), extendsList);
  };

  return (
    <div className="modal">
      <div className="modal-content">
        <div className="modal-header">
          <h2>Create New Profile</h2>
          <span className="close-modal" onClick={onClose}>&times;</span>
        </div>
        <div className="modal-body">
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="new-profile-name">Profile Name:</label>
              <input
                type="text"
                id="new-profile-name"
                value={profileName}
                onChange={(e) => setProfileName(e.target.value)}
                placeholder="Enter profile name (e.g., my-custom-profile)"
                required
              />
            </div>
            <div className="form-group">
              <label htmlFor="extends-profiles">Extends (optional):</label>
              <input
                type="text"
                id="extends-profiles"
                value={extendsProfiles}
                onChange={(e) => setExtendsProfiles(e.target.value)}
                placeholder="base,anime (comma-separated)"
              />
              <small>Profiles to inherit from</small>
              {existingProfiles.length > 0 && (
                <small>Available profiles: {existingProfiles.join(', ')}</small>
              )}
            </div>
            <div className="form-actions">
              <button type="submit" className="btn btn-primary">
                Create Profile
              </button>
              <button type="button" className="btn btn-secondary" onClick={onClose}>
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default CreateProfileModal; 
import React from 'react';
import { ProfileDetails as ProfileDetailsType } from '../types';

interface ProfileDetailsProps {
  profile: ProfileDetailsType;
  onClose: () => void;
}

const ProfileDetails: React.FC<ProfileDetailsProps> = ({ profile, onClose }) => {
  const formatModelsList = (models: any[]) => {
    if (!models || models.length === 0) {
      return <p>No models defined</p>;
    }

    return (
      <ul>
        {models.map((model, index) => (
          <li key={index}>
            <strong>{model.name}</strong> ({model.type})
            <br />
            <small>{model.url}</small>
          </li>
        ))}
      </ul>
    );
  };

  const formatExtensionsList = (extensions: any) => {
    if (!extensions) return <p>No extensions defined</p>;

    let html = '';
    
    if (extensions.git && extensions.git.length > 0) {
      html += '<h4>Git Extensions:</h4><ul>';
      extensions.git.forEach((ext: any) => {
        html += `<li><strong>${ext.name}</strong> - ${ext.url}</li>`;
      });
      html += '</ul>';
    }

    if (extensions.pip && extensions.pip.length > 0) {
      html += '<h4>Pip Extensions:</h4><ul>';
      extensions.pip.forEach((ext: any) => {
        html += `<li><strong>${ext.name}</strong> ${ext.version}</li>`;
      });
      html += '</ul>';
    }

    return html || <p>No extensions defined</p>;
  };

  return (
    <div className="pack-details-modal">
      <div className="modal-content large">
        <div className="modal-header">
          <h2>Profile Details</h2>
          <span className="close-modal" onClick={onClose}>&times;</span>
        </div>
        <div className="modal-body">
          <div className="pack-details">
            <h2>{profile.profile_name}</h2>
            
            <div className="detail-section">
              <h3>Configuration</h3>
              <p><strong>Description:</strong> {profile.config.description}</p>
              <p><strong>Version:</strong> {profile.config.version}</p>
              <p><strong>ComfyUI Version:</strong> {profile.config.comfyui_version}</p>
              <p><strong>Author:</strong> {profile.config.author}</p>
              <p><strong>License:</strong> {profile.config.license}</p>
            </div>

            <div className="detail-section">
              <h3>Dependencies</h3>
              <p><strong>Extends:</strong> {profile.config.extends ? profile.config.extends.join(', ') : 'None'}</p>
              <p><strong>Resolved Dependencies:</strong> {profile.dependencies.join(', ')}</p>
            </div>

            <div className="detail-section">
              <h3>Models ({profile.config.models ? profile.config.models.length : 0})</h3>
              {formatModelsList(profile.config.models)}
            </div>

            <div className="detail-section">
              <h3>Extensions</h3>
              {formatExtensionsList(profile.config.extensions)}
            </div>

            <div className="detail-section">
              <h3>Validation</h3>
              <p>
                <strong>Status:</strong> 
                <span className={profile.valid ? 'valid' : 'invalid'}>
                  {profile.valid ? 'Valid' : 'Invalid'}
                </span>
              </p>
              {profile.errors.length > 0 && (
                <>
                  <p><strong>Errors:</strong></p>
                  <ul>
                    {profile.errors.map((error, index) => (
                      <li key={index}>{error}</li>
                    ))}
                  </ul>
                </>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfileDetails; 
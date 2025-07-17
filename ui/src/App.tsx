import { useState, useEffect } from 'react';
import './App.css';
import ProfileList from './components/ProfileList';
import ProfileDetails from './components/ProfileDetails';
import CreateProfileModal from './components/CreateProfileModal';
import { Profile, ProfileDetails as ProfileDetailsType } from './types';

function App() {
  const [profiles, setProfiles] = useState<Profile[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedProfile, setSelectedProfile] = useState<ProfileDetailsType | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [notification, setNotification] = useState<{ message: string; type: 'success' | 'error' } | null>(null);

  // API base URL
  const API_BASE = '/pack_manager/api';

  // Fetch profiles from the API
  const fetchProfiles = async () => {
    try {
      setLoading(true);
      const response = await fetch(`${API_BASE}/profiles`);
      const data = await response.json();
      
      if (data.success) {
        setProfiles(data.profiles);
        setError(null);
      } else {
        setError(data.error || 'Failed to load profiles');
      }
    } catch (err) {
      setError('Network error while loading profiles');
      console.error('Error fetching profiles:', err);
    } finally {
      setLoading(false);
    }
  };

  // Load profiles on component mount
  useEffect(() => {
    fetchProfiles();
  }, []);

  // Show notification
  const showNotification = (message: string, type: 'success' | 'error') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 5000);
  };

  // Handle profile selection
  const handleProfileSelect = async (profileName: string) => {
    try {
      const response = await fetch(`${API_BASE}/profile/${profileName}`);
      const data = await response.json();
      
      if (data.success) {
        setSelectedProfile(data);
      } else {
        showNotification(data.error || 'Failed to load profile details', 'error');
      }
    } catch (err) {
      showNotification('Network error while loading profile details', 'error');
      console.error('Error fetching profile details:', err);
    }
  };

  // Handle profile validation
  const handleProfileValidate = async (profileName: string) => {
    try {
      const response = await fetch(`${API_BASE}/validate/${profileName}`, {
        method: 'POST',
      });
      const data = await response.json();
      
      if (data.success) {
        if (data.valid) {
          showNotification(`Profile '${profileName}' is valid!`, 'success');
        } else {
          showNotification(`Profile '${profileName}' has validation errors: ${data.errors.join(', ')}`, 'error');
        }
      } else {
        showNotification(data.error || 'Validation failed', 'error');
      }
    } catch (err) {
      showNotification('Network error during validation', 'error');
      console.error('Error validating profile:', err);
    }
  };

  // Handle profile creation
  const handleProfileCreate = async (profileName: string, extendsProfiles: string[]) => {
    try {
      const response = await fetch(`${API_BASE}/create`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: profileName,
          extends: extendsProfiles,
        }),
      });
      const data = await response.json();
      
      if (data.success) {
        showNotification(data.message, 'success');
        setShowCreateModal(false);
        // Refresh the profile list
        await fetchProfiles();
      } else {
        showNotification(data.error || 'Failed to create profile', 'error');
      }
    } catch (err) {
      showNotification('Network error while creating profile', 'error');
      console.error('Error creating profile:', err);
    }
  };

  return (
    <div className="pack-manager-app">
      <header className="pack-manager-header">
        <h1>ComfyUI Profile Manager</h1>
        <p>Manage your ComfyUI profiles with ease</p>
      </header>

      <div className="pack-manager-content">
        <div className="toolbar">
          <button 
            className="btn btn-primary"
            onClick={() => setShowCreateModal(true)}
          >
            Create New Profile
          </button>
          <button 
            className="btn btn-secondary"
            onClick={fetchProfiles}
            disabled={loading}
          >
            {loading ? 'Loading...' : 'Refresh'}
          </button>
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {loading ? (
          <div className="loading">
            Loading profiles...
          </div>
        ) : (
          <div className="main-content">
            <div className="pack-list-section">
              <h2>Available Profiles</h2>
              <ProfileList
                profiles={profiles}
                onProfileSelect={handleProfileSelect}
                onProfileValidate={handleProfileValidate}
              />
            </div>

            {selectedProfile && (
              <div className="pack-details-section">
                <ProfileDetails
                  profile={selectedProfile}
                  onClose={() => setSelectedProfile(null)}
                />
              </div>
            )}
          </div>
        )}
      </div>

      {showCreateModal && (
        <CreateProfileModal
          onClose={() => setShowCreateModal(false)}
          onCreate={handleProfileCreate}
          existingProfiles={profiles.map(p => p.name)}
        />
      )}

      {notification && (
        <div className={`notification ${notification.type}`}>
          {notification.message}
        </div>
      )}
    </div>
  );
}

export default App;

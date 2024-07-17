import React from 'react';
import { useNavigate } from 'react-router-dom';
import useLogout from '../hooks/useLogout';
import ProfileImage from './ProfileImage';
import '../styles/UserProfileCard.css';

export default function UserProfileCard({ user, onClose }) {
    const navigate = useNavigate();
    const logout = useLogout();

    const handleLogout = async () => {
        await logout();
        navigate('/');
        onClose();
    };

    return (
        <div className="profile-card">
            <div className="profile-card-header">
                <button onClick={onClose} className="profile-card-close-btn">&times;</button>
            </div>
            <div className="profile-card-body">
                <div className="profile-card-avatar">
                    <ProfileImage name={`${user?.first_name} ${user?.last_name}`} />
                </div>
                <p className="profile-name"><strong>{user?.first_name} {user?.last_name}</strong></p>
                <p className="profile-email">{user?.email}</p>
            </div>
            <div className="profile-card-footer">
                <button type="button" className="btn btn-logout" onClick={handleLogout}>
                    Logout
                </button>
            </div>
        </div>
    );
}

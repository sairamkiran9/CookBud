import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import useAuth from '../../hooks/useAuth';
import useLogout from '../../hooks/useLogout';
import useUser from '../../hooks/useUser';
import '../../styles/User.css';

export default function User() {
    const { user } = useAuth();
    const navigate = useNavigate();
    const logout = useLogout();
    const [loading, setLoading] = useState(false);
    const getUser = useUser();

    useEffect(() => {
        getUser();
    }, [getUser]);

    async function onLogout() {
        setLoading(true);
        await logout();
        navigate('/');
    }

    return (
        <div className="container mt-5 profile-container">
            <div className="profile-header">
                <div className="profile-avatar">
                    <img
                        src={`https://www.gravatar.com/avatar/${user?.email}?s=200`}
                        alt="User Avatar"
                        className="rounded-circle img-fluid"
                    />
                </div>
                <div className="profile-info">
                    <h2 className="profile-username">{user?.username}</h2>
                </div>
            </div>
            <div className="profile-details">
                <p><strong>Email:</strong> {user?.email}</p>
                <p><strong>First Name:</strong> {user?.first_name}</p>
                <p><strong>Last Name:</strong> {user?.last_name}</p>
            </div>
            <div>
                <button
                    disabled={loading}
                    type="button"
                    className="btn btn-outline-danger"
                    onClick={onLogout}
                >
                    {loading ? 'Logging out...' : 'Logout'}
                </button>
            </div>
        </div>
    );
}

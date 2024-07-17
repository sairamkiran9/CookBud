import React, { useState } from "react";
import { NavLink } from "react-router-dom";
import useAuth from "../hooks/useAuth";
import UserProfileCard from "./UserProfileCard";
import ProfileImage from "./ProfileImage";
import '../styles/Navbar.css';

export default function Navbar() {
  const { isLoggedIn, user } = useAuth();
  const [showProfileCard, setShowProfileCard] = useState(false);

  const toggleProfileCard = () => {
    setShowProfileCard(!showProfileCard);
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container-fluid">
        <button
          className="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarSupportedContent"
          aria-controls="navbarSupportedContent"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span className="navbar-toggler-icon"></span>
        </button>
        <div className="collapse navbar-collapse" id="navbarSupportedContent">
          <ul className='navbar-nav me-auto mb-2 mb-lg-0'>
            <li className='nav-item'><NavLink className={'nav-link'} to={'/'}>Home</NavLink></li>
            {isLoggedIn ? (
              <>
                <li className='nav-item'><NavLink className={'nav-link'} to={'/auth/recommendation'}>Explore</NavLink></li>
              </>
            ) : (
              <>
                <li className='nav-item'><NavLink className={'nav-link'} to={'/auth/login'}>Login</NavLink></li>
                <li className='nav-item'><NavLink className={'nav-link'} to={'/auth/register'}>Register</NavLink></li>
              </>
            )}
          </ul>
          {isLoggedIn && (
            <div className="nav-item profile-icon-container">
              <button
                className="profile-icon"
                type="button"
                aria-expanded="false"
                onClick={toggleProfileCard}
              >
                <ProfileImage name={`${user?.first_name} ${user?.last_name}`} />
              </button>
              {showProfileCard && <UserProfileCard user={user} onClose={toggleProfileCard} />}
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}

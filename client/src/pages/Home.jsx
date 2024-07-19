import React from 'react';
import { Link } from 'react-router-dom';
import '../styles/Home.css';

export default function Home() {
    return (
        <div className='home-container'>
            <div className='hero-section'>
                <div className='hero-content'>
                    <h1>Welcome to CookBuddy!</h1>
                    <p>Discover new recipes tailored to the ingredients you have at home.</p>
                    <Link to="auth/recommendation" className='btn btn-primary btn-lg'>
                        Get Started
                    </Link>
                </div>
            </div>
        </div>
    );
}

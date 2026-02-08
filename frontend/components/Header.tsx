'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';

interface HeaderProps {
  appName?: string;
}

const Header: React.FC<HeaderProps> = ({ appName = 'Todo Dashboard' }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const router = useRouter();

  useEffect(() => {
    // Check if user is logged in by checking for token in localStorage
    const token = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
    setIsLoggedIn(!!token);
  }, []);

  const handleLogout = () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
    }
    setIsLoggedIn(false);
    router.push('/login');
    router.refresh();
  };

  return (
    <header className="bg-white border-b border-gray-200 py-4 mb-8">
      <div className="container mx-auto px-4 flex justify-between items-center">
        <div className="text-xl font-bold text-gray-900">{appName}</div>
        <div>
          {isLoggedIn ? (
            <div className="flex items-center space-x-4">
              <span className="text-gray-700">Welcome!</span>
              <button
                onClick={handleLogout}
                className="text-red-600 hover:text-red-800"
              >
                Logout
              </button>
            </div>
          ) : (
            <div className="flex items-center space-x-4">
              <a href="/login" className="text-indigo-600 hover:text-indigo-800">
                Login
              </a>
              <span className="text-gray-400">|</span>
              <a href="/register" className="text-indigo-600 hover:text-indigo-800">
                Sign Up
              </a>
            </div>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
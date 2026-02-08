import React from 'react';
import { render, screen } from '@testing-library/react';
import Header from '@/components/Header';

describe('Header Component', () => {
  test('renders app name correctly', () => {
    render(<Header appName="Test App" />);
    expect(screen.getByText('Test App')).toBeInTheDocument();
  });

  test('renders default app name when not provided', () => {
    render(<Header />);
    expect(screen.getByText('Todo Dashboard')).toBeInTheDocument();
  });

  test('renders user actions when provided', () => {
    const userActions = <div>Custom Actions</div>;
    render(<Header userActions={userActions} />);
    expect(screen.getByText('Custom Actions')).toBeInTheDocument();
  });

  test('renders default user actions when not provided', () => {
    render(<Header />);
    expect(screen.getByText('Login')).toBeInTheDocument();
    expect(screen.getByText('Sign Up')).toBeInTheDocument();
  });
});
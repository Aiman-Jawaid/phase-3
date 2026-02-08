import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import EmptyState from '@/components/EmptyState';

describe('EmptyState Component', () => {
  test('renders empty state text', () => {
    render(<EmptyState />);

    expect(screen.getByText('No todos yet')).toBeInTheDocument();
    expect(screen.getByText('Get started by creating your first task')).toBeInTheDocument();
  });

  test('renders add task button', () => {
    render(<EmptyState />);

    const addButton = screen.getByRole('button', { name: /Add Task/i });
    expect(addButton).toBeInTheDocument();
  });

  test('renders task icon', () => {
    render(<EmptyState />);

    // Check if the SVG element is present (the task icon)
    const icon = screen.getByRole('img');
    expect(icon).toBeInTheDocument();
  });

  test('button has correct styling', () => {
    render(<EmptyState />);

    const addButton = screen.getByRole('button', { name: /Add Task/i });
    expect(addButton).toHaveClass('bg-indigo-600');
  });
});
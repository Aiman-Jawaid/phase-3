import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import TasksArea from '@/components/TasksArea';
import { Task } from '@/lib/types';

describe('TasksArea Component', () => {
  const mockTasks: Task[] = [
    {
      id: 1,
      title: 'Test Task 1',
      completed: false,
      createdAt: '2026-01-09T10:00:00Z',
      updatedAt: '2026-01-09T10:00:00Z',
      userId: 1
    },
    {
      id: 2,
      title: 'Test Task 2',
      completed: true,
      createdAt: '2026-01-09T10:00:00Z',
      updatedAt: '2026-01-09T10:00:00Z',
      userId: 1
    }
  ];

  test('renders tasks when tasks are provided', () => {
    render(<TasksArea tasks={mockTasks} />);
    expect(screen.getByText('Test Task 1')).toBeInTheDocument();
    expect(screen.getByText('Test Task 2')).toBeInTheDocument();
  });

  test('renders empty state when no tasks are provided', () => {
    render(<TasksArea tasks={[]} />);
    expect(screen.getByText('No todos yet')).toBeInTheDocument();
  });

  test('calls onTaskToggle when checkbox is clicked', () => {
    const mockToggle = jest.fn();
    render(<TasksArea tasks={mockTasks} onTaskToggle={mockToggle} />);

    const checkbox = screen.getByRole('checkbox', { name: '' });
    fireEvent.click(checkbox);

    expect(mockToggle).toHaveBeenCalledWith(1);
  });

  test('calls onTaskDelete when delete button is clicked', () => {
    const mockDelete = jest.fn();
    render(<TasksArea tasks={mockTasks} onTaskDelete={mockDelete} />);

    const deleteButton = screen.getByText('Delete');
    fireEvent.click(deleteButton);

    expect(mockDelete).toHaveBeenCalledWith(1);
  });
});
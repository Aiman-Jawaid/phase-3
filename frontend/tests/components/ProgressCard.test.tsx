import React from 'react';
import { render, screen } from '@testing-library/react';
import ProgressCard from '@/components/ProgressCard';

describe('ProgressCard Component', () => {
  test('displays correct task counts', () => {
    render(<ProgressCard totalTasks={5} completedTasks={2} />);

    expect(screen.getByText('2 / 5')).toBeInTheDocument();
    expect(screen.getByText('40%')).toBeInTheDocument(); // 2/5 = 40%
  });

  test('handles zero tasks correctly', () => {
    render(<ProgressCard totalTasks={0} completedTasks={0} />);

    expect(screen.getByText('0 / 0')).toBeInTheDocument();
    expect(screen.getByText('0%')).toBeInTheDocument(); // 0/0 = 0%
  });

  test('calculates percentage correctly', () => {
    render(<ProgressCard totalTasks={4} completedTasks={3} />);

    expect(screen.getByText('3 / 4')).toBeInTheDocument();
    expect(screen.getByText('75%')).toBeInTheDocument(); // 3/4 = 75%
  });

  test('renders daily progress title', () => {
    render(<ProgressCard totalTasks={3} completedTasks={1} />);

    expect(screen.getByText('Daily Progress')).toBeInTheDocument();
  });
});
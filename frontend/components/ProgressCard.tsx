'use client';

import React from 'react';

interface ProgressCardProps {
  totalTasks: number;
  completedTasks: number;
}

const ProgressCard: React.FC<ProgressCardProps> = ({
  totalTasks,
  completedTasks
}) => {
  const progressPercentage = totalTasks > 0
    ? Math.round((completedTasks / totalTasks) * 100)
    : 0;

  return (
    <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-xl shadow-md p-6 mb-6 text-white">
      <h2 className="text-lg font-semibold mb-2">Daily Progress</h2>
      <div className="flex items-center justify-between">
        <div>
          <p className="text-3xl font-bold">{completedTasks} / {totalTasks}</p>
          <p className="text-indigo-100">Completed Tasks</p>
        </div>
        <div className="text-right">
          <div className="text-2xl font-bold">{progressPercentage}%</div>
          <p className="text-indigo-100">Complete</p>
        </div>
      </div>
      <div className="mt-4">
        <div className="w-full bg-indigo-400 rounded-full h-2.5">
          <div
            className="bg-white h-2.5 rounded-full transition-all duration-500 ease-out"
            style={{ width: `${progressPercentage}%` }}
          ></div>
        </div>
      </div>
    </div>
  );
};

export default ProgressCard;
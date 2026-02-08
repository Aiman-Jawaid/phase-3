'use client';

import React, { useState } from 'react';
import { Task } from '@/lib/types';
import EmptyState from './EmptyState';

interface TasksAreaProps {
  tasks?: Task[];
  onTaskToggle?: (taskId: string | number) => void;
  onTaskDelete?: (taskId: string | number) => void;
  onAddTask?: (taskData: { title: string; description?: string }) => void;
}

const TasksArea: React.FC<TasksAreaProps> = ({
  tasks = [],
  onTaskToggle,
  onTaskDelete,
  onAddTask
}) => {
  const [newTaskTitle, setNewTaskTitle] = useState('');
  const [newTaskDescription, setNewTaskDescription] = useState('');
  const [isAdding, setIsAdding] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!newTaskTitle.trim()) return;

    onAddTask?.({
      title: newTaskTitle.trim(),
      description: newTaskDescription.trim() || undefined
    });

    setNewTaskTitle('');
    setNewTaskDescription('');
    setIsAdding(false);
  };

  const hasTasks = tasks.length > 0;

  return (
    <div className="bg-white rounded-xl shadow-sm p-6">
      {/* Add Task Form */}
      <div className="mb-6">
        {!isAdding ? (
          <button
            onClick={() => setIsAdding(true)}
            className="w-full py-3 px-4 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition-colors text-center"
          >
            + Add New Task
          </button>
        ) : (
          <form onSubmit={handleSubmit} className="border border-gray-200 rounded-lg p-4 mb-4">
            <div className="mb-3">
              <input
                type="text"
                value={newTaskTitle}
                onChange={(e) => setNewTaskTitle(e.target.value)}
                placeholder="Task title..."
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                autoFocus
              />
            </div>
            <div className="mb-3">
              <textarea
                value={newTaskDescription}
                onChange={(e) => setNewTaskDescription(e.target.value)}
                placeholder="Description (optional)..."
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                rows={2}
              />
            </div>
            <div className="flex space-x-2">
              <button
                type="submit"
                className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
              >
                Add Task
              </button>
              <button
                type="button"
                onClick={() => {
                  setIsAdding(false);
                  setNewTaskTitle('');
                  setNewTaskDescription('');
                }}
                className="px-4 py-2 bg-gray-300 text-gray-700 rounded-md hover:bg-gray-400"
              >
                Cancel
              </button>
            </div>
          </form>
        )}
      </div>

      {hasTasks ? (
        <div className="space-y-4">
          {tasks.map((task) => (
            <div
              key={task.id}
              className={`border rounded-lg p-4 flex items-center justify-between ${
                task.completed
                  ? 'bg-green-50 border-green-200'
                  : 'bg-white border-gray-200'
              }`}
            >
              <div className="flex items-center">
                <input
                  type="checkbox"
                  checked={task.completed}
                  onChange={() => onTaskToggle?.(task.id)}
                  className="h-5 w-5 text-indigo-600 rounded mr-3"
                />
                <div>
                  <h3 className={`font-medium ${
                    task.completed
                      ? 'text-gray-500 line-through'
                      : 'text-gray-900'
                  }`}>
                    {task.title}
                  </h3>
                  {task.description && (
                    <p className={`text-sm ${
                      task.completed
                        ? 'text-gray-400 line-through'
                        : 'text-gray-600'
                    }`}>
                      {task.description}
                    </p>
                  )}
                </div>
              </div>
              <button
                onClick={() => onTaskDelete?.(task.id)}
                className="text-red-500 hover:text-red-700"
              >
                Delete
              </button>
            </div>
          ))}
        </div>
      ) : (
        <EmptyState />
      )}
    </div>
  );
};

export default TasksArea;
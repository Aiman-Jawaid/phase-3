'use client';

import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import Header from '@/components/Header';
import PageTitleSection from '@/components/PageTitleSection';
import TasksArea from '@/components/TasksArea';
import ProgressCard from '@/components/ProgressCard';
import ChatbotIcon from '@/components/chatbot-icon';
import ChatPanel from '@/components/chat-panel';
import { Task } from '@/lib/types';
import { apiClient } from '@/lib/api';

const DashboardPage: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);
  const [isChatPanelOpen, setIsChatPanelOpen] = useState(false);
  const router = useRouter();

  useEffect(() => {
    const handleToggleChatPanel = (event: any) => {
      setIsChatPanelOpen(event.detail.isOpen);
    };

    window.addEventListener('toggleChatPanel', handleToggleChatPanel);

    return () => {
      window.removeEventListener('toggleChatPanel', handleToggleChatPanel);
    };
  }, []);

  useEffect(() => {
    const fetchTasks = async () => {
      try {
        const response = await apiClient.get<Task[]>('/api/tasks');
        if (response.success && response.data) {
          setTasks(response.data);
        } else {
          // Check if the error is related to authentication
          if (response.error && (response.error.includes('401') || response.error.includes('Unauthorized') || response.error.includes('403'))) {
            // Redirect to login if not authenticated
            router.push('/login');
          } else {
            console.error('Failed to fetch tasks:', response.error);
          }
        }
      } catch (error) {
        // Handle network errors or other issues
        if (error instanceof Error && (error.message.includes('401') || error.message.includes('Unauthorized') || error.message.includes('403'))) {
          // Redirect to login if not authenticated
          router.push('/login');
        } else {
          console.error('Failed to fetch tasks:', error);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchTasks();
  }, [router]);

  const toggleTaskCompletion = async (taskId: string | number) => {
    try {
      const response = await apiClient.patch(`/api/tasks/${taskId}/complete`, {
        completed: !tasks.find(task => task.id === taskId)?.completed
      });

      if (response.success && response.data) {
        setTasks(prevTasks =>
          prevTasks.map(task =>
            task.id === taskId
              ? {
                  ...task,
                  completed: !task.completed,
                  updatedAt: new Date().toISOString()
                }
              : task
          )
        );
      }
    } catch (error) {
      console.error('Failed to toggle task completion:', error);
    }
  };

  const deleteTask = async (taskId: string | number) => {
    try {
      const response = await apiClient.delete(`/api/tasks/${taskId}`);

      if (response.success) {
        setTasks(prevTasks => prevTasks.filter(task => task.id !== taskId));
      }
    } catch (error) {
      console.error('Failed to delete task:', error);
    }
  };

  const addTask = async (taskData: { title: string; description?: string }) => {
    try {
      const response = await apiClient.post('/api/tasks', taskData);

      if (response.success && response.data) {
        setTasks(prevTasks => [...prevTasks, response.data]);
      }
    } catch (error) {
      console.error('Failed to add task:', error);
    }
  };

  const completedTasksCount = tasks.filter(task => task.completed).length;

  if (loading) {
    return (
      <div className="min-h-screen bg-light-gray flex items-center justify-center">
        <div className="text-lg text-gray-600">Loading tasks...</div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-light-gray">
      <Header />
      <main className="container mx-auto px-4 py-2">
        <PageTitleSection />

        <ProgressCard
          totalTasks={tasks.length}
          completedTasks={completedTasksCount}
        />

        <TasksArea
          tasks={tasks}
          onTaskToggle={toggleTaskCompletion}
          onTaskDelete={deleteTask}
          onAddTask={addTask}
        />
      </main>

      {/* Chatbot components */}
      <ChatbotIcon />
      <ChatPanel
        isOpen={isChatPanelOpen}
        onClose={() => setIsChatPanelOpen(false)}
      />
    </div>
  );
};

export default DashboardPage;
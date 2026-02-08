// TypeScript types for Task and User entities

export interface User {
  id: string | number;
  email: string;
  name: string;
  createdAt: string; // ISO date string
}

export interface Task {
  id: string | number;
  title: string;
  description?: string;
  completed: boolean;
  createdAt: string; // ISO date string
  updatedAt: string; // ISO date string
  userId: string | number;
}

export interface TaskFormData {
  title: string;
  description?: string;
  completed: boolean;
}
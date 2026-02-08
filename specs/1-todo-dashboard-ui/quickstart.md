# Quickstart: Todo Dashboard UI Development

## Prerequisites
- Node.js 18+ installed
- npm or yarn package manager
- Basic knowledge of Next.js and TypeScript

## Setup Steps

1. **Install dependencies**:
   ```bash
   npm install next react react-dom typescript @types/react @types/node @types/react-dom tailwindcss postcss autoprefixer
   ```

2. **Initialize Tailwind CSS**:
   ```bash
   npx tailwindcss init -p
   ```

3. **Configure Tailwind** (tailwind.config.js):
   ```js
   /** @type {import('tailwindcss').Config} */
   module.exports = {
     content: [
       "./app/**/*.{js,ts,jsx,tsx}",
       "./components/**/*.{js,ts,jsx,tsx}",
     ],
     theme: {
       extend: {
         colors: {
           primary: {
             500: '#6366f1', // indigo
           },
         },
       },
     },
     plugins: [],
   }
   ```

4. **Setup global CSS** (app/globals.css):
   ```css
   @tailwind base;
   @tailwind components;
   @tailwind utilities;
   ```

## Component Structure
The dashboard consists of 5 main components:
- `Header`: Navigation and user actions
- `PageTitleSection`: Title and add task button
- `ProgressCard`: Daily progress visualization
- `TasksArea`: Container for task cards
- `EmptyState`: Display when no tasks exist

## API Integration
All API calls should go through `/lib/api.ts` following the centralized API client pattern. Remember to attach JWT tokens to all authenticated requests.

## Development Commands
- `npm run dev`: Start development server
- `npm run build`: Build for production
- `npm run start`: Start production server
- `npm run lint`: Run linter
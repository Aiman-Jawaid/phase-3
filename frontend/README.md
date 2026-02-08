# Todo Dashboard Frontend

A clean, professional todo dashboard application built with Next.js 16+, TypeScript, and Tailwind CSS.

## Features

- Clean, professional dashboard UI
- Task management with completion status
- Daily progress tracking
- Responsive design for desktop and tablet
- Empty state handling

## Tech Stack

- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- React Server Components

## Getting Started

First, install the dependencies:

```bash
cd frontend
npm install
```

Then, run the development server:

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the dashboard.

## Running Tests

To run the component tests:

```bash
npm run test
```

To run tests in watch mode:

```bash
npm run test:watch
```

## Project Structure

```text
frontend/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   └── globals.css
├── components/
│   ├── Header.tsx
│   ├── PageTitleSection.tsx
│   ├── ProgressCard.tsx
│   ├── TasksArea.tsx
│   └── EmptyState.tsx
├── lib/
│   ├── api.ts
│   └── types.ts
└── public/
```

## API Integration

The application is configured to work with a JWT-secured API. The API client is located in `lib/api.ts`.

## Environment Variables

Create a `.env.local` file in the root of the frontend directory:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Learn More

To learn more about the technologies used in this project, check out the following resources:

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [TypeScript Documentation](https://www.typescriptlang.org/docs/)
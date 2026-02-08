import type { NextConfig } from 'next';

const nextConfig: NextConfig = {
  reactStrictMode: true,
  experimental: {
    // Set the root directory to avoid the workspace warning
    turbopack: {
      root: process.cwd(),
    },
  },
  env: {
    // Explicitly set the port
    PORT: process.env.PORT || '3000',
  },
};

export default nextConfig;
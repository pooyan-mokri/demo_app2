/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'standalone',
  experimental: {
    typedRoutes: true,
    serverActions: true
  },
  reactStrictMode: true,
};

export default nextConfig;

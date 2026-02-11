import type { NextConfig } from "next";

const isProd = process.env.NODE_ENV === 'production'


const nextConfig: NextConfig = {
  output: 'export',
  basePath: isProd ? '/mosaic' : '',      // only for GitHub Pages
  assetPrefix: isProd ? '/mosaic' : '',
};

// module.exports = nextConfig

export default nextConfig;

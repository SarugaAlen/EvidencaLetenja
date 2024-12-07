import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/vite-plugin-svelte';

const config = {
  preprocess: vitePreprocess(),

  kit: {
    adapter: adapter({
      // Specify the output directory where the server-side build should go
      out: 'build', // Default output directory for the server build
    }),
    paths: {
      base: '',
      assets: '',
    },
    alias: {
      '@/*': 'src/lib/*',
    },
  },
};

export default config;

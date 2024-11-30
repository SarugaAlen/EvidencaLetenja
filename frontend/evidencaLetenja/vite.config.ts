import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vitest/config';

export default defineConfig({
	plugins: [sveltekit()],

	test: {
		globals: true,
		environment: 'jsdom',
		setupFiles: './test-setup.js'
	},

	resolve: process.env.VITEST
		? {
				conditions: ['browser']
			}
		: undefined
});

import { defineConfig } from 'astro/config';
import sitemap from '@astrojs/sitemap';

const site = 'https://thebighauler.com';

export default defineConfig({
  site,
  output: 'static',
  integrations: [sitemap()],
  markdown: {
    shikiConfig: { theme: 'github-light' },
  },
});

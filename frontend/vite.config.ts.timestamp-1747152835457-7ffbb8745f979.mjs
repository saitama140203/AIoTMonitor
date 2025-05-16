// vite.config.ts
import { fileURLToPath, URL } from "node:url";
import vue from "file:///Users/lethephu/PycharmProjects/AIoTMonitor/frontend/node_modules/@vitejs/plugin-vue/dist/index.mjs";
import vueJsx from "file:///Users/lethephu/PycharmProjects/AIoTMonitor/frontend/node_modules/@vitejs/plugin-vue-jsx/dist/index.mjs";
import autoprefixer from "file:///Users/lethephu/PycharmProjects/AIoTMonitor/frontend/node_modules/autoprefixer/lib/autoprefixer.js";
import tailwind from "file:///Users/lethephu/PycharmProjects/AIoTMonitor/frontend/node_modules/tailwindcss/lib/index.js";
import AutoImport from "file:///Users/lethephu/PycharmProjects/AIoTMonitor/frontend/node_modules/unplugin-auto-import/dist/vite.js";
import Components from "file:///Users/lethephu/PycharmProjects/AIoTMonitor/frontend/node_modules/unplugin-vue-components/dist/vite.js";
import { defineConfig } from "file:///Users/lethephu/PycharmProjects/AIoTMonitor/frontend/node_modules/vite/dist/node/index.js";
import Pages from "file:///Users/lethephu/PycharmProjects/AIoTMonitor/frontend/node_modules/vite-plugin-pages/dist/index.js";
import Layouts from "file:///Users/lethephu/PycharmProjects/AIoTMonitor/frontend/node_modules/vite-plugin-vue-layouts/dist/index.mjs";
import svgLoader from "file:///Users/lethephu/PycharmProjects/AIoTMonitor/frontend/node_modules/vite-svg-loader/index.js";
var __vite_injected_original_import_meta_url = "file:///Users/lethephu/PycharmProjects/AIoTMonitor/frontend/vite.config.ts";
var vite_config_default = defineConfig({
  css: {
    postcss: {
      plugins: [tailwind(), autoprefixer()]
    }
  },
  plugins: [
    AutoImport({
      imports: [
        "vue",
        "vue-router"
      ],
      resolvers: []
    }),
    vue(),
    vueJsx(),
    Components({ dts: true }),
    Pages(),
    Layouts(),
    svgLoader()
  ],
  resolve: {
    alias: {
      "@": fileURLToPath(new URL("./src", __vite_injected_original_import_meta_url))
    }
  }
});
export {
  vite_config_default as default
};
//# sourceMappingURL=data:application/json;base64,ewogICJ2ZXJzaW9uIjogMywKICAic291cmNlcyI6IFsidml0ZS5jb25maWcudHMiXSwKICAic291cmNlc0NvbnRlbnQiOiBbImNvbnN0IF9fdml0ZV9pbmplY3RlZF9vcmlnaW5hbF9kaXJuYW1lID0gXCIvVXNlcnMvbGV0aGVwaHUvUHljaGFybVByb2plY3RzL0FJb1RNb25pdG9yL2Zyb250ZW5kXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ZpbGVuYW1lID0gXCIvVXNlcnMvbGV0aGVwaHUvUHljaGFybVByb2plY3RzL0FJb1RNb25pdG9yL2Zyb250ZW5kL3ZpdGUuY29uZmlnLnRzXCI7Y29uc3QgX192aXRlX2luamVjdGVkX29yaWdpbmFsX2ltcG9ydF9tZXRhX3VybCA9IFwiZmlsZTovLy9Vc2Vycy9sZXRoZXBodS9QeWNoYXJtUHJvamVjdHMvQUlvVE1vbml0b3IvZnJvbnRlbmQvdml0ZS5jb25maWcudHNcIjtpbXBvcnQgeyBmaWxlVVJMVG9QYXRoLCBVUkwgfSBmcm9tICdub2RlOnVybCdcblxuaW1wb3J0IHZ1ZSBmcm9tICdAdml0ZWpzL3BsdWdpbi12dWUnXG5pbXBvcnQgdnVlSnN4IGZyb20gJ0B2aXRlanMvcGx1Z2luLXZ1ZS1qc3gnXG5pbXBvcnQgYXV0b3ByZWZpeGVyIGZyb20gJ2F1dG9wcmVmaXhlcidcbmltcG9ydCB0YWlsd2luZCBmcm9tICd0YWlsd2luZGNzcydcbmltcG9ydCBBdXRvSW1wb3J0IGZyb20gJ3VucGx1Z2luLWF1dG8taW1wb3J0L3ZpdGUnXG5pbXBvcnQgQ29tcG9uZW50cyBmcm9tICd1bnBsdWdpbi12dWUtY29tcG9uZW50cy92aXRlJ1xuaW1wb3J0IHsgZGVmaW5lQ29uZmlnIH0gZnJvbSAndml0ZSdcbmltcG9ydCBQYWdlcyBmcm9tICd2aXRlLXBsdWdpbi1wYWdlcydcbmltcG9ydCBMYXlvdXRzIGZyb20gJ3ZpdGUtcGx1Z2luLXZ1ZS1sYXlvdXRzJ1xuaW1wb3J0IHN2Z0xvYWRlciBmcm9tICd2aXRlLXN2Zy1sb2FkZXInXG4vLyBodHRwczovL3ZpdGUuZGV2L2NvbmZpZy9cbmV4cG9ydCBkZWZhdWx0IGRlZmluZUNvbmZpZyh7XG4gIGNzczoge1xuICAgIHBvc3Rjc3M6IHtcbiAgICAgIHBsdWdpbnM6IFt0YWlsd2luZCgpLCBhdXRvcHJlZml4ZXIoKV0sXG4gICAgfSxcbiAgfSxcbiAgcGx1Z2luczogW1xuICAgIEF1dG9JbXBvcnQoe1xuICAgICAgaW1wb3J0czogW1xuICAgICAgICAndnVlJyxcbiAgICAgICAgJ3Z1ZS1yb3V0ZXInLFxuICAgICAgXSxcbiAgICAgIHJlc29sdmVyczogW10sXG4gICAgfSksXG4gICAgdnVlKCksXG4gICAgdnVlSnN4KCksXG4gICAgQ29tcG9uZW50cyh7IGR0czogdHJ1ZSB9KSxcbiAgICBQYWdlcygpLFxuICAgIExheW91dHMoKSxcbiAgICBzdmdMb2FkZXIoKSxcbiAgXSxcbiAgcmVzb2x2ZToge1xuICAgIGFsaWFzOiB7XG4gICAgICAnQCc6IGZpbGVVUkxUb1BhdGgobmV3IFVSTCgnLi9zcmMnLCBpbXBvcnQubWV0YS51cmwpKSxcbiAgICB9LFxuICB9LFxufSlcbiJdLAogICJtYXBwaW5ncyI6ICI7QUFBOFUsU0FBUyxlQUFlLFdBQVc7QUFFalgsT0FBTyxTQUFTO0FBQ2hCLE9BQU8sWUFBWTtBQUNuQixPQUFPLGtCQUFrQjtBQUN6QixPQUFPLGNBQWM7QUFDckIsT0FBTyxnQkFBZ0I7QUFDdkIsT0FBTyxnQkFBZ0I7QUFDdkIsU0FBUyxvQkFBb0I7QUFDN0IsT0FBTyxXQUFXO0FBQ2xCLE9BQU8sYUFBYTtBQUNwQixPQUFPLGVBQWU7QUFYMEwsSUFBTSwyQ0FBMkM7QUFhalEsSUFBTyxzQkFBUSxhQUFhO0FBQUEsRUFDMUIsS0FBSztBQUFBLElBQ0gsU0FBUztBQUFBLE1BQ1AsU0FBUyxDQUFDLFNBQVMsR0FBRyxhQUFhLENBQUM7QUFBQSxJQUN0QztBQUFBLEVBQ0Y7QUFBQSxFQUNBLFNBQVM7QUFBQSxJQUNQLFdBQVc7QUFBQSxNQUNULFNBQVM7QUFBQSxRQUNQO0FBQUEsUUFDQTtBQUFBLE1BQ0Y7QUFBQSxNQUNBLFdBQVcsQ0FBQztBQUFBLElBQ2QsQ0FBQztBQUFBLElBQ0QsSUFBSTtBQUFBLElBQ0osT0FBTztBQUFBLElBQ1AsV0FBVyxFQUFFLEtBQUssS0FBSyxDQUFDO0FBQUEsSUFDeEIsTUFBTTtBQUFBLElBQ04sUUFBUTtBQUFBLElBQ1IsVUFBVTtBQUFBLEVBQ1o7QUFBQSxFQUNBLFNBQVM7QUFBQSxJQUNQLE9BQU87QUFBQSxNQUNMLEtBQUssY0FBYyxJQUFJLElBQUksU0FBUyx3Q0FBZSxDQUFDO0FBQUEsSUFDdEQ7QUFBQSxFQUNGO0FBQ0YsQ0FBQzsiLAogICJuYW1lcyI6IFtdCn0K

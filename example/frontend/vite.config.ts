import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import typesyncPlugin from "rollup-plugin-typesync";

// https://vite.dev/config/
export default defineConfig({
    plugins: [
        react(),
        typesyncPlugin({
            outDir: "src/flask_urls",
            backendRoot: "../backend"
        })
    ],
    server: {
        cors: true,
    }
});

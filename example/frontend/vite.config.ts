import { defineConfig } from "vite";
import typesyncPlugin from "rollup-plugin-typesync";
import react from "@vitejs/plugin-react";


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

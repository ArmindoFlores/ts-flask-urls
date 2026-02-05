# Typesync (Rollup plugin)

`rollup-plugin-typesync` is a Rollup plugin to automatically generate TypeScript types and client-side request helpers directly from a Flask application. It requires the [typesync](https://github.com/ArmindoFlores/typesync) Python package to be installed and configured in your Flask backend.

## Installation
You can install this plugin using `npm install rollup-plugin-typesync`.

## Usage
To enable this plugin, add the following to your `vite.config.ts`:

```typescript
import { defineConfig } from "vite";
import typesyncPlugin from "rollup-plugin-typesync";


export default defineConfig({
    plugins: [
        typesyncPlugin({
            outDir: "src/flask_urls",  // The directory to place the generated TypesScript code in
            backendRoot: "../backend"  // The directory where your Flask entry point lives
        })
    ]
});
```

## Configuration
Currently, additional configuration is not possible, but the goal is to support every command line flag avilable when running `flask typesync generate`.

import PATH from "path"
import tailwindcss from "@tailwindcss/vite"
import { defineConfig } from "vite"

export default defineConfig({
    build: {
        outDir: PATH.resolve(__dirname, 'app/static/src/'),
        emptyOutDir: true,
        rollupOptions: {
            input: {
                "main": PATH.resolve(__dirname, "src/main.ts")
            },
            output: {
                entryFileNames: "[name].js"
            }
        }
    },
    plugins: [
        tailwindcss(),
    ],
    server: {
        proxy: {}
    }
})
import { Plugin, PluginContext } from "rollup";
import { spawn, SpawnOptionsWithoutStdio } from "node:child_process";
import path from "node:path";
import fg from "fast-glob";

export interface TypesyncPluginOptions {
    outDir: string;
    backendRoot: string;
}

async function aspawn(command: string, args: readonly string[] | undefined, options?: SpawnOptionsWithoutStdio | undefined): Promise<{status: number|null, output: string}> {
    const child = spawn(command, args, options);
    let output = "";
    const status = await new Promise<number|null>(resolve => {
        for (const stream of [child.stderr, child.stdout]) {
            stream.on("data", (chunk: string) => output += chunk);
        }
        child.on("close", code => resolve(code));
        child.on("exit", code => resolve(code));
    });
    return { status, output };
}

async function runCodegen(this: PluginContext, options: TypesyncPluginOptions) {
    const {
        backendRoot,
        outDir,
    } = options;

    const result = await aspawn(
        "flask",
        [
            "typesync",
            "generate",
            path.resolve(outDir),
        ],
        {
            cwd: path.resolve(backendRoot),
            shell: process.platform === "win32",
        }
    );

    for (const line of result.output.split("\n")) {
        if (line.startsWith("Warning: ")) {
            this.warn(line.substring(9));
        }
    }

    if (result.status !== 0) {
       this.warn(`codegen failed with status ${result.status}`);
    }
    else {
        this.info("codegen finished")
    }
}

export default function TypesyncPlugin(options: TypesyncPluginOptions): Plugin {
    return {
        name: "typesync",
        async buildStart() {
            const files = await fg(path.join(options.backendRoot, "*"), {
                dot: true,
                absolute: true,
                onlyFiles: true,
            });
            for (const file of files) {
                this.addWatchFile(file);
            }
            await runCodegen.call(this, options);
        },
        async watchChange(id) {
            if (!id.startsWith(path.resolve(options.backendRoot))) return;
            await runCodegen.call(this, options);
        }
    };
}

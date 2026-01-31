import type { RequestOptions } from "./flask_urls/types";
import { makeAPI } from "./flask_urls/apis";

const BASE_ENDPOINT = "http://127.0.0.1:5000";

function join(s1: string, s2: string) {
    let path = s1;
    if (s1.endsWith("/") && s2.startsWith("/")) {
        path += s2.substring(1);
    }
    else if (!s1.endsWith("/") && !s2.startsWith("/")) {
        path += "/" + s2;
    }
    else {
        path += s2;
    }
    return path;
}

function makeHeadersObject(headers: Record<string, string> | undefined) {
    const headersObj = new Headers();
    for (const [key, value] of Object.entries(headers ?? {})) {
        headersObj.append(key, value);
    }
    return headersObj;
}

async function requestFn(endpoint: string, options: RequestOptions) {
    const headers = makeHeadersObject(options.headers);
    headers.append("Content-Type", "application/json");
    const req = await fetch(
        join(BASE_ENDPOINT, endpoint),
        { method: options.method, headers }
    );
    return await req.json();
}

export const API = makeAPI(requestFn);

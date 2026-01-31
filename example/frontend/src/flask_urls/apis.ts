import * as types from "./types";

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function buildUrl(rule: string, params: Record<string, any>) {
    return rule.replace(/<([a-zA-Z_]+[a-zA-Z_0-9]*)>/, (_, key) => {
        return String(params[key]);
    });
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type RequestFunction = (endpoint: string, method: string) => Promise<any>;

export function makeAPI(requestFn: RequestFunction) {
    async function headStatic(params: types.StaticArgsType): Promise<types.StaticReturnType> {
        const endpoint = buildUrl("/static/<filename>", params);
        return await requestFn(endpoint, "HEAD");
    }

    async function optionsStatic(params: types.StaticArgsType): Promise<types.StaticReturnType> {
        const endpoint = buildUrl("/static/<filename>", params);
        return await requestFn(endpoint, "OPTIONS");
    }

    async function getStatic(params: types.StaticArgsType): Promise<types.StaticReturnType> {
        const endpoint = buildUrl("/static/<filename>", params);
        return await requestFn(endpoint, "GET");
    }

    async function headMain(): Promise<types.MainReturnType> {
        const endpoint = "/main";
        return await requestFn(endpoint, "HEAD");
    }

    async function optionsMain(): Promise<types.MainReturnType> {
        const endpoint = "/main";
        return await requestFn(endpoint, "OPTIONS");
    }

    async function postMain(): Promise<types.MainReturnType> {
        const endpoint = "/main";
        return await requestFn(endpoint, "POST");
    }

    async function getMain(): Promise<types.MainReturnType> {
        const endpoint = "/main";
        return await requestFn(endpoint, "GET");
    }

    async function headComplex_(): Promise<types.Complex_ReturnType> {
        const endpoint = "/complex";
        return await requestFn(endpoint, "HEAD");
    }

    async function optionsComplex_(): Promise<types.Complex_ReturnType> {
        const endpoint = "/complex";
        return await requestFn(endpoint, "OPTIONS");
    }

    async function getComplex_(): Promise<types.Complex_ReturnType> {
        const endpoint = "/complex";
        return await requestFn(endpoint, "GET");
    }

    async function headWithArgs(params: types.WithArgsArgsType): Promise<types.WithArgsReturnType> {
        const endpoint = buildUrl("/with/<arg>/args", params);
        return await requestFn(endpoint, "HEAD");
    }

    async function optionsWithArgs(params: types.WithArgsArgsType): Promise<types.WithArgsReturnType> {
        const endpoint = buildUrl("/with/<arg>/args", params);
        return await requestFn(endpoint, "OPTIONS");
    }

    async function getWithArgs(params: types.WithArgsArgsType): Promise<types.WithArgsReturnType> {
        const endpoint = buildUrl("/with/<arg>/args", params);
        return await requestFn(endpoint, "GET");
    }

    async function headPytest(): Promise<types.PytestReturnType> {
        const endpoint = "/pytest";
        return await requestFn(endpoint, "HEAD");
    }

    async function optionsPytest(): Promise<types.PytestReturnType> {
        const endpoint = "/pytest";
        return await requestFn(endpoint, "OPTIONS");
    }

    async function getPytest(): Promise<types.PytestReturnType> {
        const endpoint = "/pytest";
        return await requestFn(endpoint, "GET");
    }

    return {
        headStatic,
        optionsStatic,
        getStatic,
        headMain,
        optionsMain,
        postMain,
        getMain,
        headComplex_,
        optionsComplex_,
        getComplex_,
        headWithArgs,
        optionsWithArgs,
        getWithArgs,
        headPytest,
        optionsPytest,
        getPytest,
    };
}

import typing


if typing.TYPE_CHECKING:
    from io import TextIOBase
    from ts_flask_urls.ts_types import TSType
    from .extractor import FlaskRouteTypeExtractor


class CodeWriter:
    def __init__(
        self,
        types_file: "TextIOBase",
        api_file: "TextIOBase",
        endpoint: str = "",
        stop_on_error: bool = False,
    ) -> None:
        self.types_file = types_file
        self.api_file = api_file
        self.endpoint = endpoint
        self.stop_on_error = stop_on_error

    def write(self, parsers: typing.Iterable["FlaskRouteTypeExtractor"]) -> bool:
        error = False
        self._write_api_header()
        for parser in parsers:
            return_type = parser.parse_return_type()
            args_type = parser.parse_args_type()
            if return_type is None or args_type is None:
                error = True
                if self.stop_on_error:
                    return False
                continue
            self._write_api_function(parser.rule_name, parser.rule_url, args_type)
            self._write_types(parser.rule_name, return_type, args_type)
        return not error

    def _write_api_header(self) -> None:
        self.api_file.write('import * as types from "./types";\n\n')
        self.api_file.write(f'const BASE_ENDPOINT = "{self.endpoint}";\n\n')
        self.api_file.write(
            "function join(urlPart1: string, urlPart2: string) {\n"
            "    let url = urlPart1;\n"
            '    if (!url.endsWith("/") && !urlPart2.startsWith("/")) {\n'
            '        url += "/";\n'
            "    }\n"
            '    else if (url.endsWith("/") && urlPart2.startsWith("/")) {\n'
            "        url = url.substring(0, -1);\n"
            "    }\n"
            "    url += urlPart2;\n"
            "    return url;\n"
            "}\n\n",
        )

        self.api_file.write(
            "async function request(endpoint: string) {\n"
            "    const req = await fetch(join(BASE_ENDPOINT, endpoint));\n"
            "    if (!req.ok) throw Error(`Request failed with code ${req.status}.`);\n"
            "    const json = await req.json();\n"
            "    return json;\n"
            "}\n\n",
        )

        self.api_file.write(
            "// eslint-disable-next-line @typescript-eslint/no-explicit-any\n"
            "export function buildUrl(rule: string, params: Record<string, any>) {\n"
            "    return rule.replace(/<([a-zA-Z_]+[a-zA-Z_0-9]*)>/, (_, key) => {\n"
            "        return String(params[key]);\n"
            "    });\n"
            "}\n\n",
        )

    def _write_api_function(
        self, rule_name: str, rule_url: str, args_type: "TSType"
    ) -> None:
        params = (
            f"params: types.{rule_name}_ArgsType" if args_type != "undefined" else ""
        )
        url_for_params = "params" if args_type != "undefined" else ""
        build_url = (
            f'buildUrl("{rule_url}", params)'
            if args_type != "undefined"
            else f'"{rule_url}"'
        )
        self.api_file.write(
            f"export function urlFor_{rule_name}({params}): string {{\n"
            f"    const endpoint = {build_url};\n"
            "    return endpoint;\n"
            "}\n\n",
        )
        self.api_file.write(
            f"export async function request_{rule_name}({params}): Promise<types.{rule_name}_ReturnType> {{\n"  # noqa: E501
            f"    const endpoint = urlFor_{rule_name}({url_for_params});\n"
            f"    return await request(endpoint);\n"
            "}\n\n",
        )

    def _write_types(
        self, rule_name: str, return_type: "TSType", args_type: "TSType"
    ) -> None:
        return_type_name = f"{rule_name}_ReturnType"
        self.types_file.write(
            f"export type {return_type_name} = {return_type.generate(return_type_name)}"
            ";\n"
        )
        args_type_name = f"{rule_name}_ArgsType"
        self.types_file.write(
            f"export type {args_type_name} = {args_type.generate(args_type_name)};\n\n"
        )

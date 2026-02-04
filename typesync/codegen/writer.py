import typing

import inflection

if typing.TYPE_CHECKING:
    from io import TextIOBase
    from typesync.ts_types import TSType
    from .extractor import FlaskRouteTypeExtractor


def make_rule_name_map(rule_name: str, prefix: str = "") -> dict[str, str]:
    return {
        prefix + "pc": inflection.camelize(rule_name, True),
        prefix + "cc": inflection.camelize(rule_name, False),
        prefix + "sc": inflection.underscore(rule_name),
        prefix + "uc": rule_name.replace("_", "").upper(),
        prefix + "lc": rule_name.replace("_", "").lower(),
        prefix + "d": rule_name,
    }


class CodeWriter:
    def __init__(
        self,
        types_file: "TextIOBase",
        api_file: "TextIOBase",
        types_file_name: str,
        return_type_format: str,
        params_type_format: str,
        function_name_format: str,
        endpoint: str = "",
        stop_on_error: bool = False,
    ) -> None:
        self.types_file = types_file
        self.api_file = api_file
        self.types_file_name = types_file_name.removesuffix(".ts")
        self.return_type_format = return_type_format
        self.params_type_format = params_type_format
        self.function_name_format = function_name_format
        self.endpoint = endpoint
        self.stop_on_error = stop_on_error

    def _api_function_name(self, rule_name: str, method: str) -> str:
        return self.function_name_format.format_map(
            {**make_rule_name_map(rule_name, "r_"), **make_rule_name_map(method, "m_")}
        )

    def _return_type_name(self, rule_name: str) -> str:
        return self.return_type_format.format_map(make_rule_name_map(rule_name))

    def _params_type_name(self, rule_name: str) -> str:
        return self.params_type_format.format_map(make_rule_name_map(rule_name))

    def write(self, parsers: typing.Iterable["FlaskRouteTypeExtractor"]) -> bool:
        error = False
        self._write_types_header()
        self._write_api_header()
        names: list[str] = []
        for parser in parsers:
            return_type = parser.parse_return_type()
            args_type = parser.parse_args_type()
            json_body_type = parser.parse_json_body()
            if return_type is None or args_type is None:
                error = True
                if self.stop_on_error:
                    return False
                continue
            return_type_name, params_type_name, has_args, has_json = self._write_types(
                parser.rule_name, return_type, args_type, json_body_type
            )
            names.extend(
                self._write_api_function(
                    parser.rule_name,
                    parser.rule_url,
                    method,
                    return_type_name,
                    params_type_name,
                    has_args,
                    has_json,
                )
                for method in (parser.rule.methods or {})
            )
        self._write_api_footer(names)
        return not error

    def _write_types_header(self) -> None:
        self.types_file.write(
            "export interface RequestArgs {\n"
            "    headers?: Record<string, string>;\n"
            "}\n\n"
        )
        self.types_file.write(
            "export interface RequestOptions extends RequestArgs {\n"
            "    method: string;\n"
            "    body?: unknown;\n"
            "}\n\n"
        )
        self.types_file.write(
            "export type RequestFunction = (\n"
            "    endpoint: string, options: RequestOptions\n"
            "// eslint-disable-next-line @typescript-eslint/no-explicit-any\n"
            ") => Promise<any>;"
            "\n\n"
        )

    def _write_api_header(self) -> None:
        self.api_file.write(f'import * as types from "./{self.types_file_name}";\n\n')
        self.api_file.write(
            "// eslint-disable-next-line @typescript-eslint/no-explicit-any\n"
            "export function buildUrl(rule: string, params: Record<string, any>) {\n"
            "    return rule.replace(/<([a-zA-Z_]+[a-zA-Z_0-9]*)>/, (_, key) => {\n"
            "        return String(params[key]);\n"
            "    });\n"
            "}\n\n",
        )
        self.api_file.write(
            "export function makeAPI(requestFn: types.RequestFunction) {\n"
        )

    def _write_api_footer(self, names: list[str]) -> None:
        self.api_file.write("    return {\n")
        for name in names:
            self.api_file.write(f"        {name},\n")
        self.api_file.write("    };\n")
        self.api_file.write("}\n")

    def _write_api_function(
        self,
        rule_name: str,
        rule_url: str,
        method: str,
        return_type_name: str,
        args_type_name: str,
        has_args: bool,
        has_json: bool,
    ) -> str:
        build_url = (
            f'buildUrl("{rule_url}", params.args)' if has_args else f'"{rule_url}"'
        )
        params = f"params: types.{args_type_name}"
        f_name = self._api_function_name(rule_name, method)
        self.api_file.write(
            f"    async function {f_name}({params}): Promise<types.{return_type_name}> {{\n"  # noqa: E501
            f"        const endpoint = {build_url};\n"
            "        return await requestFn(\n"
            "            endpoint,\n"
            '            {method: "' + method + '", ...params}\n'
            "        );\n"
            "    }\n\n",
        )
        return f_name

    def _write_types(
        self,
        rule_name: str,
        return_type: "TSType",
        args_type: "TSType",
        json_body_type: "TSType | None",
    ) -> tuple[str, str, bool, bool]:
        return_type_name = self._return_type_name(rule_name)
        self.types_file.write(
            f"export type {return_type_name} = {return_type.generate(return_type_name)}"
            ";\n"
        )
        params_type_name = self._params_type_name(rule_name)
        optional_args = "?" if args_type == "undefined" else ""
        optional_body = (
            "?" if json_body_type is None or json_body_type == "undefined" else ""
        )

        internal_args_name = f"_{rule_name}Args"
        self.types_file.write(
            f"type {internal_args_name} = {args_type.generate(internal_args_name)};\n"
        )

        internal_body_name = f"_{rule_name}Body"
        string_json_body_type = (
            "undefined"
            if json_body_type is None
            else json_body_type.generate(internal_body_name)
        )
        self.types_file.write(f"type {internal_body_name} = {string_json_body_type};\n")

        self.types_file.write(
            f"export interface {params_type_name} extends RequestArgs" + " {\n"
            f"    args{optional_args}: {internal_args_name};\n"
            f"    body{optional_body}: {internal_body_name};\n"
            "}\n\n"
        )
        return (
            return_type_name,
            params_type_name,
            optional_args == "",
            optional_body == "",
        )

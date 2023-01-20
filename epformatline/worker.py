from typing import List


def sanitize_arg(arg: str) -> str:
    if arg.startswith('std::string(') and arg.endswith(')'):
        return arg[12:-1]
    if arg.startswith('std::string{') and arg.endswith('}'):
        return arg[12:-1]
    return arg.strip()


def translate(input_string: str) -> str:
    """
    Right now I think we are assuming a well-formed string, no unclosed braces, but we might change that later
    :param input_string:
    :return:
    """
    fmt_string = ""
    out_args: List[str] = list()
    reading_quoted = False
    reading_arg = False
    reading_raw_string = False
    first_character = True
    next_token_quote_is_fine = False
    current_quote_char = ""
    cur_arg_string = ""
    max_index = len(input_string) - 1
    arg_brace_stack = []
    for i, c in enumerate(input_string):
        if first_character:
            if c == " " or c == "\n":
                continue  # pragma: no cover...this is getting hit, but shows as a miss.  Not sure.
            first_character = False
            if c == "\"" or c == "'":
                reading_quoted = True
                current_quote_char = c
                continue
            else:
                reading_arg = True
        if reading_quoted:
            if next_token_quote_is_fine:
                fmt_string += c
                next_token_quote_is_fine = False
            elif c == "\\" and input_string[i + 1] == "\"":  # single backslash escape quote
                fmt_string += c
                next_token_quote_is_fine = True
            elif c == current_quote_char:
                reading_quoted = False
            else:
                fmt_string += c
        elif reading_arg:
            if c == "[":
                arg_brace_stack.append("]")
                cur_arg_string += c
            elif c == "(":
                if cur_arg_string != 'std::string':
                    arg_brace_stack.append(")")
                cur_arg_string += c
            elif len(arg_brace_stack) > 0:
                if c == arg_brace_stack[-1]:
                    arg_brace_stack.pop()
                cur_arg_string += c
                if i == len(input_string) - 1:  # then we finished the string ending on a variable
                    cur_arg_string = sanitize_arg(cur_arg_string)
                    out_args.append(cur_arg_string)
                    cur_arg_string = ""
                    fmt_string += "{}"
            elif c == " " or c == "\n":
                cur_arg_string = sanitize_arg(cur_arg_string)
                out_args.append(cur_arg_string)
                cur_arg_string = ""
                fmt_string += "{}"
                reading_arg = False
            elif i == max_index:
                cur_arg_string += c
                cur_arg_string = sanitize_arg(cur_arg_string)
                out_args.append(cur_arg_string)
                fmt_string += "{}"
                break
            else:
                cur_arg_string += c
        elif reading_raw_string:
            if c == ")" and input_string[i + 1] == "\"":
                cur_arg_string += c
                cur_arg_string += input_string[i + 1]
                cur_arg_string = sanitize_arg(cur_arg_string)
                out_args.append(cur_arg_string)
                cur_arg_string = ""
                fmt_string += "{}"
                reading_raw_string = False
            else:
                cur_arg_string += c
        else:
            if c == "\"" or c == "'":
                reading_quoted = True
                current_quote_char = c
                continue
            elif c == " " or c == "\n" or c == "+":
                continue  # ignore whitespace in code context
            elif c == "R" and i < max_index - 4:  # 4 is a bit fuzzy, probably safe though
                if input_string[i + 1] == "\"":
                    reading_raw_string = True
                    cur_arg_string += c
                else:
                    reading_arg = True
                    cur_arg_string += c
            else:
                reading_arg = True
                cur_arg_string += c

    # if we make it out of the loop while still reading a variableName

    output_string = f"format(\"{fmt_string}\""
    for a in out_args:
        output_string += f", {a}"
    output_string += ")"
    return output_string

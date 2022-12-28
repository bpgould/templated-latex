"""
Small test python script to use Jinja2 templates
for dynamically generating tex files that can be
compiled to pdf files. I will adapt this for
creating org-wide SLI/SLO/SLA docs for my SRE team
"""
import json
import os
import subprocess
from jinja2 import Environment
from jinja2 import FileSystemLoader

# dictionary of characters to replace from json config file
replace_chars = {"%": "\\%"}

with open("template.json", encoding="utf-8") as json_file:
    template_dict = json.load(json_file)


def make_valid_string(string, replacement_map):
    for key, value in replacement_map.items():
        if key in string:
            new_string = string.replace(key, value)
            return new_string

    return string


def handle_list(list_value, search_dict, replacement_map):
    for index, item in enumerate(list_value):
        print(f"item: {item}, index: {index}")
        if isinstance(item, str):
            processed_string = make_valid_string(item, replacement_map)
            if item is not processed_string:
                list_value[index] = processed_string
        elif isinstance(item, dict):
            get_recursively(item, replacement_map)
        elif isinstance(item, list):
            handle_list(item, search_dict, replacement_map)


def get_recursively(search_dict, replacement_map):
    """
    given dictionary, recursively replace illegal values
    with legal values from a replacement map and return
    processed dictionary
    """

    for key, value in search_dict.items():
        if isinstance(value, str):
            processed_string = make_valid_string(value, replacement_map)
            if value is not processed_string:
                search_dict[key] = processed_string

        elif isinstance(value, dict):
            get_recursively(value, replacement_map)

        elif isinstance(value, list):
            handle_list(value, search_dict, replacement_map)

    return search_dict


# recursively iterate over nth child of json and replace illegal substrings

result = get_recursively(template_dict, replace_chars)

latex_jinja_env = Environment(
    block_start_string="\BLOCK{",
    block_end_string="}",
    variable_start_string="\VAR{",
    variable_end_string="}",
    comment_start_string="\#{",
    comment_end_string="}",
    line_statement_prefix="%%",
    line_comment_prefix="%#",
    trim_blocks=True,
    autoescape=False,
    loader=FileSystemLoader(os.path.abspath(".")),
)

template = latex_jinja_env.get_template("jinja-test.tex")

output_tex = template.render(result)

# print to console
print(output_tex)

# write to tex file
with open("output/out.tex", "w", encoding="utf-8") as file:
    # Writing data to a file
    file.write(output_tex)

os.chdir("output/")

output = subprocess.run(
    ['pdflatex -synctex=1 -interaction=nonstopmode "out".tex'],
    shell=True,
    check=True,
    stdout=subprocess.PIPE,
)

print(f"pdf build return code: {output.returncode}")

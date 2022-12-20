"""
Small test python script to use Jinja2 templates
for dynamically generating tex files that can be
compiles to pdf files. I will adapt this for
creating org-wide SLI/SLO/SLA docs for my SRE team
"""
import os
from jinja2 import Environment
from jinja2 import FileSystemLoader

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

output_tex = template.render(section1="Long Form", section2="Short Form")

# print to console
print(output_tex)

# write to tex file
with open("out.tex", "w", encoding="utf-8") as file1:
    # Writing data to a file
    file1.write(output_tex)

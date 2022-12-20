# Templated Latex source using Python + Jinja2

1. create a venv
2. install the dependencies in `requirements.txt`
3. run the `test.py` file
4. `out.tex` is produced which can then be compiled to pdf using something like pdflatex or another python package

This is a powerful technique for generating lots of pretty PDFs using JSON or some other data source.

## render function in Jinja can take a dictionary

```python
render([context])
This method accepts the same arguments as the dict constructor: A dict, a dict subclass or some keyword arguments. If no arguments are given the context will be empty. These two calls do the same:

template.render(knights='that say nih')
template.render({'knights': 'that say nih'})
This will return the rendered template as a string.

Parameters:
args (Any) –

kwargs (Any) –

Return type:
str
```

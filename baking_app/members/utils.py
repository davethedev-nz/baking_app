from string import Template

def render_template_string(template_string, context):
    template = Template(template_string)
    return template.safe_substitute(context)

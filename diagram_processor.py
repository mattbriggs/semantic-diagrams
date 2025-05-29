import os
import sys
import json
import yaml
import shutil
import subprocess
import jsonschema
from jinja2 import Template

# ------------------------------------------------------------------------------
# Function: find_mermaid_cli
# Description: Attempts to locate the Mermaid CLI (mmdc) on the user's system.
#   Checks system PATH first, then known common installation paths.
#   Raises FileNotFoundError with guidance if not found.
# ------------------------------------------------------------------------------

def find_mermaid_cli():
    # Check if mmdc is in system PATH
    mermaid_cli = shutil.which("mmdc")

    # Fallback to common install locations (Windows and Unix)
    if mermaid_cli is None:
        possible_paths = [
            os.path.expandvars(r"%APPDATA%\npm\mmdc.cmd"),    # Windows global npm
            os.path.expanduser(r"~/.npm-global/bin/mmdc"),     # Unix custom npm prefix
            os.path.expanduser(r"~/node_modules/.bin/mmdc"),   # Local npm install
        ]
        for path in possible_paths:
            if os.path.isfile(path) and os.access(path, os.X_OK):
                mermaid_cli = path
                break

    # Error out with installation instructions
    if mermaid_cli is None:
        raise FileNotFoundError(
            "Mermaid CLI (mmdc) not found.\n"
            "Please install it with:\n"
            "  npm install -g @mermaid-js/mermaid-cli\n"
            "Or ensure it is in your PATH."
        )

    return mermaid_cli

# ------------------------------------------------------------------------------
# Mermaid CLI setup
# ------------------------------------------------------------------------------

try:
    MERMAID_CLI = find_mermaid_cli()
    print(f"Using Mermaid CLI at: {MERMAID_CLI}")
except FileNotFoundError as e:
    print(str(e), file=sys.stderr)
    sys.exit(1)

# ------------------------------------------------------------------------------
# Constants: Schema file paths and HTML template
# ------------------------------------------------------------------------------

PAGE_SCHEMA_PATH = os.path.abspath("page.schema.json")
DIAGRAM_SCHEMA_PATH = os.path.abspath("diagram.schema.json")

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
</head>
<body>
    <h1>{{ title }}</h1>
    <h2>{{ subtitle }}</h2>
    <p><strong>Description:</strong> {{ description }}</p>
    <p><strong>Summary:</strong> {{ summary }}</p>
    {% if diagram %}
    <div>
        <h3>{{ diagram.name }}</h3>
        <img src="{{ diagram.name }}.png" alt="{{ diagram.name }} Diagram">
    </div>
    {% endif %}
</body>
</html>
"""

# ------------------------------------------------------------------------------
# Function: load_schema
# Description: Loads a JSON Schema from the provided file path.
# ------------------------------------------------------------------------------

def load_schema(schema_path):
    abs_path = os.path.abspath(schema_path)
    with open(abs_path, 'r', encoding='utf-8') as file:
        return json.load(file)

# ------------------------------------------------------------------------------
# Function: validate_yaml
# Description: Validates YAML content against a JSON Schema.
# Returns: (bool, str|None) indicating success and error message (if any)
# ------------------------------------------------------------------------------

def validate_yaml(yaml_content, schema):
    try:
        jsonschema.validate(instance=yaml_content, schema=schema)
        return True, None
    except jsonschema.exceptions.ValidationError as e:
        return False, str(e)

# ------------------------------------------------------------------------------
# Function: convert_to_mermaid
# Description: Converts a structured diagram YAML object into Mermaid syntax.
# ------------------------------------------------------------------------------

def convert_to_mermaid(diagram):
    diagram_type = diagram.get("type", "classDiagram")
    mermaid = f"{diagram_type}\n"

    # Define classes
    for thing in diagram.get("things", []):
        mermaid += f"    class {thing['id']} {{\n    }}\n"

    # Define relationships
    for relation in diagram.get("relationships", []):
        src = relation['source']
        tgt = relation['target']
        arrow = "<|--" if relation.get("type") == "directed" else "--"
        mermaid += f"    {src} {arrow} {tgt}\n"

    return mermaid

# ------------------------------------------------------------------------------
# Function: render_mermaid
# Description: Writes Mermaid syntax to file and invokes Mermaid CLI to render PNG.
# ------------------------------------------------------------------------------

def render_mermaid(diagram, output_path):
    mermaid_code = convert_to_mermaid(diagram)
    print("Generated Mermaid Code:\n", mermaid_code)  # Debug output

    with open("temp_diagram.mmd", 'w', encoding='utf-8') as file:
        file.write(mermaid_code)

    subprocess.run(
        [MERMAID_CLI, "-i", "temp_diagram.mmd", "-o", output_path],
        check=True
    )

# ------------------------------------------------------------------------------
# Function: main
# Description: Loads and validates YAML input, renders diagram, and writes HTML.
# ------------------------------------------------------------------------------

def main(input_file):
    # Load input YAML file
    with open(input_file, 'r', encoding='utf-8') as file:
        yaml_content = yaml.safe_load(file)

    # Load and validate schemas
    print("Validating YAML against schemas...")
    page_schema = load_schema(PAGE_SCHEMA_PATH)
    diagram_schema = load_schema(DIAGRAM_SCHEMA_PATH)

    page_valid, page_error = validate_yaml(yaml_content, page_schema)
    diagram_valid, diagram_error = validate_yaml(
        yaml_content.get('diagram', {}),
        diagram_schema
    )

    if not page_valid:
        print(f"Page schema validation error:\n{page_error}", file=sys.stderr)
        sys.exit(1)

    if not diagram_valid:
        print(f"Diagram schema validation error:\n{diagram_error}", file=sys.stderr)
        sys.exit(1)

    print("Validation successful. Generating HTML...")

    # Render diagram if defined
    if "diagram" in yaml_content:
        diagram_name = yaml_content["diagram"]["name"]
        render_mermaid(yaml_content["diagram"], f"{diagram_name}.png")

    # Generate HTML using Jinja2
    template = Template(HTML_TEMPLATE)
    html_content = template.render(**yaml_content)

    output_html = f"{os.path.splitext(input_file)[0]}.html"
    with open(output_html, 'w', encoding='utf-8') as file:
        file.write(html_content)

    print(f"HTML page generated: {output_html}")

# ------------------------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python diagram_processor.py <input_file.yml>", file=sys.stderr)
        sys.exit(1)

    main(sys.argv[1])
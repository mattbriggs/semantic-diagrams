import yaml
import json
import os
import sys
import jsonschema
from jinja2 import Template
import subprocess
import shutil

# Set the path to the Mermaid CLI dynamically
MERMAID_CLI = shutil.which("mmdc")

if MERMAID_CLI is None:
    MERMAID_CLI = "C:\\Users\\mabrigg\\AppData\\Roaming\\npm\\mmdc.cmd"  # 'mmdc' / Mermaid CLI for rendering diagrams (must be installed)

# if MERMAID_CLI is None:
#     raise FileNotFoundError("Mermaid CLI (mmdc) is not installed or not found in PATH.")

# Constants for schema paths
PAGE_SCHEMA_PATH = os.path.abspath("page.schema.json")
DIAGRAM_SCHEMA_PATH = os.path.abspath("diagram.schema.json")

# HTML Template
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

# Function to load JSON schema using absolute paths and file URLs
def load_schema(schema_path):
    abs_path = os.path.abspath(schema_path)
    with open(abs_path, 'r') as file:
        schema = json.load(file)
    return schema

# Function to validate YAML against a schema
def validate_yaml(yaml_content, schema):
    try:
        jsonschema.validate(instance=yaml_content, schema=schema)
        return True, None
    except jsonschema.exceptions.ValidationError as e:
        return False, str(e)

# Function to convert diagram YAML to Mermaid.js class diagram notation
def convert_to_mermaid(diagram):
    diagram_type = diagram.get("type", "classDiagram")

    # Create the initial diagram type declaration
    mermaid = f"{diagram_type}\n"
    
    # Create classes
    for thing in diagram.get("things", []):
        mermaid += f"    class {thing['id']} {{\n    }}\n"

    # Create relationships between classes
    for relation in diagram.get("relationships", []):
        if relation["type"] == "directed":
            mermaid += f"    {relation['source']} <|-- {relation['target']}\n"
        else:
            mermaid += f"    {relation['source']} -- {relation['target']}\n"

    return mermaid

# Function to render Mermaid.js diagram
def render_mermaid(diagram, output_path):
    mermaid_code = convert_to_mermaid(diagram)
    print("Generated Mermaid Code:\n", mermaid_code)  # Debug output to check generated Mermaid code
    with open("temp_diagram.mmd", 'w') as file:
        file.write(mermaid_code)
    
    # Use the Mermaid CLI to convert to PNG
    subprocess.run([MERMAID_CLI, "-i", "temp_diagram.mmd", "-o", output_path], check=True)

# Main function
def main(input_file):
    # Load YAML content
    with open(input_file, 'r') as file:
        yaml_content = yaml.safe_load(file)
    
    # Validate YAML content using absolute paths for schemas
    page_schema = load_schema(PAGE_SCHEMA_PATH)
    diagram_schema = load_schema(DIAGRAM_SCHEMA_PATH)

    print("Validating YAML against schemas...")
    page_valid, page_error = validate_yaml(yaml_content, page_schema)
    diagram_valid, diagram_error = validate_yaml(yaml_content.get('diagram', {}), diagram_schema)

    if not page_valid:
        print(f"Page schema validation error: {page_error}")
        sys.exit(1)

    if not diagram_valid:
        print(f"Diagram schema validation error: {diagram_error}")
        sys.exit(1)
    
    print("Validation successful. Generating HTML page...")
    
    # Render Mermaid Diagram if exists
    if "diagram" in yaml_content:
        diagram_name = yaml_content["diagram"]["name"]
        render_mermaid(yaml_content["diagram"], f"{diagram_name}.png")

    # Create HTML content
    template = Template(HTML_TEMPLATE)
    html_content = template.render(**yaml_content)

    # Save HTML content
    output_html = f"{os.path.splitext(input_file)[0]}.html"
    with open(output_html, 'w') as file:
        file.write(html_content)

    print(f"HTML page generated: {output_html}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python diagram_processor.py <input_file.yml>")
        sys.exit(1)
    main(sys.argv[1])

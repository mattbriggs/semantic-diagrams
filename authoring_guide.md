# Authoring Guide for Diagram YAML Files

## Overview

This guide explains how to create valid YAML files that define a structured HTML page along with a semantic diagram using `mermaid.js`. The script (`diagram_processor.py`) will transform the YAML file into an HTML page and generate the diagram as a PNG image, which will be included in the HTML file.

## YAML File Structure

The YAML file should contain the following top-level elements:

- **title**: (Required) The main title of the HTML page.
- **subtitle**: (Optional) A subtitle for the HTML page.
- **description**: (Required) A brief description of the page content.
- **summary**: (Required) A summary of the content.
- **diagram**: (Optional) Contains the information to render a diagram using Mermaid.js.

### Diagram Section Structure

The `diagram` section describes the diagram to be generated and rendered as a PNG image. It has the following structure:

```yaml
diagram:
  name: "Example Diagram"
  type: "classDiagram"
  things:
    - id: "A"
      label: "Class A"
      type: "class"
    - id: "B"
      label: "Class B"
      type: "class"
  relationships:
    - source: "A"
      target: "B"
      type: "directed"
```

### Explanation of Diagram Section Elements

- **name**: (Required) A unique name for the diagram, which will be used as the file name for the generated PNG.
- **type**: (Required) The diagram type. Supported types include `graph`, `flowchart`, `erDiagram`, and `classDiagram`.
- **things**: (Required) An array of elements that define the nodes or classes in the diagram. Each element must have:
  - `id`: (Required) A unique identifier for the node.
  - `label`: (Required) The label or display name for the node.
  - `type`: (Optional) The type of the node (for semantic meaning).
- **relationships**: (Optional) An array of relationships between the defined elements. Each relationship must have:
  - `source`: (Required) The `id` of the source node.
  - `target`: (Required) The `id` of the target node.
  - `type`: (Required) The type of relationship. Supported values are:
    - `directed`: Renders a directed relationship (`-->` in Mermaid).
    - `undirected`: Renders an undirected relationship (`---` in Mermaid).

### Example YAML File

```yaml
title: "Sample HTML Page"
subtitle: "A Demonstration of YAML to HTML Conversion"
description: "This page was generated from a YAML file."
summary: "The YAML file describes the structure of this page, including a diagram."
diagram:
  name: "Class Example"
  type: "classDiagram"
  things:
    - id: "Vehicle"
      label: "Vehicle"
      type: "class"
    - id: "Car"
      label: "Car"
      type: "class"
    - id: "Bike"
      label: "Bike"
      type: "class"
  relationships:
    - source: "Vehicle"
      target: "Car"
      type: "directed"
    - source: "Vehicle"
      target: "Bike"
      type: "directed"
```

## Script Operation

### Step-by-Step Workflow of `diagram_processor.py`

1. **Load YAML File**: 
   - The script reads the YAML file specified as an argument.
  
2. **Validate the YAML File**:
   - The script uses two JSON Schemas (`page_schema.json` and `diagram_schema.json`) to validate the structure and content of the YAML file.
   - If the YAML does not conform to the expected schema, the script outputs a validation error and stops.

3. **Convert Diagram to Mermaid.js Format**:
   - If the YAML contains a `diagram` section, the script converts the diagram elements into the appropriate `mermaid.js` syntax based on the diagram type (e.g., `graph TD` for flowcharts or `classDiagram` for class diagrams).
   - It generates nodes, relationships, and containers as defined in the YAML.

4. **Render the Diagram as a PNG**:
   - The script uses `mermaid-cli` to convert the Mermaid code into a PNG file. The image is saved using the `name` attribute from the diagram section as the filename (e.g., `Class Example.png`).

5. **Generate the HTML Page**:
   - The script then uses a Jinja2 HTML template to render the HTML page using the elements from the YAML file.
   - If the diagram was successfully generated, the HTML file includes an image tag pointing to the rendered PNG with an appropriate alt text.

6. **Save the HTML File**:
   - The final HTML file is saved with the same base name as the YAML file (e.g., `example_diagram.html`).

7. **Output Status to Terminal**:
   - During each step, the script outputs its current status and any issues encountered to the terminal.

### Expected Output

After running the script with a valid YAML file, you should see:

1. A PNG image of the diagram saved with the `name` from the `diagram` section (e.g., `Class Example.png`).
2. An HTML file generated from the YAML content with the same base name as the YAML file (e.g., `example_diagram.html`).
3. If you open the HTML file, it should contain:
   - The title and subtitle.
   - The description and summary.
   - The diagram image embedded in the body with a descriptive alt text.

### Example Command to Run the Script

```bash
python diagram_processor.py example_diagram.yml
```

The above command will read the `example_diagram.yml` file, validate it, generate a diagram, and produce an HTML file named `example_diagram.html`.

### Troubleshooting

- **YAML Schema Validation Errors**: If you receive a validation error, check your YAML file structure against the schema definition.
- **Mermaid CLI Not Installed**: Ensure that `mermaid-cli` is installed globally using npm:
  
  ```bash
  npm install -g @mermaid-js/mermaid-cli
  ```

- **Invalid Diagram Type**: Make sure that the `type` in the `diagram` section is one of the supported values (`graph`, `flowchart`, `erDiagram`, `classDiagram`).
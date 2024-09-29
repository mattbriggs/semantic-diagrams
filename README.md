# Semantic Diagrams

Creating visual diagrams is a critical part of communicating complex systems, relationships, and workflows. However, not all diagrams are created equal. There are distinct approaches to diagramming based on the toolset and methodology used. This project focuses on **semantic diagrams** and **diagrams as code**, which contrast significantly from traditional tools like Microsoft Visio or Adobe Illustrator.

### Semantic Diagrams vs. Diagrams as Code

**Semantic diagrams** are more than visual representations—they are structured, data-driven diagrams that encode meaning using a defined schema. This approach prioritizes the relationships and types of components in the diagram, enabling tools and scripts to understand the underlying data, not just the visual appearance. When defining a semantic diagram, each element (e.g., nodes, edges, containers) is given a unique identifier and contextual metadata, making it possible to derive insights, validate structures, or even transform diagrams into other formats programmatically.

**Diagrams as code** refer to creating diagrams using text-based representations, often in a markup language or code syntax. This allows diagrams to be version-controlled, easily updated, and generated using automated processes. Tools like `mermaid.js` and `Graphviz` use this approach, enabling developers and data engineers to generate diagrams directly from codebases, configuration files, or structured data formats like YAML or JSON.

### How Does This Differ from Traditional Diagram Tools?

Traditional diagram tools such as Microsoft Visio or Adobe Illustrator are **visual-first**. They focus on enabling designers and diagram creators to draw and customize shapes, lines, and styles. While these tools are powerful for creating visually rich and polished diagrams, they lack:

1. **Semantic Context**: In traditional tools, the diagram's meaning is visual and often lacks structured metadata. For example, a rectangle might visually represent a database in one context and a server in another, but without standardized metadata, there's no way to distinguish between them programmatically.

2. **Scalability and Automation**: Updating or generating large-scale diagrams manually in tools like Visio can be time-consuming and error-prone. Diagrams as code, in contrast, allow for batch generation, easy updates through version control, and automation via scripts.

3. **Interoperability**: Semantic diagrams can be exported, transformed, or even queried, making them suitable for integration with other systems or knowledge management frameworks. Traditional diagrams are often stored as binary or proprietary formats that are less suitable for integration with data pipelines or analysis tools.

### Why Choose Semantic Diagrams and Diagrams as Code?

1. **Automation**: Generate diagrams dynamically based on data, which is useful in environments with frequent updates or large-scale systems.
2. **Standardization**: Ensure consistency and adherence to diagramming standards, making it easier to share and understand diagrams across teams.
3. **Integration**: Leverage structured data and semantics to integrate diagrams into larger knowledge management systems, making them not just visual aids but interactive, data-driven assets.

### Use Case Example: Generating a Class Diagram from YAML

In this project, you can define a semantic diagram using a YAML file that describes entities and relationships. The script then processes this structured data, validates it against a schema, and generates a visual representation using `mermaid.js`. The resulting HTML page and PNG file not only look correct but are also semantically correct, enabling downstream use in documentation systems, process automation, and interoperability with other tools.

By using semantic diagrams and diagrams as code, you can transform the way you create, update, and share visual information, making your diagrams more than just static images, but dynamic, meaningful parts of your workflow.

## YAML to HTML Diagram Generator

![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Python](https://img.shields.io/badge/Python-3.x-yellow.svg)
![Mermaid](https://img.shields.io/badge/Mermaid.js-CLI-green.svg)

## Overview

The **YAML to HTML Diagram Generator** is a Python-based application that transforms structured YAML files into well-formatted HTML pages with embedded diagrams using `mermaid.js`. This project is ideal for authors who want to define content structure and diagrams in YAML and generate consistent HTML pages with visual aids. 

The application validates the YAML files against modular JSON Schemas to ensure content integrity, and then renders the defined diagrams as PNG images, which are automatically included in the HTML output.

### Features

- Convert YAML files into HTML pages using a predefined schema.
- Support for `mermaid.js` diagram types such as `classDiagram`, `flowchart`, and `erDiagram`.
- Automatic validation of YAML files against custom JSON Schemas.
- Real-time diagram rendering using `mermaid-cli` and seamless HTML integration.
- Step-by-step logging and error handling.

## Project Structure

```plaintext
project/
├── diagram_processor.py          # Python script for processing YAML and generating HTML
├── diagram.schema.json           # JSON Schema for validating the diagram structure
├── page.schema.json              # JSON Schema for validating the HTML page structure
├── example_diagram.yml           # Example YAML file to test the script
├── requirements.txt              # Python dependencies file
├── install.md                    # Installation guide
├── authoring_guide.md            # Guide for creating YAML files
├── README.md                     # Project README file
└── LICENSE.md                    # MIT License file
```

## Installation Guide

To set up and run the project, follow the steps below.

### Prerequisites

1. **Python 3.x**: [Download Python](https://www.python.org/downloads/) if it's not installed.
2. **Node.js and npm**: [Download Node.js](https://nodejs.org/en/download/) to enable Mermaid CLI installation.
3. **Mermaid CLI**: Required for rendering diagrams as PNG images.

### Step-by-Step Installation

1. **Clone the repository** or download the project files.

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install the required Python dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Install Mermaid CLI globally using npm**:

   ```bash
   npm install -g @mermaid-js/mermaid-cli
   ```

4. **Verify that the `mermaid-cli` command is available**:

   ```bash
   mmdc -h
   ```

   You should see a help message if the installation was successful.

## Usage

To convert a YAML file into an HTML page with a rendered diagram, use the following command:

```bash
python diagram_processor.py example_diagram.yml
```

### Command Line Arguments

- The script accepts a single command-line argument, which is the path to the YAML file.
- Example:

  ```bash
  python diagram_processor.py your_diagram_file.yml
  ```

### Expected Output

1. **HTML File**: The script will generate an HTML file in the same directory as the YAML file, with the same base name (e.g., `example_diagram.html`).
2. **Diagram PNG File**: If a diagram is defined in the YAML, a corresponding PNG file (e.g., `Vehicle Class Diagram.png`) will be created.

### Example YAML File

The following is an example of a YAML file that you can use to test the script. Save it as `example_diagram.yml`:

```yaml
# example_diagram.yml
title: "Sample HTML Page"
subtitle: "A Demonstration of YAML to HTML Conversion"
description: "This page was generated from a YAML file."
summary: "The YAML file describes the structure of this page, including a diagram that visualizes relationships between different vehicle classes."

diagram:
  name: "Vehicle Class Diagram"
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
    - id: "Motorcycle"
      label: "Motorcycle"
      type: "class"
  relationships:
    - source: "Vehicle"
      target: "Car"
      type: "directed"
    - source: "Vehicle"
      target: "Bike"
      type: "directed"
    - source: "Vehicle"
      target: "Motorcycle"
      type: "directed"
  containers:
    - container: "Vehicle"
      contains:
        - "Car"
        - "Bike"
        - "Motorcycle"
```

### Troubleshooting

- **YAML Validation Errors**: If the script outputs a validation error, verify your YAML file against the provided `page.schema.json` and `diagram.schema.json`.
- **Mermaid CLI Issues**: Make sure that `mermaid-cli` is properly installed and accessible in your system's PATH.
- **Python Dependency Issues**: If there are missing dependencies, run:

  ```bash
  pip install -r requirements.txt
  ```

## Authoring Guide

For detailed instructions on creating your own YAML files and diagram definitions, refer to the [Authoring Guide](./authoring_guide.md).

## License

This project is licensed under the MIT License - see the [LICENSE.md](./LICENSE.md) file for details.

## Contributing

Contributions are welcome! If you find a bug or want to add a feature, feel free to submit a pull request or open an issue.

## Acknowledgments

Special thanks to the developers of the following libraries and tools:

- **Mermaid.js**: For the diagram rendering capabilities.
- **Jinja2**: For HTML templating.
- **jsonschema**: For YAML validation.

--- 

Let me know if you need any adjustments to the README or additional details!
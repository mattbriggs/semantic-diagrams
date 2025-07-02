## Semantic Diagrams: YAML to HTML Diagram Generator

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

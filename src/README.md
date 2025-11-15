# PDF Analyzer Application

## Overview
The PDF Analyzer Application is designed to process PDF files containing multiple pages, extracting client references, analyzing parameters for compliance, and logging any non-compliance issues into an Excel file. This application is useful for organizations that need to ensure that their documents meet specific standards and regulations.

## Project Structure
```
pdf_analyzer_app
├── src
│   ├── main.py          # Entry point of the application
│   ├── pdf_splitter.py  # Functions to split PDF into individual pages
│   ├── analyzer.py      # Functions to analyze compliance of parameters
│   ├── logger.py        # Manages logging of non-compliance issues into Excel
│   └── types
│       └── index.py     # Defines data types and structures used in the application
├── requirements.txt      # Lists dependencies required for the project
└── README.md             # Documentation for the project
```

## Installation
To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd pdf_analyzer_app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage
To run the application, execute the following command:
```
python src/main.py <input_pdf_path> <output_excel_path>
```
Replace `<input_pdf_path>` with the path to the PDF file you want to analyze and `<output_excel_path>` with the desired path for the output Excel file.

## Functionality
- **PDF Splitting**: The application reads the input PDF and splits it into individual pages, naming each page according to the client reference found in the text.
- **Parameter Analysis**: Each page is analyzed for compliance against predefined criteria. Any non-compliance issues are identified and logged.
- **Logging**: Non-compliance issues are recorded in an Excel file, allowing for easy tracking and reporting.

## Dependencies
The project requires the following Python libraries:
- `PyMuPDF`: For handling PDF files.
- `pandas`: For data manipulation and analysis.
- `openpyxl`: For writing to Excel files.

## Contributing
Contributions to the project are welcome. Please submit a pull request or open an issue for any suggestions or improvements.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.
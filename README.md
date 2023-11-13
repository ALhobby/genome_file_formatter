# Genomic Data File Re-formatter

This repository contains a Streamlit app for reformatting genomic data files. The app allows users to rename columns, sort data, and add/remove the "chr" prefix in a particular column. It provides a simple and painless interface for reformatting BED or IGV GWAS files, although it can be used for any text file containing tabular data.

## Features

- **Rename columns:** Easily rename columns in the uploaded genomic data file using a sidebar interface.
- **Sort data:** Sort the data based on a chosen column, either in ascending or descending order.
- **Manipulate chromosome prefix:** Add or remove the "chr" prefix from a specific column.
- **Download updated data:** Download the reformatted data as a CSV file.

## Usage

You can run the Streamlit app by executing the following command:

    streamlit run genome_file_formatter.py

## Contributing

Contributions to the Genomic Data File Re-formatter are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request. We appreciate your feedback and contributions.

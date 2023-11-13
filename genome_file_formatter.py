import streamlit as st
import pandas as pd
import base64


def column_renamer(df: pd.DataFrame, has_header: bool = True) -> list:
    """
    Adds a text_input() object to the sidebar for each column in the DataFrame. The default values are the current
    names. It then collects all the names to a list that is returned as output.

    :param df: DataFrame to read column names from.
    :param has_header: True if the DataFrame has a header. False if it does not.

    :return: List of column names.
    """
    st.sidebar.write("Rename columns:")
    output_list = []
    if has_header:
        for column in df.columns.to_list():
            col_name = st.sidebar.text_input(column, value=column, key=f"{column}_text_input")
            output_list.append(col_name)
    else:
        for i, column in enumerate(df.columns.to_list()):
            col_name = st.sidebar.text_input(f"Col {i}", value=column)
            output_list.append(col_name)

    st.sidebar.divider()

    return output_list


def sort_dataframe(df):
    column_to_sort_by = st.sidebar.selectbox("Sort by", [''] + df.columns.tolist())
    ascending = st.sidebar.checkbox("Ascending", value=True)

    if column_to_sort_by:
        df.sort_values(by=column_to_sort_by, ascending=ascending, inplace=True)

    return df.copy()


def set_chr_flip_bool(new_bool: bool = True) -> None:
    """
    Setter for the st.session_state object key 'apply_chr_prefix_flip'
    :return:
    """
    st.session_state.apply_chr_prefix_flip = new_bool


def main():
    # "st.session_state object", st.session_state  # Uncomment for debugging
    if 'apply_chr_prefix_flip' not in st.session_state:
        st.session_state.apply_chr_prefix_flip = False

    st.title("Genomic Data File Re-formatter 🧬")
    st.write("Welcome to the Genomic Data File Re-formatter!")
    st.write("The goal of this app is to provide a simple and painless interface to reformat BED or IGV GWAS files, "
             "although you can use it for any text file containing tabular data. The reformatter allows for renaming "
             "columns, sorting values, and adding/removing the prefix 'chr' to/from a particular column.")
    st.write("Before uploading your file, please select the separator and whether the file has a header.")

    # Collect info about separator and header before reading the file with Pandas
    # Define separator of the input file
    separator = st.selectbox("Separator", ('\\t', ','))
    if separator == '\\t':  # Deal with the escaped character
        separator = '\t'

    input_header_bool = st.checkbox("Input file has header", value=True)
    header_arg = 0 if input_header_bool else None  # Pandas will use the 0th row as header, or none at all

    st.divider()

    # Upload file
    data_file = st.file_uploader("Upload File", key="input_file")

    if data_file is not None:
        df = pd.read_csv(data_file, sep=separator, header=header_arg)

        st.divider()
        st.header("Your table 📝")
        # Create an empty placeholder for the updated DataFrame
        updated_df_placeholder = st.empty()

        st.divider()

        # Generate the 'text_input' elements on the sidebar that allow to rename the columns
        new_names_list = column_renamer(df, input_header_bool)

        # Create a new DataFrame with the updated column names
        updated_df = df.rename(columns=dict(zip(df.columns, new_names_list)))

        # Sort the DataFrame based on a column of choice
        updated_df = sort_dataframe(updated_df)

        # Manage the chromosome prefix
        st.write("Add or remove the 'chr' prefix:")
        chromosome_col = st.selectbox("The Chromosome column is", [''] + updated_df.columns.tolist(),
                                      key="chromosome_column")

        if chromosome_col:
            chr_prefix_button = st.button("Apply Prefix Manipulation", on_click=set_chr_flip_bool)
            if st.session_state.apply_chr_prefix_flip:
                if updated_df[chromosome_col].dtype != object:  # Cast to str if it is not already
                    updated_df[chromosome_col] = updated_df[chromosome_col].astype(str)

                updated_df[chromosome_col] = updated_df[chromosome_col].apply(
                    lambda x: x.lstrip("chr") if x.startswith("chr") else "chr" + x)

        # Display the updated DataFrame
        updated_df_placeholder.dataframe(updated_df, use_container_width=True)

        st.divider()

        # Download the updated DataFrame as a CSV file
        output_separator = st.selectbox("Separator of the output file:", ('\\t', ','))
        if output_separator == '\\t':  # Deal with the escaped character
            output_separator = '\t'
            output_file_extension = 'tsv'
        elif output_separator == ',':
            output_file_extension = 'csv'
        output_has_header = st.checkbox("Include header", value=True)
        if st.button("Download Updated DataFrame"):
            csv = updated_df.to_csv(index=False, sep=output_separator, header=output_has_header)
            b64 = base64.b64encode(csv.encode()).decode()
            href = f'<a href="data:file/{output_file_extension};base64,{b64}" download="updated_dataframe.{output_file_extension}">Download {output_file_extension.upper()} File</a>'
            st.markdown(href, unsafe_allow_html=True)


if __name__ == "__main__":
    main()

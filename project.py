"""
Name:       Matthew O'Neil
CS230:      6
Data:       London Pubs
URL:
Description:
This program analyzes the Excel file London Pubs and uses the data to generate some cool and useful information from it.
The program contains a map of the U.K. with the Pubs appearing on the map. They are represented by a blue dot and their
names and addresses appear when hovering over the dot.
The program also contains two different informational charts and a pivot table displaying the parts of the dataset.
"""

import pandas as pd
import streamlit as st
import plotly.express as px

# [PY1] A function with two or more parameters, one of which has a default value
def load_data(file_path="open_pubs_10000_sample.xlsx"):
    """Load the London Pubs dataset."""
    df = pd.read_excel(file_path)
    return df

# [DA1] Cleaning or manipulating data
def clean_data(df):
    """Clean the London Pubs dataset."""
    # Remove any rows with missing values
    df.dropna(inplace=True)

    # Convert latitude and longitude columns to numeric
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    return df

# [PY2] A function that returns more than one value
def filter_pubs_by_authority(df, authority_name):
    """Filter pubs by local authority."""
    return df[df['local_authority'] == authority_name], df['local_authority'].unique()

# [VIZ4]
# [PY4] A function that returns a value and is called in at least two different places in your program
def display_pubs(df, filtered_df):
    """Display pubs on an interactive map."""
    # Create an interactive map using Plotly
    fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name="name", zoom=10, height=500)
    fig.update_layout(mapbox_style="open-street-map")

    if filtered_df is not None:
        # Update the existing map with markers for the filtered pubs
        fig.update_traces(
            lat=filtered_df['latitude'],
            lon=filtered_df['longitude'],
            customdata=filtered_df[['name', 'address']],
            hovertemplate="<b>%{customdata[0]}</b><br>%{customdata[1]}<extra></extra>",
            hoverinfo="text",
        )
    # Display the updated map
    st.plotly_chart(fig)

# [PY5] A dictionary where you write code to access its keys, values, or items
def get_local_authority_options(df):
    """Get local authority options for select box."""
    return {authority: authority for authority in df['local_authority'].unique()}

# [DA5]
# [PY3] A function that returns a value and is called in at least two different places in your program
def filter_pubs_by_name_and_authority(df, pub_name, authority_name):
    """Filter pubs by name and local authority."""
    filtered_df = df[(df['name'].str.contains(pub_name, case=False)) & (df['local_authority'] == authority_name)]
    return filtered_df

# [ST1], [ST2], [ST3] At least three Streamlit different widgets
def main():
    st.title("London Pubs Explorer")

    # Load and clean the data
    df = load_data()
    df = clean_data(df)

    #  [ST1] Sidebar input for local authority
    authority_name = st.sidebar.selectbox("Select Local Authority", options=get_local_authority_options(df))

    # [ST4] Page design features
    st.sidebar.header("Explore London Pubs")
    st.sidebar.write("Select a local authority to view pubs on the map.")
    st.sidebar.write("You can also filter pubs by name.")

    # [DA4]
    # [ST1] Text input widget for pub name
    pub_name = st.sidebar.text_input("Enter Pub Name", "")

    # [ST2] Button widgets for Show Pub and Reset
    col1, col2 = st.sidebar.columns([2, 1])
    show_pub_button = col1.button("Show Pub")
    reset_button = col2.button("Reset Map")

    if show_pub_button:
        filtered_df = filter_pubs_by_name_and_authority(df, pub_name, authority_name)
        st.subheader("Map of London Pubs")
        display_pubs(df, filtered_df)
    elif reset_button:
        st.subheader("Map of London Pubs")
        display_pubs(df, None)
    else:
        # [ST3] Map widget
        st.subheader("Map of London Pubs")
        display_pubs(df, None)  # Pass None as filtered_df when not filtering

    # [VIZ1]
    st.subheader("Top Local Authorities with the Most Pubs")
    top_local_authorities = st.selectbox("Select number of top local authorities to display:", [5, 10, 15, 20], index=2)

    pub_counts = df['local_authority'].value_counts().head(top_local_authorities)
    df_top_n = pd.DataFrame({'local_authority': pub_counts.index, 'pub_count': pub_counts.values})

    if not df_top_n.empty:
        fig = px.pie(df_top_n, names='local_authority', values='pub_count', title=f"Distribution of Pubs by Local Authority (Top {top_local_authorities})")
        fig.update_traces(textinfo='percent+label', showlegend=True)
        st.plotly_chart(fig)
        st.write("This pie chart illustrates the distribution of pubs across different local authorities in London.")
    else:
        st.warning("No data available to display the pie chart.")

    # [DA9]
    # Calculate the sum of pubs for each postal code
    df['postcode_prefix'] = df['postcode'].str[:2]  # Extract first two characters of postcode
    pub_counts_by_postcode = df['postcode_prefix'].value_counts().head(10)

    # Create a DataFrame for the top ten postal codes and their pub counts
    df_top_10_postcodes = pd.DataFrame(
        {'postcode_prefix': pub_counts_by_postcode.index, 'pub_count': pub_counts_by_postcode.values})

    # [VIZ2] New pie chart for top ten postal codes with most pubs
    st.subheader("Top Ten Postal Codes with the Most Pubs")
    if not df_top_10_postcodes.empty:
        fig_postcode = px.pie(df_top_10_postcodes, names='postcode_prefix', values='pub_count',
                              title="Distribution of Pubs by Postal Code Prefix")
        fig_postcode.update_traces(textinfo='percent+label', showlegend=True)
        st.plotly_chart(fig_postcode)
        st.write("This pie chart shows the distribution of pubs in London based on the postal code prefixes. This provides a more vague area but still provides a unique way of analyzing the distribution of pubs across the U.K.")
    else:
        st.warning("No data available to display the pie chart for postal codes.")

    # [VIZ3] Bar chart for top ten pub names
    st.subheader("Top Ten Pub Names")
    pub_counts_by_name = df['name'].value_counts().head(10)
    if not pub_counts_by_name.empty:
        fig_names = px.bar(pub_counts_by_name, x=pub_counts_by_name.index, y=pub_counts_by_name.values, title="")
        fig_names.update_xaxes(title_text="Pub Name")
        fig_names.update_yaxes(title_text="Number of Pubs")

        st.plotly_chart(fig_names)
        st.write("This bar chart displays the top ten most popular pub names in London and tallies the how many pubs share these names. It is a unique and interesting fact that can be calculated from the dataset.")
    else:
        st.warning("No data available to display the bar chart for pub names.")

    # Select columns to include in the pivot table
    columns_to_include = ['id', 'name', 'address', 'postcode', 'local_authority']

    # Drop duplicate rows based on the selected columns
    df_unique = df[columns_to_include].drop_duplicates()

    # [DA6] Create a pivot table to summarize the number of pubs by selected columns
    pivot_table = df_unique.pivot_table(index=columns_to_include, aggfunc='size')

    # Display the pivot table
    st.write("Pivot Table - Number of Pubs by Selected Columns")
    st.write(pivot_table)

if __name__ == "__main__":
    main()




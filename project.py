import pandas as pd
import streamlit as st
import plotly.express as px

# [PY1] A function with two or more parameters, one of which has a default value
def load_data(file_path="open_pubs_10000_sample.xlsx"):
    """Load the London Pubs dataset."""
    df = pd.read_excel(file_path)
    return df

# [DA1]
def clean_data(df):
    """Clean the London Pubs dataset."""
    # Remove any rows with missing values
    df.dropna(inplace=True)

    # Convert latitude and longitude columns to numeric
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    print("Null values in latitude column after cleaning:", df['latitude'].isnull().sum())

    return df

# [PY2] A function that returns more than one value
def filter_pubs_by_authority(df, authority_name):
    """Filter pubs by local authority."""
    return df[df['local_authority'] == authority_name], df['local_authority'].unique()

# [PY3] A function that returns a value and is called in at least two different places in your program
def display_pubs(df, filtered_df):
    """Display pubs on an interactive map."""
    print("Displaying pubs...")  # Debug print
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
        )

    # Display the updated map
    st.plotly_chart(fig)

# [PY5] A dictionary where you write code to access its keys, values, or items
def get_local_authority_options(df):
    """Get local authority options for selectbox."""
    return {authority: authority for authority in df['local_authority'].unique()}

# [PY3] A function that returns a value and is called in at least two different places in your program
def filter_pubs_by_name_and_authority(df, pub_name, authority_name):
    """Filter pubs by name and local authority."""
    print("Filtering pubs by name:", pub_name, "and authority:", authority_name)  # Debug print
    filtered_df = df[(df['name'].str.contains(pub_name, case=False)) & (df['local_authority'] == authority_name)]
    print("Filtered dataframe shape:", filtered_df.shape)  # Debug print
    return filtered_df

# [ST1], [ST2], [ST3] At least three Streamlit different widgets
def main():
    st.title("London Pubs Explorer")

    # Load and clean the data
    df = load_data()
    df = clean_data(df)

    # Sidebar input for local authority
    authority_name = st.sidebar.selectbox("Select Local Authority", options=get_local_authority_options(df))

    # [DA2] Sorting data in ascending or descending order, by one or more columns
    sorted_df = df.sort_values(by='name', ascending=True)

    # [ST4] Page design features
    st.sidebar.header("Explore London Pubs")
    st.sidebar.write("Select a local authority to view pubs on the map.")
    st.sidebar.write("You can also filter pubs by name.")

    # [ST1] Dropdown widget
    pub_name = st.sidebar.text_input("Enter Pub Name", "")

    # [ST2] Button widget
    show_pub_button = st.sidebar.button("Show Pub")
    reset_button = st.sidebar.button("Reset Map")

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

    # Calculate the sum of pubs for each local authority
    pub_counts = df['local_authority'].value_counts()
    top_local_authorities = st.selectbox("Select number of top local authorities to display:", [5, 10, 15, 20], index=1)

    top_n_local_authorities = pub_counts.head(top_local_authorities)

    # Create a DataFrame from the selected number of top local authorities and their pub counts
    df_top_n = pd.DataFrame(
        {'local_authority': top_n_local_authorities.index, 'pub_count': top_n_local_authorities.values})

    # [VIZ2] Pie chart
    st.subheader(f"Top {top_local_authorities} Local Authorities with the Most Pubs")
    if not df_top_n.empty:  # Check if the DataFrame is not empty
        fig = px.pie(df_top_n, names='local_authority', values='pub_count',
                     title="Distribution of Pubs by Local Authority")
        fig.update_traces(textinfo='percent+label', showlegend=True)  # Show percentage and label in the legend
        st.plotly_chart(fig)
    else:
        st.warning("No data available to display the pie chart.")

if __name__ == "__main__":
    main()



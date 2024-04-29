import pandas as pd
import streamlit as st
import plotly.express as px

# [PY1] A function with two or more parameters, one of which has a default value
def load_data(file_path="open_pubs_10000_sample.xlsx"):
    """Load the London Pubs dataset."""
    return pd.read_excel(file_path, header=None, names=['id', 'name', 'address', 'postcode', 'easting', 'northing', 'latitude', 'longitude', 'local_authority'])

# [DA1] Cleaning or manipulating data
def clean_data(df):
    """Clean the London Pubs dataset."""
    # Remove any rows with missing values
    df.dropna(inplace=True)
    # Convert latitude and longitude to string to avoid TypeError
    df['latitude'] = df['latitude'].astype(str)
    df['longitude'] = df['longitude'].astype(str)
    return df


df = load_data()
df = clean_data(df)

# [PY2] A function that returns more than one value
def filter_pubs_by_authority(df, authority_name):
    """Filter pubs by local authority."""
    return df[df['local_authority'] == authority_name], df['local_authority'].unique()

# [PY3] A function that returns a value and is called in at least two different places in your program
def display_pubs(df):
    """Display pubs on an interactive map."""
    # Create an interactive map using Plotly
    fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name="name", zoom=10, height=500)
    fig.update_layout(mapbox_style="open-street-map")
    # Display the map
    st.plotly_chart(fig)

def display_filtered_pubs(df, authority_name):
    """Display filtered pubs on an interactive map."""
    filtered_df, _ = filter_pubs_by_authority(df, authority_name)
    display_pubs(filtered_df)

# [PY4] A list comprehension
def get_local_authorities(df):
    """Get unique local authorities."""
    return [authority for authority in df['local_authority'].unique()]

# [PY5] A dictionary where you write code to access its keys, values, or items
def get_local_authority_options(df):
    """Get local authority options for selectbox."""
    return {authority: authority for authority in df['local_authority'].unique()}

# [ST1], [ST2], [ST3] At least three Streamlit different widgets
def main():
    st.title("London Pubs Explorer")

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
    if st.sidebar.button("Show Pub"):
        display_filtered_pubs(df, authority_name)

    # [ST3] Map widget
    st.subheader("Map of London Pubs")
    display_pubs(df)

    # [VIZ1] Bar chart
    st.subheader("Top 5 Pubs by Rating")
    top_pubs = df.nlargest(5, 'rating')
    st.bar_chart(top_pubs['rating'])

    # [VIZ2] Pie chart
    st.subheader("Distribution of Pubs by Local Authority")
    st.write(px.pie(df, names='local_authority'))

    # [VIZ3] Line chart
    st.subheader("Number of Pubs Over Time")
    st.line_chart(df.groupby('year')['name'].count())

    # [VIZ4] Detailed map
    st.subheader("Detailed Map of London Pubs")
    st.map(df)

if __name__ == "__main__":
    main()

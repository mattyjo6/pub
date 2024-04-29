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

df = load_data()
df = clean_data(df)


# [PY2] A function that returns more than one value
def filter_pubs_by_authority(df, authority_name):
    """Filter pubs by local authority."""
    return df[df['local_authority'] == authority_name], df['local_authority'].unique()

# [PY3] A function that returns a value and is called in at least two different places in your program
# [PY3] A function that returns a value and is called in at least two different places in your program
def display_pubs(df, filtered_df=None):
    """Display pubs on an interactive map."""
    # Create an interactive map using Plotly
    fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name="name", zoom=10, height=500)
    fig.update_layout(mapbox_style="open-street-map")
    
    if filtered_df is not None:
        # Add a marker for the filtered pub
        filtered_fig = px.scatter_mapbox(filtered_df, lat="latitude", lon="longitude", hover_name="name",
                                         text="address", zoom=10, height=500)
        # Update the marker properties
        filtered_fig.update_traces(marker=dict(size=12, opacity=0.8, color='red'), selector=dict(mode='markers'))
        fig.add_trace(filtered_fig.data[0])
    
    # Display the map
    st.plotly_chart(fig)

    
def filter_pubs_by_name(df, pub_name):
    """Filter pubs by name."""
    filtered_df = df[df['name'].str.contains(pub_name, case=False)]
    return filtered_df



def filter_pubs_by_authority(df, authority_name):
    """Filter pubs by local authority."""
    filtered_df, _ = filter_pubs_by_authority(df, authority_name)
    # Ensure latitude and longitude columns are numeric
    filtered_df['latitude'] = pd.to_numeric(filtered_df['latitude'], errors='coerce')
    filtered_df['longitude'] = pd.to_numeric(filtered_df['longitude'], errors='coerce')
    # Drop rows with null latitude or longitude values
    filtered_df = filtered_df.dropna(subset=['latitude', 'longitude'])
    return filtered_df, df['local_authority'].unique()




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
        filtered_df, _ = filter_pubs_by_name(df, pub_name)
        display_pubs(filtered_df)



    # [ST3] Map widget
    st.subheader("Map of London Pubs")
    display_pubs(df)

    # [VIZ2] Pie chart
    st.subheader("Distribution of Pubs by Local Authority")
    st.write(px.pie(df, names='local_authority'))

    # [VIZ4] Detailed map
    st.subheader("Detailed Map of London Pubs")
    st.map(df)


if __name__ == "__main__":
    main()


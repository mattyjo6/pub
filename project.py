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

# [PY3] A function that returns a value and is called in at least two different places in your program
def display_pubs(df, filtered_df=None):
    """Display pubs on an interactive map."""
    # Create an interactive map using Plotly
    fig = px.scatter_mapbox(df, lat="latitude", lon="longitude", hover_name="name", zoom=10, height=500)
    fig.update_layout(mapbox_style="open-street-map")

    if filtered_df is not None:
        # Add markers for the filtered pubs
        filtered_fig = px.scatter_mapbox(filtered_df, lat="latitude", lon="longitude", hover_name="name",
                                         text="address", zoom=10, height=500)
        fig.add_trace(filtered_fig.data[0])

    # Display the map
    st.plotly_chart(fig)

# [ST1], [ST2], [ST3] At least three Streamlit different widgets
def main():
    st.title("London Pubs Explorer")

    # Load the data
    df = load_data()
    # Clean the data
    df = clean_data(df)

    # Calculate the sum of pubs for each local authority
    pub_counts = df['local_authority'].value_counts()
    top_10_local_authorities = pub_counts.head(10)

    # Create a DataFrame from the top 10 local authorities and their pub counts
    df_top_10 = pd.DataFrame({'local_authority': top_10_local_authorities.index, 'pub_count': top_10_local_authorities.values})

    # [VIZ2] Pie chart
    st.subheader("Top 10 Local Authorities with the Most Pubs")
    if not df_top_10.empty:  # Check if the DataFrame is not empty
        fig = px.pie(df_top_10, names='local_authority', values='pub_count', title="Distribution of Pubs by Local Authority")
        fig.update_traces(textinfo='percent+label', showlegend=True)  # Show percentage and label in the legend
        st.plotly_chart(fig)
    else:
        st.warning("No data available to display the pie chart.")

    # [PY3] A function that returns a value and is called in at least two different places in your program
    display_pubs(df)

if __name__ == "__main__":
    main()


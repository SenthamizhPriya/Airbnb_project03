import streamlit as st
import pandas as pd
import folium
from streamlit_folium import folium_static
from folium import IFrame
from folium.plugins import HeatMap
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

def set_gradient_bg():

    st.markdown(
        """
        <style>
        .stApp {
            background-image: linear-gradient(120deg,#FFB5BC, #F54655);
        }

        [data-testid="stSidebar"] {
            background-color: #ffffff;
        }

        /* Customizing button colors in the sidebar */
        .stButton > button {
            display: block;
            width: 100%;
            color: #000000;
            background-color: transparent;
            border-color: #FF5A5F;
            margin-bottom: 10px;
        }

        .stButton > button:hover {
            border-color: #FF5A5F;
            color: #000000;
        }

        </style>
        """,
        unsafe_allow_html=True
    )

def intro_page():

    set_gradient_bg()

    st.markdown("<h1 style='text-align: center; color: #ffffff;'>Airbnb Analysis</h1>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])  
    with col2:
        st.image('Airbnb.jpg', width=350, output_format="auto")

    st.markdown(f"""
        <div style='text-align: left;'>
            <h3 style='color: #ffffff;'>Tools Used</h3>
            <ul style='font-size: 16px;color: #ffffff;'>
                <li><b>Python</b>: For Data Extraction and visualisations (Backend Development).</li>
                <li><b>Pandas</b>: For Converting Data to Data Frame.</li>
                <li><b>Power BI</b>: For Visualisations.</li>
                <li><b>Streamlit</b>: For Creating the Web Application.</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)


    st.markdown("<p style='text-align: right; font-size: 16px;color: #ffffff;margin-bottom: 0px; '>Submitted by</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: right;color: #ffffff; font-size: 18px;'><b>N. Senthamizh Priya</b></p>", unsafe_allow_html=True)

def Geospatial_visualisation_page():

    Geospatial_df = pd.read_csv('Geospatial_data.csv')

    countries = Geospatial_df['Country'].unique()
    selected_countries = st.multiselect('Select countries', countries, default=[])

    Room_type = Geospatial_df['Room type'].unique()
    selected_Room_type = st.multiselect('Select Room type', Room_type, default=[])

    col1, col2 = st.columns(2)

    with col1:
        min_price = st.number_input(
            'Minimum price', 
            min_value=int(Geospatial_df['Price'].min()), 
            max_value=int(Geospatial_df['Price'].max()), 
            value=int(Geospatial_df['Price'].min())
        )

    with col2:
        max_price = st.number_input(
            'Maximum price', 
            min_value=int(Geospatial_df['Price'].min()), 
            max_value=int(Geospatial_df['Price'].max()), 
            value=int(Geospatial_df['Price'].max())
        )

    min_rating, max_rating = st.slider(
        'Select rating range',
        min_value=int(Geospatial_df['Rating'].min()),
        max_value=int(Geospatial_df['Rating'].max()),
        value=(int(Geospatial_df['Rating'].min()), int(Geospatial_df['Rating'].max()))
    )

    if not selected_Room_type:
        filtered_df = Geospatial_df[
            (Geospatial_df['Country'].isin(selected_countries)) &
            (Geospatial_df['Price'] >= min_price) &
            (Geospatial_df['Price'] <= max_price) &
            (Geospatial_df['Rating'] >= min_rating) &
            (Geospatial_df['Rating'] <= max_rating)
        ]
    else:
        filtered_df = Geospatial_df[
            (Geospatial_df['Country'].isin(selected_countries)) &
            (Geospatial_df['Room type'].isin(selected_Room_type)) &
            (Geospatial_df['Price'] >= min_price) &
            (Geospatial_df['Price'] <= max_price) &
            (Geospatial_df['Rating'] >= min_rating) &
            (Geospatial_df['Rating'] <= max_rating)
        ]
    
    map = folium.Map(location=[0, 0], zoom_start=2)

    for _, row in filtered_df.iterrows():

        formatted_rating = f"{float(row['Rating'])}"
        
        html = f"""
        <b>Country:</b> {row['Country']}<br>
        <b>City:</b> {row['City']}<br>
        <b>Suburb:</b> {row['Suburb']}<br>
        <b>Price:</b> {row['Price']}<br>
        <b>Rating:</b> {formatted_rating}<br>
        <b>Room type:</b> {row['Room type']}<br>
        """
        iframe = IFrame(html, width=200, height=150)
        popup = folium.Popup(iframe, max_width=200)
        
        folium.Marker(
            location=[row['Longitude'], row['Latitude']],  
            popup=popup
        ).add_to(map)

    map_with_heatmap = folium.Map(location=[0, 0], zoom_start=2)
    heat_data = [[row['Longitude'], row['Latitude']] for index, row in filtered_df.iterrows()]
    HeatMap(heat_data).add_to(map_with_heatmap)

    if st.button('Display Map'):
        st.subheader("Map with Markers")
        folium_static(map)
        
        st.subheader("Listings Heatmap")
        folium_static(map_with_heatmap)

def Room_Property_Pricing():

    Price_df = pd.read_csv('Price_data.csv')

    st.markdown("<h1 style='text-align: center; font-size: 32px;color: #ffffff;'>Country-wise Price Trends: Room and Property Type Insights</h1>", unsafe_allow_html=True)

    st.markdown("""<hr style="height:1px;border:none;color:#FF5A5F;background-color:#FF5A5F;" /> """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:

            room_type = st.selectbox("Select Room type", Price_df['Room type'].unique())

            # Filter data based on selected property type
            filtered_room_data = Price_df[Price_df['Room type'] == room_type]

            # Compute mean prices for each country for the selected property type
            mean_prices = filtered_room_data.groupby('Country')['Price'].mean().reset_index()

            # Create a bar plot
            st.subheader(f"Prices of {room_type}")
            fig3, ax = plt.subplots()

            sns.barplot(x='Country', y='Price', data=mean_prices, ax=ax,color='#FF5A5F')

            # Customize font sizes
            ax.set_title(f"Prices of {room_type}", fontsize=12)
            ax.set_xlabel("Country", fontsize=10)
            ax.set_ylabel("Average Price", fontsize=10)
            ax.tick_params(axis='both', which='major', labelsize=8)
            plt.xticks(rotation=45, ha='right', fontsize=10)
            plt.yticks(fontsize=8)

            # Display the plot

            st.pyplot(fig3)

    with col2:
            country = st.selectbox("Select country", Price_df['Country'].unique())

            # Filter data based on selected country
            filter_price_data = Price_df[Price_df['Country'] == country]

            # Create a bar plot
            st.subheader(f"Room Type Prices")
            fig4, ax = plt.subplots()
            sns.barplot(x='Room type', y='Price', data=filter_price_data, ax=ax,color='#FF5A5F')

            ax.set_title(f"Room Prices by Type in {country}", fontsize=12)
            ax.set_xlabel("Room Type", fontsize=10)
            ax.set_ylabel("Price", fontsize=10)
            ax.tick_params(axis='both', which='major', labelsize=8)
            plt.xticks(rotation=45, ha='right', fontsize=10) 
            plt.yticks(fontsize=8)

            # Display the plot
            st.pyplot(fig4)

    st.markdown("""<hr style="height:1px;border:none;color:#FF5A5F;background-color:#FF5A5F;" /> """, unsafe_allow_html=True)

    col3, col4 = st.columns([2,2])

    with col3:

        property_type = st.selectbox("Select Property type", Price_df['Property type'].unique())

        # Filter data based on selected property type
        filtered_prop_data = Price_df[Price_df['Property type'] == property_type]

        # Compute mean prices for each country for the selected property type
        mean_prices = filtered_prop_data.groupby('Country')['Price'].mean().reset_index()

        # Create a bar plot
        st.subheader(f"Prices of {property_type}")
        fig3, ax = plt.subplots()
        sns.barplot(x='Country', y='Price', data=mean_prices, ax=ax,color='#FF5A5F')

        # Customize font sizes
        ax.set_title(f"Prices of {property_type}", fontsize=12)
        ax.set_xlabel("Country", fontsize=10)
        ax.set_ylabel("Average Price", fontsize=10)
        ax.tick_params(axis='both', which='major', labelsize=8)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=8)

        # Display the plot

        st.pyplot(fig3)

    with col4:

        country = st.selectbox("Select Country", Price_df['Country'].unique())

        # Filter data based on selected country
        filter_price_data = Price_df[Price_df['Country'] == country]

        # Create a bar plot
        st.subheader(f"Property Prices")
        fig, ax = plt.subplots()
        sns.barplot(x='Property type', y='Price', data=filter_price_data, ax=ax,color='#FF5A5F')

        ax.set_title(f"Property Prices by Type in {country}", fontsize=12)
        ax.set_xlabel("Property Type", fontsize=10)
        ax.set_ylabel("Price", fontsize=10)
        ax.tick_params(axis='both', which='major', labelsize=8)
        plt.xticks(rotation=45, ha='right', fontsize=10)
        plt.yticks(fontsize=8)

        # Display the plot
        st.pyplot(fig)

    st.markdown("""<hr style="height:1px;border:none;color:#FF5A5F;background-color:#FF5A5F;" /> """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; font-size: 32px;color: #ffffff;'>Availability by Cities</h1>", unsafe_allow_html=True)

    Availability_df = pd.read_csv('Availability_data.csv')
    Availability_df.columns = Availability_df.columns.str.strip()
    
    Availability_df = Availability_df[~Availability_df['City'].isin(['Other (Domestic)', 'Other (International)'])] 
    

    city_availability = Availability_df.groupby('City')[['next 30', 'next 60', 'next 90', 'next 365']].sum().reset_index()

    # Create the grouped bar chart
    fig = go.Figure()

    # Add traces for each availability period
    fig.add_trace(go.Bar(
        x=city_availability['City'],
        y=city_availability['next 30'],
        name='30 Days',
        marker_color='#767676'
    ))
    fig.add_trace(go.Bar(
        x=city_availability['City'],
        y=city_availability['next 60'],
        name='60 Days',
        marker_color='#484848'
    ))
    fig.add_trace(go.Bar(
        x=city_availability['City'],
        y=city_availability['next 90'],
        name='90 Days',
        marker_color='#FF979A'
    ))
    fig.add_trace(go.Bar(
        x=city_availability['City'],
        y=city_availability['next 365'],
        name='365 Days',
        marker_color='#FF5A5F'
    ))

    # Update the layout for grouped bars
    fig.update_layout(
        barmode='group',
        title='Availability for Different Periods by City',
        xaxis_title='City',
        yaxis_title='Availability',
        xaxis_tickangle=-45,
        legend_title='Availability Period'
    )

    # Display the chart in Streamlit
    st.plotly_chart(fig)


def Neighborhood_page():

    Price_df = pd.read_csv('Price_data.csv')

    st.markdown("<h1 style='text-align: center; font-size: 32px;color: #ffffff;'>Neighborhood Price Analysis: A comparison </h1>", unsafe_allow_html=True)

    country = st.selectbox("Select your country", Price_df['Country'].unique())

    City_data = Price_df[Price_df['Country'] == country]

    # City filter (dependent on selected country)
    city = st.selectbox("Select your city", City_data['City'].unique())

    # Filter the data based on the selected city
    Suburb_data = City_data[City_data['City'] == city]

    # Compute mean prices for each suburb in the selected city
    mean_suburb_prices = Suburb_data.groupby('Suburb')['Price'].mean().reset_index()

    # Sort suburbs by average price in descending order
    mean_suburb_prices = mean_suburb_prices.sort_values(by='Price', ascending=False)


    #create chart
    fig5, ax = plt.subplots(figsize=(10,17))
    sns.barplot(x='Price', y='Suburb', data=mean_suburb_prices, ax=ax,color='#FF5A5F')

    #customise
    ax.set_title(f"Average Price of Suburbs in {city}({country})", fontsize=16)
    ax.set_xlabel("Average Price", fontsize=14)
    ax.set_ylabel("Suburbs", fontsize=14)
    ax.tick_params(axis='both', which='major', labelsize=11.5)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(True)
    ax.spines['bottom'].set_visible(False)

    for i in ax.containers:
        ax.bar_label(i, fmt='%.2f', label_type='edge', fontsize=11.5)

    if st.button('Display the suburb prices'):

    # Display the plot
        st.pyplot(fig5)

def Correlation_page():

    # Set the title
    st.markdown("<h1 style='text-align: center; font-size: 32px;color: #ffffff;'>Correlation Heatmaps </h1>", unsafe_allow_html=True)

    st.markdown("""<hr style="height:1px;border:none;color:#FF5A5F;background-color:#FF5A5F;" /> """, unsafe_allow_html=True)

    # Load the data
    Corelation_df = pd.read_csv('Corelation_data.csv')

    # Define the columns for correlation
    Corr_01 = ['Price', 'Rating', 'Minimum nights', 'Maximum nights', 'Bedroom count', 'Bathroom count']

    # Calculate the correlation matrix
    correlation_matrix = Corelation_df[Corr_01].corr()

    # Plot the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='Blues', linewidths=.5)
    plt.title('Price and Rating vs Nights and Rooms count')

    # Display the plot in Streamlit
    st.pyplot(plt.gcf())

    # PLOT 3

    # Define the columns for correlation
    Corr_03 = ['Rating','Review count','Cleanliness score','Communication score','Location score','Pricevalue score']


    # Calculate the correlation matrix
    correlation_matrix = Corelation_df[Corr_03].corr()

    # Plot the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='Blues', linewidths=.5)
    plt.title('Price and Review scores')

    # Display the plot in Streamlit
    st.pyplot(plt.gcf())

    # PLOT 2

    # Define the columns for correlation
    Corr_02 = ['Price','Super host','Review count','Rating']

    # Calculate the correlation matrix
    correlation_matrix = Corelation_df[Corr_02].corr()

    # Plot the heatmap
    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='Blues', linewidths=.5)
    plt.title('Price and Availability')

    # Display the plot in Streamlit
    st.pyplot(plt.gcf())

def Super_host_page():

    Superhost_df = pd.read_csv('Superhost_data.csv')

    st.markdown("<h1 style='text-align: center; font-size: 32px;color: #ffffff;'>Superhost Analysis: Country and city wise insights</h1>", unsafe_allow_html=True)

    st.markdown("""<hr style="height:1px;border:none;color:#FF5A5F;background-color:#FF5A5F;" /> """, unsafe_allow_html=True)

    col5, col6 = st.columns([5,3])

    st.markdown("""<hr style="height:1px;border:none;color:#FF5A5F;background-color:#FF5A5F;" /> """, unsafe_allow_html=True)

    col7, col8 = st.columns([5,3])

    with col5:
        st.subheader("Superhost by Country")

        # Count superhosts by country
        country_counts = Superhost_df.groupby(['Country', 'Super host']).size().reset_index(name='Count')
        country_counts['Super host'] = country_counts['Super host'].replace({True: 'Superhost', False: 'Not Superhost', None: 'Not Available'})

        custom_colors = {
            'Superhost': '#FF5A5F',
            'Not Superhost': '#767676',
            'Not Available': '#767676'
        }

        # Bar chart for countries
        plt.figure(figsize=(8, 7))
        sns.barplot(data=country_counts, x='Country', y='Count', hue='Super host', palette=custom_colors)
        plt.title("Superhost Status by Country")
        plt.xlabel("Country",fontsize=14)
        plt.ylabel("Count",fontsize=14)
        plt.xticks(rotation=90,fontsize=13)
        for container in plt.gca().containers:
            plt.gca().bar_label(container)
        st.pyplot(plt.gcf())
        plt.clf()

    with col6:
        Superhost_df.columns = Superhost_df.columns.str.strip()

        st.subheader("Average Price")

        # Calculate average price by country
        country_avg_price = Superhost_df.groupby('Country')['Price'].mean().reset_index()
        country_avg_price['Price'] = country_avg_price['Price'].round(2)

        # Bar chart for average price by country
        plt.figure(figsize=(8,13))
        sns.barplot(data=country_avg_price, x='Country', y='Price', palette=['#FF5A5F'])
        plt.title("Average Price by Country",fontsize=16)
        plt.xlabel("Country",fontsize=16)
        plt.ylabel("Average Price",fontsize=16)
        plt.xticks(rotation=90,fontsize=18)
        for container in plt.gca().containers:
            plt.gca().bar_label(container)
        st.pyplot(plt.gcf())
        plt.clf()


    with col7:
        st.subheader("Superhost by City")

        # Count superhosts by city
        city_counts = Superhost_df.groupby(['City', 'Super host']).size().reset_index(name='Count')
        city_counts['Super host'] = city_counts['Super host'].replace({True: 'Superhost', False: 'Not Superhost', None: 'Not Available'})

        custom_colors = {
            'Superhost': '#FF5A5F',
            'Not Superhost': '#767676',
            'Not Available': '#767676'
        }

        # Bar chart for cities
        plt.figure(figsize=(8, 6))
        sns.barplot(data=city_counts, x='City', y='Count', hue='Super host', palette=custom_colors)
        plt.title("Superhost Status by City")
        plt.xlabel("City", fontsize=14)
        plt.ylabel("Count", fontsize=14)
        plt.xticks(rotation=90, fontsize=13)
        for container in plt.gca().containers:
            plt.gca().bar_label(container)
        st.pyplot(plt.gcf())
        plt.clf()

    with col8:
        st.subheader("Average Price by City")

        # Calculate average price by city
        city_avg_price = Superhost_df.groupby('City')['Price'].mean().reset_index()
        city_avg_price['Price'] = city_avg_price['Price'].round(2)

        # Bar chart for average price by city
        plt.figure(figsize=(8, 12))
        sns.barplot(data=city_avg_price, x='City', y='Price', palette=['#FF5A5F'])
        plt.title("Average Price by City", fontsize=16)
        plt.xlabel("City", fontsize=16)
        plt.ylabel("Average Price", fontsize=16)
        plt.xticks(rotation=90, fontsize=16)
        for container in plt.gca().containers:
            plt.gca().bar_label(container)
        st.pyplot(plt.gcf())
        plt.clf()

    st.markdown("""<hr style="height:1px;border:none;color:#FF5A5F;background-color:#FF5A5F;" /> """, unsafe_allow_html=True)

    st.markdown("<h1 style='text-align: center; font-size: 32px;color: #ffffff;'>Host-listings Analysis: Market Insights </h1>", unsafe_allow_html=True)

    st.markdown("""<hr style="height:1px;border:none;color:#FF5A5F;background-color:#FF5A5F;" /> """, unsafe_allow_html=True)

    Superhost_df = pd.read_csv('Superhost_data.csv')

    col9, col10 = st.columns([2,2])

    with col9:
        # Calculate averages

            st.subheader('Avg. host listings')

            unique_cities = Superhost_df['City'].unique()

            city_avg_listings = Superhost_df.groupby('City')['Host Listings'].mean().reindex(unique_cities).reset_index()
            city_avg_listings['Host Listings'] = city_avg_listings['Host Listings'].round(2)

                # Create the bar chart
            plt.figure(figsize=(11, 19))        
            ax = sns.barplot(data=city_avg_listings, y='City', x='Host Listings', palette=['#FF5A5F'])
            plt.title("Average Listings per Host by City", fontsize=16)
            plt.xlabel("Average Listings per Host", fontsize=14)
            plt.ylabel("City", fontsize=14)
            plt.xticks(fontsize=20)
            plt.yticks(rotation=45,fontsize=20)
            


                # Display the chart in Streamlit
            st.pyplot(plt.gcf())
            plt.clf() 

    with col10:

        st.subheader('Total listings by city')

        unique_cities = Superhost_df['City'].unique()
        
        city_listing_counts = Superhost_df['City'].value_counts().reindex(unique_cities).reset_index()
        city_listing_counts.columns = ['City', 'Listing Count']

        

            # Create the bar chart
        plt.figure(figsize=(11, 19))
        sns.barplot(data=city_listing_counts, y='City', x='Listing Count', palette=['#FF5A5F'])
        plt.title("Listing Count by City", fontsize=16)
        plt.xlabel("Listing Count", fontsize=14)
        plt.ylabel("City", fontsize=14)
        plt.xticks(fontsize=20)
        plt.yticks(rotation=45,fontsize=20)

            # Display the chart in Streamlit
        st.pyplot(plt.gcf())

    st.subheader('Avg. Host listings vs Total listings')

    unique_cities = Superhost_df['City'].unique()

    # Calculate total listings in each city
    city_listing_counts = Superhost_df['City'].value_counts().reindex(unique_cities).reset_index()
    city_listing_counts.columns = ['City', 'Listing Count']

    # Calculate the average number of listings per host for each city
    city_avg_listings = Superhost_df.groupby('City')['Host Listings'].mean().reindex(unique_cities).reset_index()
    city_avg_listings['Host Listings'] = city_avg_listings['Host Listings'].round(2)

    # Merge the dataframes on 'City'
    merged_data = pd.merge(city_listing_counts, city_avg_listings, on='City')

    # Create the scatter plot with Plotly
    fig = px.scatter(merged_data, 
                    x='Listing Count', 
                    y='Host Listings', 
                    text='City', 
                    labels={
                        'Listing Count': 'Total Listings in City',
                        'Host Listings': 'Average Listings per Host'
                    },
                    title="Number of Listings per Host vs. Total Listings in Each City")

    fig.update_traces(marker=dict(size=12),
                    selector=dict(mode='markers+text'),
                    textposition='top center')

    # Display the chart in Streamlit
    st.plotly_chart(fig)




def main():

    set_gradient_bg()

    st.sidebar.title("Navigation")

    if 'current_page' not in st.session_state:  
        st.session_state.current_page = 'Introduction'

        # Button navigation
    if st.sidebar.button("Introduction"):
        st.session_state.current_page = 'Introduction'
    if st.sidebar.button("Geospatial Visualisation"):
        st.session_state.current_page = 'Geospatial Visualisation'
    if st.sidebar.button("Room & Property Type Pricing"):
        st.session_state.current_page = 'Room & Property Type Pricing'
    if st.sidebar.button("Neighborhood Price trends"):
        st.session_state.current_page = 'Neighborhood Price trends'
    if st.sidebar.button("Correlation Visualisation"):
        st.session_state.current_page = 'Correlation Visualisation'
    if st.sidebar.button("Host Insights"):
        st.session_state.current_page = 'Host Insights'
    

        # Display the selected page
    if st.session_state.current_page == "Introduction":
        intro_page()
    elif st.session_state.current_page == "Geospatial Visualisation":
        Geospatial_visualisation_page()
    elif st.session_state.current_page == "Room & Property Type Pricing":
        Room_Property_Pricing()
    elif st.session_state.current_page == "Neighborhood Price trends":
        Neighborhood_page()
    elif st.session_state.current_page == "Correlation Visualisation":
        Correlation_page()
    elif st.session_state.current_page == "Host Insights":
        Super_host_page()

if __name__ == "__main__":
    main()




import streamlit as st
import pydeck as pdk
import pandas as pd
import matplotlib.pyplot as plt

from PIL import Image





path = 'C:/Users/irinn/OneDrive - Bentley University/New Folder/pythonProjectweb2'

df_explo = pd.read_csv('001nuclear_explosions.csv')
df_explo.rename(columns={"Lat":"lat", "Lon": "lon"}, inplace= True)

which_one = st.sidebar.radio("Please Data you want to see ", [":house:","CUSTOM","US ANALYSIS"])


#Main Page-
if which_one == ":house:":
    st.title('Nuclear Explosions')
    results = df_explo[['WEAPON SOURCE COUNTRY', 'Date.Year',"Data.Type","WEAPON DEPLOYMENT LOCATION",'lat','lon']]

    years_allmap = results[['WEAPON SOURCE COUNTRY','Date.Year','lat','lon']]
    country_map = results[['WEAPON SOURCE COUNTRY']]
    results = df_explo[['WEAPON SOURCE COUNTRY', 'Date.Year', "Data.Type", "WEAPON DEPLOYMENT LOCATION", 'lat', 'lon']]
    results = df_explo[['WEAPON SOURCE COUNTRY', 'Date.Year', 'lat', 'lon']]


    selected_year = st.selectbox("Select Data you want to analyze",
                                 ('ALL YEARS','ALL COUNTRIES','LOCATION' ))

    df_results = df_explo[['WEAPON SOURCE COUNTRY', 'Date.Year', "Data.Type", "WEAPON DEPLOYMENT LOCATION", 'lat', 'lon']]
    if selected_year == 'ALL COUNTRIES':
        country_counts = country_map['WEAPON SOURCE COUNTRY'].value_counts().reset_index()
        country_counts.columns = ['Country', 'Frequency']
        country_counts.set_index('Country', inplace=True)
        fig, ax = plt.subplots()
        country_counts.plot(kind="bar", color=["red"], ax=ax)
        plt.xlabel("Country")
        plt.ylabel("Frequency")
        plt.title("Frequency of Each Country")
        st.pyplot(fig)

        fig, ax = plt.subplots()
        country_counts['Frequency'].plot(kind='pie', autopct='%.2f%%', ax=ax, fontsize=7.5)
        plt.title("Pie Chart: Frequency of Each Country")
        st.pyplot(fig)
        st.write('**As we can see the USA had the most nuclear '
                'explosions from 1945- 1998 which is about 50 % we will go deeper about the US in our USA analysis column** ',fontsize = 35)



    elif selected_year == "ALL YEARS":
        country_year_counts = years_allmap.groupby(['Date.Year', 'WEAPON SOURCE COUNTRY']).size().unstack()
        fig, ax = plt.subplots()
        country_year_counts.plot(kind="line", ax=ax)
        plt.xlabel("Year")
        plt.ylabel("Frequency")
        plt.title("Frequency of Each Country Over Time")
        st.pyplot(fig)


    elif selected_year == 'LOCATION':

        icon_url = "https://upload.wikimedia.org/wikipedia/commons/e/ee/Map_marker_icon_%E2%80%93_Nicolas_Mollet_%E2%80%93_Fountain_%E2%80%93_Tourism_%E2%80%93_White.png"
        icon_data = {"url": icon_url, "width": 100, "height": 100, "anchorY": 100}
        results["icon_data"] = [icon_data] * len(results)
        view_state = pdk.ViewState(
            latitude=results["lat"].mean(),
            longitude=results["lon"].mean(),
            zoom=1,
            pitch=0
            )


        layer = pdk.Layer(
            type='ScatterplotLayer',
            data=results,
            get_position='[lon, lat]',
            get_radius=10000,
            get_fill_color=[100, 40, 200],
            get_icon='marker',
            pickable=True,
            radius_min_pixels=2,
            radius_max_pixels=500,
            hover_name=['WEAPON SOURCE COUNTRY','Date.Year']
        )

        map = pdk.Deck(
            map_provider='carto',
            map_style='light',
            initial_view_state=view_state,
            layers=[layer]
        )

        icon_layer = pdk.Layer(
            type='IconLayer',
            data=results,
            get_position='[lon, lat]',
            get_icon='icon_data',
            get_size=25,
            pickable=True,
            tooltip=['WEAPON SOURCE COUNTRY', 'Date.Year'],
        )
        map.layers.append(icon_layer)
        st.pydeck_chart(map)






#FILTER PAGE

elif which_one == "CUSTOM":

    st.sidebar.header('PLEASE FILTER HERE:')
    city_options = df_explo['WEAPON SOURCE COUNTRY'].unique()
    year_options = df_explo['Date.Year'].unique()

    city = st.sidebar.multiselect("Select Country:", options=city_options, default=city_options)
    year = st.sidebar.multiselect("Select Years:", options=year_options, default=year_options)
    df_selection = df_explo.query('`WEAPON SOURCE COUNTRY` == @city & `Date.Year` == @year')

    st.dataframe(df_selection)

    view_state = pdk.ViewState(
        latitude=df_selection["lat"].mean(),
        longitude=df_selection["lon"].mean(),
        zoom=1,
        pitch=0
    )

    layer = pdk.Layer(
        type='ScatterplotLayer',
        data=df_selection,
        get_position='[lon, lat]',
        get_radius=10000,
        get_fill_color=[100, 40, 200],
        get_icon='marker',

        pickable=True,
        radius_min_pixels=2,
        radius_max_pixels=500,
        tooltip=['WEAPON SOURCE COUNTRY', 'Date.Year'],
    )

    map = pdk.Deck(
        map_provider='carto',
        map_style='light',
        initial_view_state=view_state,
        layers=[layer]
    )

    st.pydeck_chart(map)





elif which_one == "US ANALYSIS":
    st.title('USA ANALYSIS')
    st.header('About USA data')
    img = Image.open('explosions.png')


    st.write('As stated previously between 1945 and 1998 USA had the most nuclear explosions,upon research we can see that between the years '
             '1960-1970 is where the most detonations happened since this was during time of the Cold War and Arms race when tensions between  '
             'USA and the USSR  as they competed against each other by conducting  tests to improve their weapons. The USSR came in second in most nuclear explosions ')

    st.image(img,width =300)
    df_usa = df_explo[df_explo['WEAPON SOURCE COUNTRY'] == 'USA']

    view_state = pdk.ViewState(
        latitude=df_usa["lat"].mean(),
        longitude=df_usa["lon"].mean(),
        zoom=1,
        pitch=0
    )
    layer = pdk.Layer(
        type='ScatterplotLayer',
        data=df_usa,
        get_position='[lon, lat]',
        get_radius=10000,
        get_fill_color=[100, 40, 200],
        get_icon='marker',
        pickable=True,
        radius_min_pixels=2,
        radius_max_pixels=500,
        tooltip=['WEAPON SOURCE COUNTRY', 'Date.Year'],
    )
    map = pdk.Deck(
        map_provider='carto',
        map_style='light',
        initial_view_state=view_state,
        layers=[layer]
    )

    st.pydeck_chart(map)

    call_us = st.selectbox('What data do you want anaylsis',
                       ('Data.Type', 'WEAPON DEPLOYMENT LOCATION'))

    if call_us == 'WEAPON DEPLOYMENT LOCATION':
        analyze_data = df_usa.groupby(call_us).size()
        st.subheader('**Results**')
        img = Image.open('latest7 (1).png')
        fig, ax = plt.subplots(figsize=(5, 3))
        analyze_data.plot(kind='bar', color=['red'], ax=ax)
        plt.title("Frequency of Each Location")
        st.pyplot(fig)

        st.write(
            'As we can see from our data the location NTS had the most drops, upon reasearch that the most drops happended in the state Neveda'
            'as shown in our map  upon futher while reasearching it was discovered that each plot was in and around in the same area and located which is a military bases conducting nuclear testing '
            'discovering that the neculear denotions happended in Tonopah Test Range also known as Area 51 ')
        st.image(img, width=350)






    elif call_us == 'Data.Type':
        analyze_data =  df_usa.groupby(call_us).size()
        st.write(analyze_data)














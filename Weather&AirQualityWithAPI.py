import streamlit as st
import requests

api_key = "47953df7-482a-4581-876a-2784312abb9a"

st.title("Weather and Air Quality Web App")
st.header("Streamlit and AirVisual API")

@st.cache_data
def map_creator(latitude, longitude):
    from streamlit_folium import folium_static
    import folium

    # This centers on the station
    m = folium.Map(location=[latitude, longitude], zoom_start=10)

    # This adds marker for the station
    folium.Marker([latitude, longitude], popup="Station", tooltip="Station").add_to(m)

    # This calls to render Folium map in Streamlit
    folium_static(m)

@st.cache_data
def generate_list_of_countries():
    countries_url = f"https://api.airvisual.com/v2/countries?key={api_key}"
    countries_dict = requests.get(countries_url).json()
    st.write(countries_dict)
    return countries_dict

@st.cache_data
def generate_list_of_states(country_selected):
    states_url = f"https://api.airvisual.com/v2/states?country={country_selected}&key={api_key}"
    states_dict = requests.get(states_url).json()
    st.write(states_dict)
    return states_dict

@st.cache_data
def generate_list_of_cities(state_selected, country_selected):
    cities_url = f"https://api.airvisual.com/v2/cities?state={state_selected}&country={country_selected}&key={api_key}"
    cities_dict = requests.get(cities_url).json()
    st.write(cities_dict)
    return cities_dict

category = st.selectbox(
    "Select Category",
    ("By City, State, and Country", "By Nearest City (IP Address)", "By Latitude and Longitude"))

st.write("You selected:", category)

if category == "By City, State, and Country":
    countries_dict = generate_list_of_countries()
    if countries_dict["status"] == "success":
        countries_list = []
        for i in countries_dict["data"]:
            countries_list.append(i["country"])
        countries_list.insert(0, "")

        country_selected = st.selectbox("Select a country", options=
        countries_list)
        if country_selected:

            states_dict = generate_list_of_states(country_selected)
            if states_dict["status"] == "success":
                states_list = []
                for i in states_dict["data"]:
                    states_list.append(i["state"])
                states_list.insert(0, "")

            state_selected = st.selectbox(
                "Select a State", options=
                states_list)

            if state_selected:

                cities_dict = generate_list_of_cities(state_selected, country_selected)
                if cities_dict["status"] == "success":
                    cities_list = []
                    for i in cities_dict["data"]:
                        cities_list.append(i["city"])
                    cities_list.insert(0, "")

                city_selected = st.selectbox(
                    "Select a City", options=
                    cities_list)

                if city_selected:
                    aqi_data_url = f"https://api.airvisual.com/v2/city?city={city_selected}&state={state_selected}&country={country_selected}&key={api_key}"
                    aqi_data_dict = requests.get(aqi_data_url).json()

                    if aqi_data_dict["status"] == "success":

                        st.markdown(f"Tempurature in the nearest city is {aqi_data_dict['data']['current']['weather']['tp']} Celcius")
                        st.markdown(f"Humidity, {aqi_data_dict['data']['current']['weather']['hu']}%")
                        st.markdown(f"The air quality index is currently {aqi_data_dict['data']['current']['pollution']['aqius']}")

                    else:
                        st.warning("No data available for this location.")
            else:
                st.warning("No stations available, please select another state.")
        else:
            st.warning("No stations available, please select another country.")
    else:
        st.error("Too many requests. Wait for a few minutes before your next API call.")

elif category == "By Nearest City (IP Address)":
    url = f"https://api.airvisual.com/v2/nearest_city?key={api_key}"
    aqi_data_dict = requests.get(url).json()

    if aqi_data_dict["status"] == "success":

        st.markdown(f"Tempurature in the nearest city is {aqi_data_dict['data']['current']['weather']['tp']} Celcius")
        st.markdown(f"Humidity, {aqi_data_dict['data']['current']['weather']['hu']}%")
        st.markdown(f"The air quality index is currently {aqi_data_dict['data']['current']['pollution']['aqius']}")

    else:
        st.warning("No data available for this location.")

elif category == "By Latitude and Longitude":

    latitude = st.text_input("Enter latitude, e.g. -21.240495341995576")

    longitude = st.text_input("Enter longitude, e.g. -44.99782911715176")

    if latitude and longitude:
        url = f"https://api.airvisual.com/v2/nearest_city?lat={latitude}&lon={longitude}&key={api_key}"
        aqi_data_dict = requests.get(url).json()

        if aqi_data_dict["status"] == "success":

            st.markdown(f"Tempurature in the nearest city is {aqi_data_dict['data']['current']['weather']['tp']} Celcius")
            st.markdown(f"Humidity, {aqi_data_dict['data']['current']['weather']['hu']}%")
            st.markdown(f"The air quality index is currently {aqi_data_dict['data']['current']['pollution']['aqius']}")

        else:
            st.warning("No data available for this location.")
import streamlit as st
import pandas as pd
import datetime as dt
import streamlit.components.v1 as components
import plotly.express as px

st.title("Air Quality Index in Central and South Jakarta (2016-2022)")

# Import the data

c_data = \
    pd.read_csv("jakarta-central (us consulate), indonesia-air-quality.csv", 
    header = 0, 
    names = ["Date", "PM25", "PM10"])
c_data["Loc"] = "Central Jakarta"

s_data = \
    pd.read_csv("jakarta-south (us consulate), indonesia-air-quality.csv", 
    header = 0, 
    names = ["Date", "PM25", "PM10"])
s_data["Loc"] = "South Jakarta"

# Combine the data for Central Jakarta and South Jakarta

data = pd.concat([c_data, s_data])

# Calculate the AQI as the maximum values between PM25 and PM10

data["AQI"] = data[["PM25", "PM10"]].max(axis = 1)

# Drop PM25 and PM10 columns

data.drop(["PM25", "PM10"], axis = 1, inplace = True)

# Convert date column to datetime format

data["Date"] = pd.to_datetime(data["Date"])

# Drop data below 2016 (the data is incomplete)

data["Year"] = data["Date"].dt.year
data["Month"] = data["Date"].dt.strftime("%Y-%m")
data.drop(index = data[data["Year"] < 2016].index, inplace = True)

# Group data (monthly)

data_monthly = \
    data.drop(columns = ["Date", "Year"]).\
    groupby(["Month", "Loc"]).\
    agg(["min", "mean", "max"]).\
    reset_index()
data_monthly.columns = \
    [" ".join(column) for column in data_monthly.columns.to_flat_index()]
data_monthly.columns = \
    [column.strip() for column in data_monthly.columns]

# Group date (yearly)

data_yearly = \
    data.drop(columns = ["Date", "Month"]).\
    groupby(["Year", "Loc"]).\
    agg(["min", "mean", "max"]).\
    reset_index()
data_yearly.columns = \
    [" ".join(column) for column in data_yearly.columns.to_flat_index()]
data_yearly.columns = \
    [column.strip() for column in data_yearly.columns]

# Streamlit parts

## Header

st.header("Introduction")

st.markdown("An air quality index (AQI) is used by government agencies to communicate to the public how polluted the air currently is or how polluted it is forecast to become. It is obtained by averaging readings from an air quality sensor, which can increase due to vehicle traffic, forest fires, or anything that can increase air pollution. Pollutants tested include ozone, nitrogen dioxide, sulphur dioxide, among others.")
st.markdown("Public health risks increase as the AQI rises, especially affecting children, the elderly, and individuals with respiratory or cardiovascular issues. During these times, governmental bodies generally encourage people to reduce physical activity outdoors, or even avoid going out altogether. The use of face masks such as cloth masks may also be recommended.")

aqi_ref = pd.DataFrame(columns = ["Health Concern", "AQI Value", "Remarks"])
aqi_ref.loc[len(aqi_ref.index)] = [
    "Good", 
    "0 to 50", 
    "Satisfactory, air pollution poses little or no risk"]
aqi_ref.loc[len(aqi_ref.index)] = [
    "Moderate", 
    "51 to 100", 
    "Acceptable; however, for some pollutants there may be a moderate health concern for a very small number of people who are unusually sensitive to air pollution."]
aqi_ref.loc[len(aqi_ref.index)] = [
    "Unhealthy for Sensitive Groups", 
    "101 to 150",
    "Members of sensitive groups may experience health effects. The general public is not likely to be affected."]
aqi_ref.loc[len(aqi_ref.index)] = [
    "Unhealthy", 
    "151 to 200", 
    "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects."]
aqi_ref.loc[len(aqi_ref.index)] = [
    "Very Unhealthy", 
    "201 to 300", 
    "Health warnings of emergency conditions. The entire population is more likely to be affected."]
aqi_ref.loc[len(aqi_ref.index)] = [ 
    "Hazardous", 
    "301 to 500", 
    "Health alert: everyone may experience more serious health effects."]
st.write(aqi_ref.style.hide_index().to_html(), unsafe_allow_html = True)

st.markdown("")
st.markdown("For this project, AQI data from  US Embassy Jakarta is used. The data was collected from the embassy's air quality meters located in Central and South Jakarta from January 2016 to October 2022.")

# Historical Data

st.header("Historical Data")

## Yearly Data

st.subheader("Yearly Data")

c1, c2 = st.columns(2)
with c1:
    st.markdown("**Central Jakarta**")
    components.iframe("https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d63465.833488223354!2d106.76461943256236!3d-6.182308177244731!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2e69f436b8c94b07%3A0x6ea6d5398b7c82f6!2sCentral%20Jakarta%2C%20Central%20Jakarta%20City%2C%20Jakarta!5e0!3m2!1sen!2sid!4v1665699018349!5m2!1sen!2sid")
    styler_yearly =\
        data_yearly[data_yearly["Loc"] == "Central Jakarta"][["Year", "AQI min", "AQI mean", "AQI max"]].\
        style.hide_index().format(precision = 2).bar(subset = ["AQI min", "AQI mean", "AQI max"], cmap = "Reds")
    st.write(styler_yearly.to_html(), unsafe_allow_html = True)
    
with c2:
    st.markdown("**South Jakarta**")
    components.iframe("https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d126907.03875481836!2d106.73186763750911!3d-6.2841018694149255!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x2e69f1ec2422b0b3%3A0x39a0d0fe47404d02!2sSouth%20Jakarta%2C%20South%20Jakarta%20City%2C%20Jakarta!5e0!3m2!1sen!2sid!4v1665699103708!5m2!1sen!2sid")
    styler_yearly = \
        data_yearly[data_yearly["Loc"] == "South Jakarta"][["Year", "AQI min", "AQI mean", "AQI max"]].\
        style.hide_index().format(precision = 2).bar(subset = ["AQI min", "AQI mean", "AQI max"], cmap = "Reds")
    st.write(styler_yearly.to_html(), unsafe_allow_html = True)

st.markdown("")
st.markdown("Looking at the yearly summary from the historical data, it is clearly visible that the average AQI value was the highest during 2016 in both Central and South Jakarta. There was a decrease starting in 2017. In 2020 to 2021, the values dropped even more during the COVID lockdown. However, we see an increase again in 2022 after the COVID lockdown was relaxed. The maximum value in 2022 is almost the same as it was before the COVID lockdown, with South Jakarta area seeing a very drastic increase")

st.markdown("The AQI value distributon for each year can be seen in the box plot below. The data points were mainly distributed between `Moderate` and `Unhealthy for Sensitive Groups`. There were also some outliers where the data points were categorized as `Unhealthy` and `Very Unhealthy`, most prominently in 2016, 2018, and 2022.")
st.markdown("")

fig_box = px.box(data, x = "Year", y = "AQI", color = "Loc")
fig_box.update_layout(plot_bgcolor="rgba(0,0,0,0)")
fig_box.update_layout(template = "plotly_dark")
fig_box.update_layout(legend = dict(orientation = "h", y = 1.1, xanchor = "center", yanchor = "middle", x = 0.5))
st.plotly_chart(fig_box)

## Monthly Data

st.markdown("")
st.subheader("Monthly Data")

st.markdown("")
st.markdown("Here we can see how the monthly AQI value changed over time in more detail.")
            
### Central Jakarta

st.markdown("**Central Jakarta**")

line_central = \
    px.line(data_monthly[data_monthly["Loc"] == "Central Jakarta"], 
    x = "Month", 
    y = ["AQI min", "AQI mean", "AQI max"])
line_central.update_layout(plot_bgcolor="rgba(0,0,0,0)")
line_central.update_layout(template = "plotly_dark")
line_central.update_layout(legend = dict(orientation = "h", y = -0.2, xanchor = "center", yanchor = "middle", x = 0.5))
line_central.update_layout(legend_title_text = None)
st.plotly_chart(line_central)

st.dataframe(data_monthly[data_monthly["Loc"] == "Central Jakarta"]\
    [["Month", "AQI mean", "AQI min", "AQI max"]].\
    transpose().\
    style.format(precision = 2))

### South Jakarta

st.markdown("**South Jakarta**")

line_south = \
    px.line(data_monthly[data_monthly["Loc"] == "South Jakarta"], 
    x = "Month", 
    y = ["AQI min", "AQI mean", "AQI max"])
line_south.update_layout(plot_bgcolor="rgba(0,0,0,0)")
line_south.update_layout(template = "plotly_dark")
line_south.update_layout(legend = dict(orientation = "h", y = -0.2, xanchor = "center", yanchor = "middle", x = 0.5))
line_south.update_layout(legend_title_text = None)
st.plotly_chart(line_south)

st.dataframe(data_monthly[data_monthly["Loc"] == "South Jakarta"]\
    [["Month", "AQI mean", "AQI min", "AQI max"]].\
    transpose().\
    style.format(precision = 2))

## Conclusion

st.header("Conclusion")

st.markdown("While the AQI level dropped a lot during the COVID lockdown period, we can see an upward trends in 2022. It is even more drastic in South Jakarta area during January 2022 where the AQI value reached the record high for the past 6 years.")
st.markdown("Left uncorrected withouth any action, we can expect to see the AQI values to rise beyond what we had in 2016.")

## Sources

st.markdown("\n" 
    "\n" 
    "\n" )

st.markdown("##### Sources:")
st.markdown( 
    "- [https://aqicn.org/](https://aqicn.org/) \n" 
    "- [https://id.usembassy.gov/embassy-consulates/airqualitymonitor/](https://id.usembassy.gov/embassy-consulates/airqualitymonitor/)")

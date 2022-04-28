# life-and-death
# PROJECT OVERVIEW

    The goal is to provide context to the death counts of covid in the US. Covid Deaths have been used to as a reason to change culture and pass new laws, these laws and restrictions have caused massive harm economicly, socially, and physically.

## Project Description

    All data is pulled from CDC Wonder database (https://wonder.cdc.gov/) from 2018 to current. The data is then cleaned and organized into a table. The table is then used to create a report that provides context to the death counts of covid in the US. The report is then used to create a visualization that shows the death counts of covid in the US. With more time, the visualization will be updated to include more information and will show future death predictions.

## Goals
1. Create a report that provides context to the death counts of covid in the US.
2. Create visualizations that shows the death counts of covid in the US.

---

## Acquire Data

    The data is all available in the CDC Wonder database(https://wonder.cdc.gov/). An API is available for data before 2018 but that is not useful for the project. Several queries were made to the database to get the data that is needed and these queries are saved in a .txt files and combined using pandas. CDC limits queries to 75,000 rows per query and significantly more data was needed.

    The acquisition is done in the wrangle.py module.

## Preparing the Data

The data is in a mostly usable format with some exceptions. The exceptions are:
1. notes are included in the table
2. redundant columns are included in the table
3. some columns are not in the table but are needed for the report
4. dates need to be reformatted
5. numerical columns need to be converted to int
6. general cleaning of column names (lowercase, remove spaces, etc.)

## No Outliers
    Outliers would be removed but there are none. 
    * However, Mar 2022 has some incomplete data and is removed

---

## Exploratory Data Analysis
    Here I will look at the data and see if there are any trends or patterns that could be used to predict future death counts. Stats testing is also done here.

## Summary

1. There is a major correlation between age and covid deaths. Age also increases all cause mortality as expected
2. Men die from COVID in higher numbers
3. Covid was a top cause of death for a short period
4. Covid deaths are going down but death causes like homicide and diabetes remain higher
5. There are a lot of areas to spend our time money and energy on to reduce overall death and furthermore to improve the quality and quantity of life for the majority of Americans long term.

## Modeling
With more time a forecasting will be done on all relevant causes of death.

# Conclusion
Covid kills, and that is absolutely horrible. But other things kill as well and have been for a long time and will continue to do so. Fortunately the covid deaths are concentrated in the ages closer to end of life.

# Future Work
CDC should provide better API for data after 2018 as the do for data prior. UCD (Underlying Cause of Death) is used in this notebook but from personal experience it can be deceiving. I would like to compare MCD (Multiple Cause of Death) and see what other causes arrise with covid cases.

# Data Source
* https://wonder.cdc.gov/

# Data Dictionary
|Variable                       | description 
|-------------------------------|-------------
|all_cause_deaths               | all cause deaths      
|covid_deaths                   | covid deaths        
|scaled_covid                   | covid deaths scaled to 0-1 (1 being max deaths recorded)
|scaled_all_cause               | all cause deaths scaled to 0-1 (1 being max deaths recorded)
|difference                     | difference between covid deaths and all cause deaths
|average_death_age              | average age of death (all cause deaths)
|average_covid_death_age        | average age of death (covid deaths)
|heart_related_deaths           | heart related deaths(Heart attack, CHF, etc.)
|scaled_heart_deaths            | heart related deaths scaled to 0-1 (1 being max recorded)
|homicide_deaths                | homicide deaths
|scaled_homicide_deaths         | homicide deaths scaled to 0-1 (1 being max recorded)
|suicide_deaths                 | suicide or self harm
|scaled_suicide_deaths          | suicide deaths scaled to 0-1
|diabetes_deaths                | deaths contributed to diabetes
|scaled_diabetes_deaths         | diabetes deaths scaled
|accident_deaths                | deaths to unintentional accidents
|scaled_accident_deaths         | accident deaths scaled
|male_covid_deaths              | male covid deaths
|male_scaled_covid              | scaled
|male_heart_related_deaths      | male version of above
|male_scaled_heart_deaths       | male version of above
|male_homicide_deaths           | male version of above
|male_scaled_homicide_deaths    | male version of above
|male_suicide_deaths            | male version of above
|male_scaled_suicide_deaths     | male version of above
|male_diabetes_deaths           | male version of above
|male_scaled_diabetes_deaths    | male version of above
|male_accident_deaths           | male version of above
|male_scaled_accident_deaths    | male version of above
|female_covid_deaths            | female version of above
|female_scaled_covid            | female version of above
|female_heart_related_deaths    | female version of above
|female_scaled_heart_deaths     | female version of above
|female_homicide_deaths         | female version of above
|female_scaled_homicide_deaths  | female version of above
|female_suicide_deaths          | female version of above
|female_scaled_suicide_deaths   | female version of above
|female_diabetes_deaths         | female version of above
|female_scaled_diabetes_deaths  | female version of above
|female_accident_deaths         | female version of above
|female_scaled_accident_deaths  | female version of above

### Steps to reproduce
1. get data from cdc or pull .txt files from repo
2. clone notebook, viz, and wrangle
3. Ensure all libraries are installed, sklearn, pandas, numpy, matplotlib, seaborn, and scikit-learn

## Plan
1. Get the data
2. clean and prepare the data, remove outliers, scale, feature engineer
3. explore the data. Look for features to use in modeling, make visuals
4. give recomedations to move forward

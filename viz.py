import pandas as pd
import matplotlib
from scipy.stats import pearsonr
from scipy import stats
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib import style

style.use("ggplot")
import os
import wrangle
import datetime as dt


def death_rates_by_age_group():
    """Visualize the death rates by age group"""
    # get df for viz
    df = wrangle.wrangle_data()
    # create a pivot table with month as row and age group as column
    pivot_covid_rate = df[df["cause"].str.contains("#COVID-19")].pivot_table(
        index="month", columns="age_group", values="crude_rate", aggfunc="sum"
    )
    # create a pivot table with month as row and age group as column
    pivot_all_cause_rate = df.pivot_table(
        index="month", columns="age_group", values="crude_rate", aggfunc="sum"
    )
    plt.figure(figsize=(10, 6))
    pivot_all_cause_rate.mean().plot(label="all cause")
    pivot_covid_rate.mean().plot(label="COVID-19")
    plt.legend()
    plt.title("Death rates by Age Group")
    plt.show()


def deaths_by_age_group():
    """Visualize the deaths by age group"""
    df = wrangle.wrangle_data()
    # create a pivot table with month as row and age group as column
    pivot_all_cause_deaths = df.pivot_table(
        index="month", columns="age_group", values="deaths", aggfunc="sum"
    )
    # # create a pivot table with month as row and age group as column
    pivot_covid_deaths = df[df["cause"].str.contains("#COVID-19")].pivot_table(
        index="month", columns="age_group", values="deaths", aggfunc="sum"
    )
    plt.figure(figsize=(10, 6))
    pivot_all_cause_deaths.sum().plot(label="all cause")
    pivot_covid_deaths.sum().plot(label="COVID-19")
    plt.legend()
    plt.title("Deaths by Age Group")


def deaths_by_age_group_over_time():
    """visulize the deaths by age over time"""
    df = wrangle.wrangle_data()
    # create a pivot table with month as row and age group as column
    pivot_covid_rate = df[df["cause"].str.contains("#COVID-19")].pivot_table(
        index="month", columns="age_group", values="crude_rate", aggfunc="sum"
    )
    pivot_covid_rate.plot(figsize=(10, 6))
    # move legend to the top right
    plt.legend(loc="upper right")
    plt.title("Deaths by Age Group over time")
    plt.show()


def top_five_causes_over_time():
    """visualize the top five causes of death over time"""
    df = wrangle.wrangle_data()
    # top five causes of death
    top_five_causes = (
        df.groupby("cause").sum().sort_values(by="deaths", ascending=False).head(5)
    )
    sns.barplot(x=top_five_causes.index, y=top_five_causes["deaths"])
    # rotate x labels
    plt.xticks(rotation=90)
    plt.title("Top Five Causes of Death over time")


def top_ten_causes_over_time():
    """visualize the top ten causes of death over time"""
    df = wrangle.wrangle_data()
    # top ten causes of death
    top_ten_causes = (
        df.groupby("cause").sum().sort_values(by="deaths", ascending=False).head(10)
    )
    top_ten_causes["new_crude_rate"] = top_ten_causes.deaths / top_ten_causes.population
    top_ten_causes.plot(y="new_crude_rate", kind="bar", figsize=(10, 6))


def covid_vs_time():
    """visualize the covid deaths vs time"""
    df = wrangle.wrangle_data()
    pivot_covid_deaths = df[df["cause"].str.contains("#COVID-19")].pivot_table(
        index="month", columns="age_group", values="deaths", aggfunc="sum"
    )
    # add total deaths to pivot table
    pivot_covid_deaths["total_deaths"] = pivot_covid_deaths.sum(axis=1)
    # add 65+ age group to pivot table
    pivot_covid_deaths["65+"] = (
        pivot_covid_deaths["75-84"]
        + pivot_covid_deaths["65-74"]
        + pivot_covid_deaths["85+"]
    )
    # add 65+ age group to pivot table
    pivot_covid_deaths["75+"] = pivot_covid_deaths["75-84"] + pivot_covid_deaths["85+"]
    # plot the pivot table
    pivot_covid_deaths.plot(figsize=(10, 6))
    # move legend to the top right
    plt.legend(loc="upper right")
    plt.title("COVID-19 Deaths over time")
    plt.show()


def deaths_by_age_group_with_avg():
    """visualize the deaths by age group with average age"""
    covid_all_ages = wrangle.prep_covid()
    # groupby age and graph age vs death rate
    covid_all_ages.groupby("age").sum()["deaths"].plot(figsize=(10, 6))
    # spike at 100 is due to 100+ age group is compressed into 1 data point
    total_deaths = covid_all_ages.groupby("age").sum()["deaths"].sum()
    avg_deaths_by_age = total_deaths / 100
    # add line to graph
    plt.axhline(
        y=avg_deaths_by_age,
        color="grey",
        linestyle="--",
        label="Average deaths per age",
    )
    plt.legend()
    plt.title("Deaths by Age Group til Mar 2022")
    plt.show()


def covid_deaths_vs_gender():
    """visualize the covid deaths by gender"""
    covid_all_ages = wrangle.prep_covid()
    # plot the covid deaths vs gender
    covid_all_ages.groupby("gender").sum()["deaths"].plot(
        figsize=(10, 6), kind="bar", title="Covid Deaths by Gender"
    )
    plt.show()


def covid_deaths_by_age_and_gender():
    """visualize the deaths by age and gender"""
    covid_all_ages = wrangle.prep_covid()
    plt.figure(figsize=(10, 6))
    ax = sns.lineplot(data=covid_all_ages, x="age", y="deaths", hue="gender")
    plt.title("Covid Deaths by Age and Gender")
    # set xticklabels
    ax.set_xticks([0, 20, 40, 60, 80, 99.5])
    ax.set_xticklabels(["0", "20", "40", "60", "80", "100+"])
    plt.show()


def monthly_avg_age_covid():
    """visualize the monthly average age of covid deaths"""
    monthly_deaths = wrangle.get_monthly_deaths()
    monthly_deaths[["scaled_covid", "average_covid_death_age"]].plot(
        figsize=(10, 6),
        ylim=(0, 100),
        title="Monthly Average Age of Death from COVID-19",
    )
    plt.show()


def monthly_avg_age_all_cause():
    """visualize the monthly average age of all cause deaths"""
    monthly_deaths = wrangle.get_monthly_deaths()
    monthly_deaths[["all_cause_deaths", "covid_deaths"]].plot(
        figsize=(10, 6), title="Monthly Average Age of Death since covid"
    )
    plt.show()


def monthly_avg_age_all_cause():
    """visualize the monthly average age of all cause deaths"""
    df = wrangle.wrangle_data()
    df.groupby("month").sum()["deaths"].plot(
        figsize=(10, 6),
        title="Monthly Average Age of Death from All Causes 2018-Feb 2022",
    )
    plt.show()


def monthly_scaled_deaths_cause_and_covid():
    """visualize the monthly scaled deaths cause and covid"""
    (
        df2,
        male_scaled_cols,
        male_deaths_cols,
        female_scaled_cols,
        female_deaths_cols,
    ) = wrangle.make_df2()
    df2[["scaled_covid", "scaled_all_cause"]].plot(
        figsize=(10, 6), title="Monthly Scaled Deaths from COVID-19 vs All Causes"
    )
    plt.show()


def monthly_avg_age_all_cause_and_covid():
    """visualize the monthly average age of all cause deaths and covid"""
    (
        df2,
        male_scaled_cols,
        male_deaths_cols,
        female_scaled_cols,
        female_deaths_cols,
    ) = wrangle.make_df2()
    df2[["average_death_age", "average_covid_death_age"]].plot(
        figsize=(10, 6),
        ylim=(60, 80),
        title="Monthly Average Age of Death from COVID-19 vs All Causes",
    )
    plt.show()


def monthly_deaths_all_cause_and_covid():
    """visualize the monthly deaths of all cause and covid"""
    (
        df2,
        male_scaled_cols,
        male_deaths_cols,
        female_scaled_cols,
        female_deaths_cols,
    ) = wrangle.make_df2()
    deaths_cols = [
        col for col in df2.columns if ("deaths" in col) and ("scaled" not in col)
    ]
    df2[deaths_cols].plot(
        figsize=(10, 6), title="Monthly Deaths from COVID-19 vs other Causes"
    )
    plt.show()


def monthly_scaled_deaths_all_cause_and_covid():
    """visualize the monthly scaled deaths of all cause and covid"""
    (
        df2,
        male_scaled_cols,
        male_deaths_cols,
        female_scaled_cols,
        female_deaths_cols,
    ) = wrangle.make_df2()
    df2[["scaled_homicide_deaths", "scaled_diabetes_deaths", "scaled_accident_deaths"]][
        df2.index < "2021/10"
    ].plot(figsize=(10, 6), title="Monthly scaled Deaths from COVID-19 vs other Causes")
    # add vertical line to show 2020/03
    plt.axvline(
        x="2020/03", color="grey", linestyle="--", label="covid-19 declared pandemic"
    )
    plt.legend()
    plt.show()


def gendered_deaths():
    """visualize the gendered deaths"""
    (
        df2,
        male_scaled_cols,
        male_deaths_cols,
        female_scaled_cols,
        female_deaths_cols,
    ) = wrangle.make_df2()
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    df2[male_deaths_cols].plot(
        figsize=(18, 6),
        ax=ax1,
        title="Male Monthly Deaths from COVID-19 vs other Causes",
    )
    df2[female_deaths_cols].plot(
        ax=ax2, title="Female Monthly Deaths from COVID-19 vs other Causes"
    )
    plt.show()


def scaled_gendered_deaths():
    """visualize scaled gendered deaths"""
    (
        df2,
        male_scaled_cols,
        male_deaths_cols,
        female_scaled_cols,
        female_deaths_cols,
    ) = wrangle.make_df2()
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    df2[male_scaled_cols].plot(
        figsize=(18, 6),
        ax=ax1,
        title="Male Monthly Deaths from COVID-19 vs other Causes",
    )
    ax1.legend(loc="lower left")
    df2[female_scaled_cols].plot(
        ax=ax2, title="Female Monthly Deaths from COVID-19 vs other Causes"
    )
    ax2.legend(loc="lower left")
    plt.show()


def select_gendered_deaths():
    """visual subset of gendered deaths"""
    f, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    (
        df2,
        male_scaled_cols,
        male_deaths_cols,
        female_scaled_cols,
        female_deaths_cols,
    ) = wrangle.make_df2()
    df2[
        [
            "male_scaled_homicide_deaths",
            "male_scaled_diabetes_deaths",
            "male_scaled_accident_deaths",
        ]
    ][df2.index < "2021/10"].plot(
        ax=ax1,
        figsize=(18, 6),
        title="Monthly scaled Deaths from COVID-19 vs other Causes",
    )
    ax1.axvline(
        x="2020/03", color="grey", linestyle="--", label="covid-19 declared pandemic"
    )
    ax1.legend()
    df2[
        [
            "female_scaled_homicide_deaths",
            "female_scaled_diabetes_deaths",
            "female_scaled_accident_deaths",
        ]
    ][df2.index < "2021/10"].plot(
        ax=ax2,
        figsize=(18, 6),
        title="Monthly scaled Deaths from COVID-19 vs other Causes",
    )
    ax2.axvline(
        x="2020/03", color="grey", linestyle="--", label="covid-19 declared pandemic"
    )
    ax2.legend()
    plt.show()

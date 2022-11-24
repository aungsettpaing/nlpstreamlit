import streamlit as st
import altair as alt
import pandas as pd 
import numpy as np
import os 
import matplotlib.pyplot as plt
import math


PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.dirname(PROJECT_ROOT)

# title
st.title("Arsenal Under Mikel Arteta (EPL)")

# get data
def get_data():
        # fetch data
        data = pd.read_csv("https://raw.githubusercontent.com/aungsettpaing/EPL-Data/master/arsenal_under_mikel.csv")
        return data
arsenal_dataset = get_data()

# CURRENT FORM
st.subheader("Current Form")
colors = {"W": "green", "D": "grey", "L": "red"}
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
        result = arsenal_dataset.iloc[-1]["FinalResult"][0]
        st.markdown("### <font color='"+colors[result]+"'>" + result + "</font>", unsafe_allow_html=True)
        team = arsenal_dataset.iloc[-1]["AwayTeam"] if arsenal_dataset.iloc[-1]["HomeTeam"]=="Arsenal" else arsenal_dataset.iloc[-1]["HomeTeam"]
        goal = str(arsenal_dataset.iloc[-1]["FTHG"]) + " - " + str(arsenal_dataset.iloc[-1]["FTAG"])
        st.markdown("_" + team + " " + goal + "_")
with col2:
        result = arsenal_dataset.iloc[-2]["FinalResult"][0]
        st.markdown("### <font color='"+colors[result]+"'>" + result + "</font>", unsafe_allow_html=True)
        team = arsenal_dataset.iloc[-2]["AwayTeam"] if arsenal_dataset.iloc[-2]["HomeTeam"]=="Arsenal" else arsenal_dataset.iloc[-2]["HomeTeam"]
        goal = str(arsenal_dataset.iloc[-2]["FTHG"]) + " - " + str(arsenal_dataset.iloc[-2]["FTAG"])
        st.markdown("_" + team + " " + goal + "_")
with col3:
        result = arsenal_dataset.iloc[-3]["FinalResult"][0]
        st.markdown("### <font color='"+colors[result]+"'>" + result + "</font>", unsafe_allow_html=True)
        team = arsenal_dataset.iloc[-3]["AwayTeam"] if arsenal_dataset.iloc[-3]["HomeTeam"]=="Arsenal" else arsenal_dataset.iloc[-3]["HomeTeam"]
        goal = str(arsenal_dataset.iloc[-3]["FTHG"]) + " - " + str(arsenal_dataset.iloc[-3]["FTAG"])
        st.markdown("_" + team + " " + goal + "_")
with col4:
        result = arsenal_dataset.iloc[-4]["FinalResult"][0]
        st.markdown("### <font color='"+colors[result]+"'>" + result + "</font>", unsafe_allow_html=True)
        team = arsenal_dataset.iloc[-4]["AwayTeam"] if arsenal_dataset.iloc[-4]["HomeTeam"]=="Arsenal" else arsenal_dataset.iloc[-4]["HomeTeam"]
        goal = str(arsenal_dataset.iloc[-4]["FTHG"]) + " - " + str(arsenal_dataset.iloc[-4]["FTAG"])
        st.markdown("_" + team + " " + goal + "_")
with col5:
        result = arsenal_dataset.iloc[-5]["FinalResult"][0]
        st.markdown("### <font color='"+colors[result]+"'>" + result + "</font>", unsafe_allow_html=True)
        team = arsenal_dataset.iloc[-5]["AwayTeam"] if arsenal_dataset.iloc[-5]["HomeTeam"]=="Arsenal" else arsenal_dataset.iloc[-5]["HomeTeam"]
        goal = str(arsenal_dataset.iloc[-5]["FTHG"]) + " - " + str(arsenal_dataset.iloc[-5]["FTAG"])
        st.markdown("_" + team + " " + goal + "_")
st.write("***")

# FILTER
seasons = ["All Seasons"] + list(pd.unique(arsenal_dataset["season"]))
selected_season = st.selectbox("Filter", seasons)

# create a placeholder container
container = st.empty()

with container.container():
        # CURRENT SEASON
        if selected_season and selected_season != "All Seasons":
                # to get win, draw, lose count
                win_draw_lose = arsenal_dataset[arsenal_dataset["season"]==selected_season]["FinalResult"].value_counts()
                win_draw_lose_df = pd.DataFrame(win_draw_lose).rename(columns={"FinalResult": "Total"})
                # to get GA and GF count
                goal_for_against = arsenal_dataset[arsenal_dataset["season"]==selected_season][["FTGT", "FTGC"]].sum()
                goal_for_against_df = pd.DataFrame(goal_for_against).rename(columns={0: "Total"}, index={"FTGT":"Goal For", "FTGC": "Goal Against"})
        else:
                # to get win, draw, lose count
                win_draw_lose = arsenal_dataset["FinalResult"].value_counts()
                win_draw_lose_df = pd.DataFrame(win_draw_lose).rename(columns={"FinalResult": "Total"})
                # to get GA and GF count
                goal_for_against = arsenal_dataset[["FTGT", "FTGC"]].sum()
                goal_for_against_df = pd.DataFrame(goal_for_against).rename(columns={0: "Total"}, index={"FTGT":"Goal For", "FTGC": "Goal Against"})



        col1, col2, col3, col4 = st.columns(4)
        with col1:
                # to compute win percentage
                win_percentage = round(win_draw_lose["Win"] / win_draw_lose.sum() * 100, 2)
                st.markdown("## " + str(win_percentage) + "%")
                st.write("Win Percentage")

        with col2:
                points_per_game = round(((3*win_draw_lose["Win"]) + win_draw_lose["Draw"]) / win_draw_lose.sum(), 2)
                st.markdown("## " + str(points_per_game))
                st.write("Points / Game")

        with col3:
                goal_for = round(goal_for_against["FTGT"].sum() / win_draw_lose.sum(), 2)
                st.markdown("## <font color='green'> " + str(goal_for) + "</font>", unsafe_allow_html=True)
                st.write("Goal For / Game")

        with col4:
                goal_against = round(goal_for_against["FTGC"].sum() / win_draw_lose.sum(), 2)
                st.markdown("## <font color='red'> " + str(goal_against) + "</font>", unsafe_allow_html=True)
                st.write("Goal Against / Game")
        st.write("***")

        # Total games, win, draw and loss
        st.subheader("Winning Stats 💪")
        total_games, total_wins = st.columns(2)
        
        with total_games:
                # final data
                win_draw_lose_goal_for_against = pd.concat([win_draw_lose_df, goal_for_against_df])
                st.dataframe(
                        win_draw_lose_goal_for_against,
                        use_container_width=True
                )

        with total_wins:
                # Pie chart, where the slices will be ordered and plotted counter-clockwise:
                labels = 'Win', 'Draw', 'Lose'
                sizes = [win_draw_lose["Win"], win_draw_lose["Draw"], win_draw_lose["Lose"]]
                explode = (0.1, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')

                fig1, ax1 = plt.subplots()
                ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                        colors=["green", "grey", "red"],
                        startangle=90)
                ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                ax1.legend()
                st.pyplot(fig1)

        # HOME OR AWAY
        st.subheader("Home/Away Performance 🏟️")
        home_ground = arsenal_dataset[arsenal_dataset["Home"]=="Yes"].pivot_table(
                index=["season"],
                values=["FTGT", "FTGC", "Point"],
                aggfunc=["mean"]
        )
        home_ground.columns = ["Average GA", "Average GF", "Average Pts"]

        away_from_home = arsenal_dataset[arsenal_dataset["Home"]=="No"].pivot_table(
                index=["season"],
                values=["FTGT", "FTGC", "Point"],
                aggfunc=["mean"]
        )
        away_from_home.columns = ["Average GA", "Average GF", "Average Pts"]

        col1, col2 = st.columns(2, gap="large")
        with col1:
                st.markdown("##### Home Ground")
                st.line_chart(home_ground)
        
        with col2:
                st.markdown("##### Away From Home")
                st.line_chart(away_from_home)


        # WITH BIG Six
        st.subheader("Big Six Performance 😎")
        big_6_teams = ["Man City", "Liverpool", "Chelsea", "Man United", "Tottenham"]
        big_6_data = arsenal_dataset[(arsenal_dataset["HomeTeam"].isin(big_6_teams)) | (arsenal_dataset["AwayTeam"].isin(big_6_teams))]
        big_6_summary = big_6_data.pivot_table(
                index=["season"],
                values=["Point", "FTGT", "FTGC"],
                aggfunc=["mean"]
        )
        big_6_summary.columns = ["Average GA", "Average GF", "Average Pts"]
        st.line_chart(big_6_summary)

        col1, col2 = st.columns(2, gap="large")
        with col1:
                home_big_6_summary = big_6_data[big_6_data["Home"]=="Yes"].pivot_table(
                        index=["season"],
                        values=["Point", "FTGT", "FTGC"],
                        aggfunc=["mean"]
                )
                home_big_6_summary.columns = ["Average GA", "Average GF", "Average Pts"]
                st.markdown("##### Home Ground Focused")
                st.bar_chart(home_big_6_summary)
        
        with col2:
                away_big_6_summary = big_6_data[big_6_data["Home"]=="No"].pivot_table(
                        index=["season"],
                        values=["Point", "FTGT", "FTGC"],
                        aggfunc=["mean"]
                )
                away_big_6_summary.columns = ["Average GA", "Average GF", "Average Pts"]
                st.markdown("##### Away From Home Focused")
                st.bar_chart(away_big_6_summary)

        big_5_table = big_6_data.copy()
        big_5_table["GoalScore"] = big_5_table["FTHG"].astype("str") + " : " + big_5_table["FTAG"].astype("str")
        big_5_table = big_5_table.sort_values(by="Date", ascending=False).reset_index()[:10]
        def resultHightlight(val):
                if val == "Win":
                        color = 'rgba(0, 255, 0, 0.3)'
                elif val == "Draw":
                        color = 'rgba(211, 211, 211, 0.3)'
                elif val == "Lose":
                        color = 'rgba(255, 0, 0, 0.3)'
                else:
                        color = ''
                return 'background-color: ' + color

        st.markdown("##### Last 10 H2H")
        st.dataframe(
                big_5_table[["Date", "season", "HomeTeam", "GoalScore", "AwayTeam", "FinalResult", "Referee"]].style.applymap(resultHightlight),
                use_container_width=True
        )
        # REFEREES
        st.subheader("Referees 👀")
        if selected_season and selected_season != "All Seasons":
                referees = arsenal_dataset[arsenal_dataset["season"]==selected_season].pivot_table(
                        index="Referee",
                        values="Point",
                        aggfunc=["count", "sum", "mean"]
                )
        else:
                referees = arsenal_dataset.pivot_table(
                        index="Referee",
                        values="Point",
                        aggfunc=["count", "sum", "mean"]
                )
        referees.columns = ["# In Charge", "Total Pts", "Average Pts"]

        col1, col2 = st.columns(2, gap="large")
        game_threshold = int(win_draw_lose.sum() / 20) # 5% of total games
        referees_charged_5_percent_games = referees[referees["# In Charge"] >= game_threshold].sort_values(by="Average Pts", ascending=False)[:]
        with col1:
                st.markdown("##### Love you, Refs 🥰")
                # most_referees = referees[referees["# In Charge"] >= game_threshold].sort_values(by="Average Pts", ascending=False)[:]
                st.dataframe(
                        (referees_charged_5_percent_games[referees_charged_5_percent_games["Average Pts"]>=1.5].style
                                        .highlight_between(["Average Pts"], 
                                                                left=2, 
                                                                right=3, 
                                                                axis=1, 
                                                                props='background-color:rgba(0, 255, 0, 0.3);')),
                        use_container_width=True
                )
        
        with col2:
                st.markdown("##### Sorry! Next! 🤢")
                # least_referees = referees.sort_values(by="Average Pts", ascending=True)[:6]
                st.dataframe(
                        (referees_charged_5_percent_games[referees_charged_5_percent_games["Average Pts"]<1.5].style
                                .highlight_between(["Average Pts"], 
                                                left=0, 
                                                right=1.99, 
                                                axis=1, 
                                                props='background-color:rgba(255, 0, 0, 0.3);')),
                        use_container_width=True
                )

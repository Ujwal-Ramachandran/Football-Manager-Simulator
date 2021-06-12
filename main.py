from flask import Flask, render_template, request
import pandas as pd
import numpy as np

app = Flask(__name__)

df = pd.read_csv("fifa_processed.csv")

# Rank the players
def rank_players(pos, country, age, sortby, nop):
    df_smaller = df    
    if pos != "Any":
        df_smaller = df_smaller.loc[df["Pos_simp"] == pos]
    if country != "Any":
        df_smaller = df_smaller.loc[df["Nationality"] == country]
    if age != "Any":
        if age == "Below 18":
            df_smaller = df_smaller.loc[df["Age"] < 18]
        if age == "18-21":
            df_smaller = df_smaller.loc[(df["Age"] >= 18) & (df["Age"] < 22)]
        if age == "22-26":
            df_smaller = df_smaller.loc[(df["Age"] >= 22) & (df["Age"] < 27)]
        if age == "27-31":
            df_smaller = df_smaller.loc[(df["Age"] >= 27) & (df["Age"] < 32)]
        if age == "Above 31":
            df_smaller = df_smaller.loc[(df["Age"] > 31)]
    
    df_smaller = df_smaller.sort_values(by = [sortby], ascending = False).head(nop)
    df_smaller = df_smaller[["Name", "Pos_simp", "Age", "Nationality", sortby]]
    return df_smaller


# Find the best team
def man_mode(formation, age, country):
    df_smaller = df    
    if country != "Any":
        df_smaller = df_smaller.loc[df["Nationality"] == country]

    if age != "Any":
        if age == "Below 18":
            df_smaller = df_smaller.loc[df["Age"] < 18]
        if age == "18-21":
            df_smaller = df_smaller.loc[(df["Age"] >= 18) & (df["Age"] < 22)]
        if age == "22-26":
            df_smaller = df_smaller.loc[(df["Age"] >= 22) & (df["Age"] < 27)]
        if age == "27-31":
            df_smaller = df_smaller.loc[(df["Age"] >= 27) & (df["Age"] < 32)]
        if age == "Above 31":
            df_smaller = df_smaller.loc[(df["Age"] > 31)]
    l = 0   
    df_gk = df_smaller.loc[df_smaller["Pos_simp"] == "GK"]
    gk_list = df_gk.head(1)["Name"].tolist()
    l += len(gk_list)

    df_def = df_smaller.loc[df_smaller["Pos_simp"] == "DEF"]
    n_def = int(formation.split("-")[0])
    def_list = df_def.head(n_def)["Name"].tolist()
    l += len(def_list)
    
    df_mid = df_smaller.loc[df_smaller["Pos_simp"] == "MID"]
    n_mid = int(formation.split("-")[1])
    mid_list = df_mid.head(n_mid)["Name"].tolist()
    l += len(mid_list)
    
    df_st = df_smaller.loc[df_smaller["Pos_simp"] == "ATT"]
    n_st = int(formation.split("-")[2])
    st_list = df_st.head(n_st)["Name"].tolist()
    l += len(st_list)
    
    team_list = [st_list] + [mid_list] + [def_list]  + [gk_list]
    team_list.append(l)
    return team_list


# Home
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/home")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("aboutUs.html")


# Manager Mode
@app.route("/manager")
def manager():
    return render_template("manMode.html")

@app.route("/mop", methods = ["POST","GET"]) 
def disp_team():
    if request.method == "GET" :
        return render_template("manMode.html")
    if request.method == "POST" :
        team_f = request.form.get("formation")
        team_a = request.form.get("age")
        team_n = request.form.get("country").title()
        if team_n == "" :
            team_n = "Any"
        team = man_mode(team_f,team_a,team_n)
        return render_template("manager.html", team = team)


# Ranking Mode
@app.route("/rank")
def rank():
    return render_template("rankMode.html")

@app.route("/rop", methods = ["POST","GET"])
def disp_rank():
    if request.method == "GET" :
        return render_template("rankMode.html")
    if request.method == "POST":
        rd_p = request.form.get("pos")
        rd_a = request.form.get("age")
        rd_c = request.form.get("country").title()
        if rd_c == "" :
            rd_c = "Any"
        rd_s = request.form.get("sortby")
        nop = request.form.get("nop")
        if nop == "" :
            nop = 10
        else : 
            nop = int(nop)
        rd = rank_players(rd_p, rd_c, rd_a, rd_s, nop)
        rd_name = rd["Name"].astype(str).values.tolist()
        rd_pf = rd["Pos_simp"].astype(str).values.tolist()
        rd_cf = rd["Nationality"].astype(str).values.tolist()
        rd_af = rd["Age"].astype(str).values.tolist()
        if rd_s == "Stamina" :
            rd_sf = rd["Stamina"].astype(str).values.tolist()
        elif rd_s == "Acceleration" :
            rd_sf = rd["Acceleration"].astype(str).values.tolist()
        elif rd_s == "Finishing" :
            rd_sf = rd["Finishing"].astype(str).values.tolist()
        elif rd_s == "Strength" :
            rd_sf = rd["Strength"].astype(str).values.tolist()
        elif rd_s == "Vision" :
            rd_sf = rd["Vision"].astype(str).values.tolist()
        elif rd_s == "Positioning" :
            rd_sf = rd["Positioning"].astype(str).values.tolist()
        elif rd_s == "GKReflexes" :
            rd_sf = rd["GKReflexes"].astype(str).values.tolist()
        elif rd_s == "Dribbling" :
            rd_sf = rd["Dribbling"].astype(str).values.tolist()
        elif rd_s == "Height_cm" :
            rd_sf = rd["Height_cm"].astype(str).values.tolist()
        elif rd_s == "Weight" :
            rd_sf = rd["Weight"].astype(str).values.tolist()
        else :
            rd_sf = rd["Overall"].astype(str).values.tolist()
    
        rank_data = [rd_name, rd_pf, rd_af, rd_cf, rd_sf, len(rd_name),rd_s]
        return render_template("rank.html", rank_data = rank_data)



if __name__ == "__main__" :
    app.run()


# Rank
# -> Position - Dropdown
# -> Age - Dropdown
# -> Nationality - Text 
# -> SortBy

# Manager
# -> Formation
# -> Age
# -> Nationality

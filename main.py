from flask import Flask, render_template, request
import pandas as pd
import numpy as np

app = Flask(__name__)

df = pd.read_csv("fifa_processed.csv")

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
            
    df_gk = df_smaller.loc[df_smaller["Pos_simp"] == "GK"]
    gk_list = df_gk.head(1)["Name"].tolist()
    
    df_def = df_smaller.loc[df_smaller["Pos_simp"] == "DEF"]
    n_def = int(formation.split("-")[0])
    def_list = df_def.head(n_def)["Name"].tolist()
    
    df_mid = df_smaller.loc[df_smaller["Pos_simp"] == "MID"]
    n_mid = int(formation.split("-")[1])
    mid_list = df_mid.head(n_mid)["Name"].tolist()
    
    df_st = df_smaller.loc[df_smaller["Pos_simp"] == "ATT"]
    n_st = int(formation.split("-")[2])
    st_list = df_st.head(n_st)["Name"].tolist()
    
    team_list = gk_list + def_list + mid_list + st_list
    return team_list

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/manager")
def man():
    return render_template('manMode.html')

@app.route("/rank")
def rank():
    return render_template('rankMode.html')

@app.route("/rop", methods = ['POST','GET'])
def disp_rank():
    if request.method == 'GET' :
        return render_template('rankMode.html')
    if request.method == 'POST':
        rd_p = request.form.get("pos")
        rd_a = request.form.get("age")
        rd_c = request.form.get("country")
        rd_s = request.form.get("sortby")
        nop = int(request.form.get("nop"))
        rd = rank_players(rd_p, rd_c, rd_a, rd_s, nop)
        rd_name = rd["Name"].astype(str).values.tolist()
        rd_pf = rd["Pos_simp"].astype(str).values.tolist()
        rd_cf = rd["Nationality"].astype(str).values.tolist()
        rd_af = rd["Age"].astype(str).values.tolist()
        if rd_s == "Height in cm" :
            rd_sf = rd["Height_cm"].astype(str).values.tolist()
        elif rd_s == "Acceleration" :
            rd_sf = rd["Acceleration"].astype(str).values.tolist()
        else :
            rd_sf = rd["Overall"].astype(str).values.tolist()
        rank_data = [rd_name, rd_pf, rd_af, rd_cf, rd_sf, len(rd_name),rd_s]
        return render_template('rank.html', rank_data = rank_data)

#ImmutableMultiDict([('pos', 'GK'), ('age', '18-22'), ('country', 'India'), ('sortby', 'Overall')])    

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
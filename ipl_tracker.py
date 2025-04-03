import streamlit as st
import requests

# --- CONFIG ---
USE_MOCK_DATA = True  # Change to False to use the live API

# --- CLASS DEFINITIONS ---
class Team:
    def __init__(self, name, points, placement):
        self.name = name
        self.points = points
        self.placement = placement

    def __repr__(self):
        return f"{self.name} - {self.points} pts, Place: {self.placement}"

class TeamManager:
    def __init__(self, name, team_names):
        self.name = name
        self.team_names = team_names
        self.teams = []

    def assign_teams(self, all_teams):
        self.teams = [team for team in all_teams if team.name in self.team_names]

    def average_points(self):
        return sum(t.points for t in self.teams) / len(self.teams)

    def average_placement(self):
        return sum(t.placement for t in self.teams) / len(self.teams)

# --- API DATA FETCH ---
@st.cache_data(ttl=900)
def fetch_ipl_table():
    url = "https://cricbuzz-cricket.p.rapidapi.com/mcenter/v1/41881/comm "
    headers = {
        "X-RapidAPI-Key": st.secrets[x_rapidapi_key],
        "X-RapidAPI-Host": "x-rapidapi-host: cricbuzz-cricket.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return [
            {
                "team": t["team"],
                "points": t["points"],
                "placement": t["position"]
            }
            for t in data["points_table"]
        ]
    else:
        st.error(f"API error: {response.status_code}")
        return []

# --- DATA SOURCING ---
if USE_MOCK_DATA:
    raw_data = [
        {'team': 'CSK', 'points': 12, 'placement': 4},
        {'team': 'RCB',  'points': 10, 'placement': 6},
        {'team': 'GT',   'points': 6,  'placement': 8},
        {'team': 'RR',   'points': 14, 'placement': 2},
        {'team': 'LSG',  'points': 8,  'placement': 7},
        {'team': 'MI',   'points': 10, 'placement': 5},
        {'team': 'KKR',  'points': 16, 'placement': 1},
        {'team': 'SRH',  'points': 12, 'placement': 3},
        {'team': 'DC',   'points': 6,  'placement': 9},
        {'team': 'PBKS', 'points': 4,  'placement': 10}
    ]
else:
    raw_data = fetch_ipl_table()

# --- CREATE TEAM OBJECTS ---
all_teams = [Team(d["team"], d["points"], d["placement"]) for d in raw_data]

# --- ASSIGN PLAYERS ---
players = [
    TeamManager("Ollie", ['CSK', 'RCB', 'GT', 'RR', 'LSG']),
    TeamManager("Luke", ['MI', 'KKR', 'SRH', 'DC', 'PBKS']),
]

for p in players:
    p.assign_teams(all_teams)

# --- STATS CALCULATIONS ---
top_team = sorted(all_teams, key=lambda x: x.placement)[0]
top_owner = next((p.name for p in players if top_team.name in p.team_names), "Unknown")
best_points_player = max(players, key=lambda p: p.average_points())
best_placement_player = min(players, key=lambda p: p.average_placement())

# --- STREAMLIT UI ---
st.title("🏏 IPL Team Tracker")

# Toggle mock/API view
st.info(f"**Data Source:** {'Mock Data' if USE_MOCK_DATA else 'Live API'}")

st.subheader("📊 Full Table")
team_rows = [{"Team": t.name, "Points": t.points, "Placement": t.placement} for t in all_teams]
st.dataframe(team_rows, use_container_width=True)

st.subheader("🧑‍🤝‍🧑 Player Stats")
for player in players:
    st.markdown(f"**{player.name}**")
    st.write(f"- Avg Points: `{player.average_points():.2f}`")
    st.write(f"- Avg Placement: `{player.average_placement():.2f}`")

st.subheader("🏆 Highlights")
col1, col2, col3 = st.columns(3)
col1.metric("Top Team", top_team.name, f"Owned by {top_owner}")
col2.metric("Best Avg Points", best_points_player.name, f"{best_points_player.average_points():.2f}")
col3.metric("Best Avg Placement", best_placement_player.name, f"{best_placement_player.average_placement():.2f}")

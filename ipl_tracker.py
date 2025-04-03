import streamlit as st

# --- Class Definitions ---
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

# --- Mock data ---
team_data = [
    ('CSK', 12, 4), ('RCB', 10, 6), ('GT', 6, 8),
    ('RR', 14, 2), ('LSG', 8, 7), ('MI', 10, 5),
    ('KKR', 16, 1), ('SRH', 12, 3), ('DC', 6, 9), ('PBKS', 4, 10)
]

all_teams = [Team(name, points, place) for name, points, place in team_data]

# --- Assign ownership ---
players = [
    TeamManager("Ollie", ['CSK', 'RCB', 'GT', 'RR', 'LSG']),
    TeamManager("Luke", ['MI', 'KKR', 'SRH', 'DC', 'PBKS']),
]

for player in players:
    player.assign_teams(all_teams)

# --- Find top team & stats ---
top_team = sorted(all_teams, key=lambda x: x.placement)[0]
top_owner = next((p.name for p in players if top_team.name in p.team_names), "Unknown")
best_points_player = max(players, key=lambda p: p.average_points())
best_placement_player = min(players, key=lambda p: p.average_placement())

# --- Streamlit UI ---
st.title("🏏 IPL Team Tracker")
st.subheader("📊 Team Ownership & Stats")

# Show table of all teams
st.markdown("### Full Table (Mock Data)")
team_rows = [{"Team": t.name, "Points": t.points, "Placement": t.placement} for t in all_teams]
st.dataframe(team_rows, use_container_width=True)

# Show average stats per player
st.markdown("### Player Stats")
for player in players:
    st.markdown(f"**{player.name}**")
    st.write(f"- Avg Points: `{player.average_points():.2f}`")
    st.write(f"- Avg Placement: `{player.average_placement():.2f}`")

# Highlights section
st.subheader("🏆 Leaderboard Highlights")
col1, col2, col3 = st.columns(3)
col1.metric("Top Team", top_team.name, f"Owned by {top_owner}")
col2.metric("Best Avg Points", best_points_player.name, f"{best_points_player.average_points():.2f}")
col3.metric("Best Avg Placement", best_placement_player.name, f"{best_placement_player.average_placement():.2f}")

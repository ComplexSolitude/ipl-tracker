cclass Team:
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

# --- Output results ---
print("\n📊 IPL Competition Stats:\n")
for player in players:
    print(f"{player.name}")
    print(f"  Avg Points: {player.average_points():.2f}")
    print(f"  Avg Placement: {player.average_placement():.2f}\n")
    
# --- Top team ---
top_team = sorted(all_teams, key=lambda x: x.placement)[0]

# Find who owns the top team
top_owner = next((p.name for p in players if top_team.name in p.team_names), "Unknown")
# Find highest average points
best_points_player = max(players, key=lambda p: p.average_points())
# Find lowest average placement (closer to 1 is better)
best_placement_player = min(players, key=lambda p: p.average_placement())

print(f"🥇 Top Team: {top_team.name} ({top_team.points} pts) - Owned by: {top_owner}")
print(f"\n🏆 Highest Average Points: {best_points_player.name} ({best_points_player.average_points():.2f})")
print(f"\n📍 Best Average Placement: {best_placement_player.name} ({best_placement_player.average_placement():.2f})")

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

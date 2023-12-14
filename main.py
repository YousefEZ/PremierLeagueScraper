import csv

from rich.progress import Progress, track

from leaguescraper import LeagueTable, FIELDS, validate


if __name__ == "__main__":
    with open("leaguetables.csv", "w") as league_table_file:
        writer = csv.DictWriter(league_table_file, fieldnames=FIELDS)
        fields = set(FIELDS)
        for season in track(range(2000, 2024)):
            for team in LeagueTable(season).teams:
                writer.writerow(validate(team.data(fields), fields))

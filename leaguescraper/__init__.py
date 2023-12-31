from typing import cast, Any, Dict, Set, List, Generator

import bs4
import urllib
import urllib.request

BASE_URL = "https://fbref.com/en/comps/9"
HEADERS = {"User-Agent": "Mozilla/5.0"}


FIELDS = [
    "season",
    "rank",
    "team",
    "games",
    "wins",
    "ties",
    "losses",
    "goals_for",
    "goals_against",
    "goal_diff",
    "points",
    "points_avg",
    "xg_for",
    "xg_against",
    "xg_diff",
    "xg_diff_per90",
]


def create_url(season: int) -> str:
    """Creates the url based on the given season, from the season before

    Args:
            season: the season of the season from before to this season

    Example:
            2001, would result in the season 2000-2001
    """
    return f"{BASE_URL}/{season-1}-{season}/{season-1}-{season}-Premier-League-Stats"


class Team:
    def __init__(self, name: str, data: Dict[str, Any], season: int, rank: int):
        self._name = name
        self._data = data
        self._data["team"] = name
        self._data["season"] = season
        self._data["rank"] = rank

    def data(self, keys: Set[str]):
        return dict(filter(lambda item: item[0] in keys, self._data.items()))


class LeagueTable:
    def __init__(self, season: int):
        self._year = season
        self._teams = list(self._scrape())

    @property
    def teams(self) -> List[Team]:
        return self._teams

    @property
    def season(self) -> int:
        return self._year

    """
    def _format_form(self, last: bs4.element.Tag) -> Dict[str, Any]:
        return "".join(map(lambda row: row.string, last.find_all("a")))
    """

    def _scrape(self) -> Generator[Team, None, None]:
        page_req = urllib.request.Request(create_url(self._year), headers=HEADERS)
        page = urllib.request.urlopen(page_req)
        soup = bs4.BeautifulSoup(page, "html.parser")

        raw_table = soup.find("table")
        assert raw_table is not None, "Could not find table"

        tbody = raw_table.find("tbody")
        assert type(tbody) == bs4.element.Tag, "Could not find table body"

        table = list(tbody.children)
        for i in range(1, len(table), 2):
            row = cast(bs4.element.Tag, table[i])
            cols = list(row.find_all("td"))
            yield Team(
                cols[0].find("a").string,
                {
                    cols[column].get("data-stat"): cols[column].string
                    for column in range(1, len(cols))
                },
                self._year,
                (i // 2) + 1,
            )


def validate(data: Dict[str, Any], fields: Set[str]):
    # if the a field in fields is not in data, then set that key to -1
    for field in fields:
        if field not in data:
            data[field] = -1
    return data

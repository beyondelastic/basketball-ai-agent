import xml.etree.ElementTree as ET
import httpx
from typing import Any, Dict, Annotated
from datetime import datetime
from semantic_kernel.functions import kernel_function

# This plugin fetches EuroLeague game results and processes them.
class EuroleaguePlugin:

    # This function converts an XML element and its children to a dictionary.
    def xml_to_dict(self, element: ET.Element) -> Any:
        """Recursively converts an XML element and its children to a dictionary."""
        node = {}
        if element.attrib:
            node.update(element.attrib)
        children = list(element)
        if children:
            for child in children:
                child_dict = self.xml_to_dict(child)
                if child.tag not in node:
                    node[child.tag] = []
                node[child.tag].append(child_dict)
        else:
            node = element.text or ""
        return node

    # This function fetches the latest six EuroLeague game results for a given season.
    @kernel_function
    async def get_latest_euroleague_game_results(self, season: Annotated[str, "The year of the season, e.g. 2024 for season 2024/25"]) -> Dict[str, Any]:
        """Fetches EuroLeague game results and returns only the last 6 games by date."""
        url = "https://api-live.euroleague.net/v1/results"
        params = {"season_code": "E" + season}
        headers = {"Accept": "application/xml"}
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url, params=params, headers=headers)
                response.raise_for_status()
                root = ET.fromstring(response.text)
                data = self.xml_to_dict(root)

            # Extract the games from the parsed XML data
            games = data.get("game", [])  

            # Parse and sort games by date
            def parse_date(game):
                
                # The date is a list, so get the first element
                date_val = game.get("date", [""])
                if isinstance(date_val, list):
                    date_str = date_val[0]
                else:
                    date_str = date_val
                try:
                    return datetime.strptime(date_str, "%b %d, %Y")
                except Exception:
                    return datetime.min
                
            # Sort the games by date in descending order
            games_sorted = sorted(games, key=parse_date, reverse=True)
            last_6_games = games_sorted[:6]

            # Replace the games in the data dict with only the last 6
            data["game"] = last_6_games
            return data
        
        # Exception handling
        except Exception as e:
            print(f"Exception when making direct request: {e}")
            return {}
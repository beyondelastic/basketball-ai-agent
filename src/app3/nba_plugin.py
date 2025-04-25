from nba_api.live.nba.endpoints import scoreboard
from typing import Dict, Any
from semantic_kernel.functions import kernel_function

# This plugin fetches the NBA scoreboard for today or latest.
class NBAplugin:

    # This function fetches the NBA scoreboard for today or latest.
    @kernel_function
    async def get_nba_live_scoreboard(self) -> Dict[str, Any]:
        """Fetch today's NBA scoreboard (live or latest)."""
        try:
            sb = scoreboard.ScoreBoard()
            return sb.get_dict()
        except Exception as e:
            return {"error": str(e)}

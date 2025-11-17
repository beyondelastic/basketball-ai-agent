"""
Basketball roster management tools.
"""
from typing import List, Dict, Any


def get_roster_status() -> List[Dict[str, Any]]:
    """
    Get the current roster status with player stats and availability.
    
    Returns a list of 8 basketball players with their positions, individual skills,
    and current game statistics. 5 players show active game stats (having played),
    while 3 bench players show 0 minutes played.
    
    Returns:
        List[Dict[str, Any]]: List of player dictionaries containing:
            - Basic info: name, position, jersey_number
            - Skills: shooting, ball_handling, passing, rebounding, strength, speed (1-10 scale)
            - Game stats: minutes_played, points, assists, rebounds, turnovers, fouls
    """
    roster = [
        # Starting 5 - Active players with game stats
        {
            "name": "Marcus Johnson",
            "position": "Point Guard",
            "jersey_number": 1,
            "skills": {
                "shooting": 7,
                "ball_handling": 9,
                "passing": 9,
                "rebounding": 6,
                "strength": 6,
                "speed": 8
            },
            "game_stats": {
                "minutes_played": 28,
                "points": 14,
                "assists": 8,
                "rebounds": 4,
                "turnovers": 3,
                "fouls": 2
            }
        },
        {
            "name": "Tyler Rodriguez",
            "position": "Shooting Guard",
            "jersey_number": 23,
            "skills": {
                "shooting": 9,
                "ball_handling": 7,
                "passing": 6,
                "rebounding": 5,
                "strength": 7,
                "speed": 7
            },
            "game_stats": {
                "minutes_played": 32,
                "points": 21,
                "assists": 3,
                "rebounds": 5,
                "turnovers": 2,
                "fouls": 1
            }
        },
        {
            "name": "Kevin Thompson",
            "position": "Small Forward",
            "jersey_number": 33,
            "skills": {
                "shooting": 8,
                "ball_handling": 6,
                "passing": 7,
                "rebounding": 7,
                "strength": 8,
                "speed": 7
            },
            "game_stats": {
                "minutes_played": 30,
                "points": 16,
                "assists": 4,
                "rebounds": 7,
                "turnovers": 1,
                "fouls": 3
            }
        },
        {
            "name": "David Wilson",
            "position": "Power Forward",
            "jersey_number": 44,
            "skills": {
                "shooting": 6,
                "ball_handling": 4,
                "passing": 5,
                "rebounding": 9,
                "strength": 9,
                "speed": 5
            },
            "game_stats": {
                "minutes_played": 26,
                "points": 12,
                "assists": 2,
                "rebounds": 9,
                "turnovers": 2,
                "fouls": 4
            }
        },
        {
            "name": "Andre Davis",
            "position": "Center",
            "jersey_number": 55,
            "skills": {
                "shooting": 5,
                "ball_handling": 3,
                "passing": 4,
                "rebounding": 10,
                "strength": 10,
                "speed": 4
            },
            "game_stats": {
                "minutes_played": 24,
                "points": 8,
                "assists": 1,
                "rebounds": 11,
                "turnovers": 1,
                "fouls": 3
            }
        },
        # Bench players - 0 minutes played
        {
            "name": "Chris Martinez",
            "position": "Point Guard",
            "jersey_number": 12,
            "skills": {
                "shooting": 6,
                "ball_handling": 8,
                "passing": 8,
                "rebounding": 5,
                "strength": 5,
                "speed": 9
            },
            "game_stats": {
                "minutes_played": 0,
                "points": 0,
                "assists": 0,
                "rebounds": 0,
                "turnovers": 0,
                "fouls": 0
            }
        },
        {
            "name": "James Parker",
            "position": "Forward",
            "jersey_number": 34,
            "skills": {
                "shooting": 7,
                "ball_handling": 5,
                "passing": 6,
                "rebounding": 8,
                "strength": 8,
                "speed": 6
            },
            "game_stats": {
                "minutes_played": 0,
                "points": 0,
                "assists": 0,
                "rebounds": 0,
                "turnovers": 0,
                "fouls": 0
            }
        },
        {
            "name": "Michael Brown",
            "position": "Center",
            "jersey_number": 50,
            "skills": {
                "shooting": 4,
                "ball_handling": 2,
                "passing": 3,
                "rebounding": 9,
                "strength": 9,
                "speed": 3
            },
            "game_stats": {
                "minutes_played": 0,
                "points": 0,
                "assists": 0,
                "rebounds": 0,
                "turnovers": 0,
                "fouls": 0
            }
        }
    ]
    
    return roster
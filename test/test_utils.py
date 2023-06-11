import pytest
from ..utils import count_players_in_event

def test_count_players_in_event():
    groups = [
        {"id": 1, "size": 5},
        {"id": 2, "size": 3},
        {"id": 3, "size": 4},
    ]
    events = [
        {"id": 100, "groups": [1, 2]},
        {"id": 200, "groups": [2, 3]},
        {"id": 300, "groups": []},
    ]

    assert count_players_in_event(groups, events[0]) == 8
    assert count_players_in_event(groups, events[1]) == 7
    assert count_players_in_event(groups, events[2]) == 0
    assert count_players_in_event(groups, None) == 0
    assert count_players_in_event(groups, {'id': 100}) == 0

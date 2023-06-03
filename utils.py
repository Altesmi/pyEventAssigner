def count_players_in_event(groups, events, eventId):
  eInd = next((i for i, e in enumerate(events) if e["id"] == eventId), None)
  # return 0 if there are no groups in the event
  if eInd is None or len(events[eInd]["groups"]) == 0:
    return 0
  # sum up the individual group sizes
  playerCount = sum(groups[gInd]["size"] for gInd in map(lambda x: next(i for i, g in enumerate(groups) if g["id"] == x), events[eInd]["groups"]))

  return playerCount

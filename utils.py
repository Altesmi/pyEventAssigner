# def count_players_in_event(groups, events, event_id):
#     eInd = next((i for i, e in enumerate(events) if e["id"] == event_id), None)
#     # return 0 if there are no groups in the event
#     if eInd is None or len(events[eInd]["groups"]) == 0:
#         return 0
#     # sum up the individual group sizes
#     playerCount = sum(groups[gInd]["size"] for gInd in map(lambda x: next(i for i, g in enumerate(groups) if g["id"] == x), events[eInd]["groups"]))

#     return playerCount


def update_after_assignment(events,
                            phantom_events,
                            groups,
                            assignments,
                            assigned_event,
                            assigned_group,
                            phantom_to_real=False):

    # if there is a phantom event need to handle every group in the event
    # otherwise it is enough to handle just the assigned group.
    # Therefore check first is the event a phantom event

    events_updated = events.copy()
    phantom_events_updated = phantom_events.copy()
    assignments_updated = assignments.copy()
    deficit_updated = 0  # this is calculated below

    if phantom_to_real:
        # This event was a phantom event but now has enough groups to be a real event
        # Remove all the groups in the event from all other events they are set

        # First remove the assigned event from phantom events
        phantom_events_updated.remove(assigned_event['id'])

        # Find the index of the assigned_event in the events dict and set every group's assignment there
        # to assigned_event

        assigned_event_ind = find_index_in_list_of_dicts(events, 'id', assigned_event['id'])

        for group_id in events_updated[assigned_event_ind]['groups']:
            # Assign groups to assigend_event
            assignment_ind = find_index_in_list_of_dicts(assignments, 'id', group_id)
            assignments_updated[assignment_ind]['assignment'] = assigned_event['id']

            # Remove groups from any other event they were assigned to

            for event in events_updated:
                if event['id'] != assigned_event['id']:
                    if group_id in event['groups']:
                        event['groups'].remove(group_id)
                        num_players = count_players_in_event(groups, event)
                        if event['id'] not in phantom_events_updated and num_players < event['min']:
                            # This event has become a phantom event because the group got assigned to another event
                            # set this event to be phantom event again
                            phantom_events_updated, assignments_updated = set_real_event_to_phantom_event(
                                groups,
                                events_updated,
                                phantom_events,
                                event,
                                assignments_updated)
                        elif num_players == 0 and event['id'] in phantom_events_updated:
                            phantom_events_updated.remove(event['id'])
    else:
        # This event is already a real event. Remove that group
        # from possible other events
        event_ind = find_index_in_list_of_dicts(events, 'id', assigned_event['id'])

        for event in events_updated:
            if assigned_group['id'] in event['groups'] and event['id'] != events[event_ind]['id']:
                event['groups'].remove(group_id)
                num_players = count_players_in_event(groups, event)
                if event['id'] not in phantom_events_updated and num_players < event['min']:
                    # This event has become a phantom event because the group got assigned to another event
                    # set this event to be phantom event again
                    phantom_events_updated, assignments_updated = set_real_event_to_phantom_event(
                        groups,
                        events_updated,
                        phantom_events,
                        event,
                        assignments_updated)
                elif num_players == 0 and event['id'] in phantom_events_updated:
                    phantom_events_updated.remove(event['id'])


    # Check that deficit equals sum ( event min - numPlayers in event)
    # over the set of phantom events

    if len(phantom_events_updated) > 0:
        for event_id in phantom_events_updated:
            event_ind = find_index_in_list_of_dicts(events,'id',event_id)
            num_players = count_players_in_event(groups, events_updated[event_ind])
            deficit_updated = deficit_updated + (events[event_ind]['min'] - num_players)

    return events_updated, phantom_events_updated, assignments_updated, deficit_updated

def initialize_assignment(groups):
    return list(map(lambda x: {'id': x['id'], 'assignment': -1}, groups))


def remove_id_from_list(list, id):
    return [l for l in list if list['id'] != id]


def includes_event(events, id):
    return len([event for event in events if event['id'] == id]) > 0


def count_players_in_list(list):
    return sum([l['size'] for l in list])


def count_players_in_events(groups, events):
    return list(map(lambda x: {'id': x['id'], 'num_players': sum(i['size'] for i in groups if x['id'] in i['pref'])}, events))

def count_players_in_event(groups, event):
    if event is None or 'groups' not in event.keys():
        return 0
    return sum([x['size'] for x in groups if x['id'] in event['groups']])

def find_index_in_list_of_dicts(list, target_field, target_value):
    return next((ind for (ind, list_item) in enumerate(list) if list_item[target_field] == target_value), None)


def count_players_currently_in_event(assignments, groups, event):
    assigned_groups = [x['id']
                       for x in assignments if x['assignment'] == event['id']]
    return sum([x['size'] for x in groups if x['id'] in assigned_groups])


def count_unassigned_players(assignments, groups):
    unassigned_groups = [x['id']
                         for x in assignments if x['assignment'] == -1]
    return sum([x['size'] for x in groups if x['id'] in unassigned_groups])


def set_real_event_to_phantom_event(groups, events, phantom_events, new_phantom_event, assignments):
    assignments_updated = assignments.copy()
    phantom_events_updated = phantom_events.copy()

    phantom_events_updated.append(new_phantom_event['id'])

    # set the assignment of the groups in event to be -1

    for new_phantom_event_group_id in new_phantom_event['groups']:
        new_phatom_event_assignment_ind = find_index_in_list_of_dicts(assignments, 'id', new_phantom_event_group_id)
        assignments_updated[new_phatom_event_assignment_ind]['assignment'] = -1

    return phantom_events_updated, assignments_updated

def find_groups_with_certain_preference(groups, pref):
    groups_to_event = [x['id'] for x in groups if pref in x['pref']]
    return groups_to_event
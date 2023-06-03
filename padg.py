# import { updateGroupsAfterAssignment } from './updateGroupsAfterAssignment'
from utils import count_players_in_event
# from update_groups_after_assignment import update_groups_after_assignment


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


def count_players_currently_in_event(assignments, groups, event):
    assigned_groups = [x['id']
                       for x in assignments if x['assignment'] == event['id']]
    return sum([x['size'] for x in groups if x['id'] in assigned_groups])

def count_unassigned_players(assignments, groups):
    unassigned_groups = [x['id']
                       for x in assignments if x['assignment'] == -1]
    return sum([x['size'] for x in groups if x['id'] in unassigned_groups])

def update_groups_and_events_after_assignment(assignments, assignment_id, groups_to_be_assigned, events):
    assignment_inds = [i for i,x in enumerate(assignments) if x['assignment'] in [100]]

    group_ids = [x['id'] for x in groups_to_be_assigned]

    # Update assignments
    for i in assignment_inds:
        assignments[i]['assignment'] = assignment_id

    # Remove the groups from every other events

    for event in events:
        if event['id'] is not assignment_id:
            event['groups'] = list(filter(lambda x: x not in group_ids , event['groups']))

    return assignments, events
    

def padg(input):
    groups, events, gain_list, update_list = input
    assignments = initialize_assignment(groups)

    phantom_events = []

    deficit = 0

    # unassigned_groups = groups.copy()

    gain_list.sort(key=lambda x: x['gain'])

    num_players_signed_to_events = count_players_in_events(groups, events)

    for gain_list_item in gain_list:

        # Find indices of this list item from events, groups and assignments lists
        event_ind = next((i for i, item in enumerate(events)
                         if item["id"] == gain_list_item['event']), None)

        group_ind = next((i for i, item in enumerate(groups)
                         if item["id"] == gain_list_item['id']), None)

        assignment_ind = next((i for i, item in enumerate(
            assignments) if item["id"] == gain_list_item['id']), None)
        
        # For convenience define current group, event and assignment for easier reference
        current_group = groups[group_ind]
        current_event = events[event_ind]
        current_assignment = assignments[assignment_ind]

        # check if there are enough people signed up for this game
        # in order to avoid matching some group with this event
        # without hope of this event ever happening

        num_players_signed_to_event = next(
            (item['num_players'] for item in num_players_signed_to_events if item["id"] == gain_list_item['event']), None)

        if (gain_list_item['gain'] > 0 and num_players_signed_to_event >= current_event['min']):
            # consider only cases where adding u to event increases happiness
            # and those where there is even theoretically possible to have
            # minimum number of players
            current_num_players_in_event = count_players_currently_in_event(
                assignments, groups, current_event)
            current_num_unassigned_players = count_unassigned_players(assignments, groups)
            if assignments[assignment_ind]['assignment'] == -1 and \
                    current_num_players_in_event + groups[group_ind]['size'] <= current_event['max']:
                # group in listElement is not assigned and there is space in the event
                #  where we try to place
                if current_num_players_in_event == 0:
                    # no players currently in the event
                    if deficit + (current_event['min'] - current_group['size']) < current_num_unassigned_players \
                        and current_event['id'] not in phantom_events:
                        # Assigning current_group to current_event does not increase deficit over critical limit
                        # And no players yet in this event. Push first to phantom events.
                            phantom_events.push(current_event['id'])
                        # else the event is already a phantom event
                        # Phantom events are checked below and they can become real events
                        
                elif current_event[id] in phantom_events:
                    # Event has players no need to put it in phantom events
                    deficit = deficit - current_group['size']

            # Next we put the group to the event since there is place for it
            events[event_ind]['groups'].push(current_group['id'])

            # No check if the putting the current group to this event pushed to event to have minimum number of players
            # and thus not being a phantom event anymore

            if current_num_players_in_event + current_group['size'] >= current_event['min']\
                and current_event['id'] in phantom_events:

                # This event was a phantom event but is not anymore

                assignments[assignment_ind]['assignment'] = current_event['id']

                # Update the assignment also for the other groups



                #     if (assignment[assignmentInd].assignment === -1
                #       && countPlayersInEvent(groups, events, listElement.event) + listElement.size
                #         <= events[eventInd].max) {
                #       // group in listElement is not assigned and there is space in the event where we try to place

                #       // const playersBefore =
                #       if (countPlayersInEvent(groups, events, listElement.event) === 0) {
                #         // no players in this event
                #       .... there was somthing here...
                #
                #       } else if (phantomEvents.includesEvent(events[eventInd]) === 1) {
                #         // event has players, decrease deficit
                #         deficit -= listElement.size
                #       }
                #       events[eventInd].groups.push(listElement.id)

                #       unassignedGroups.removeGroup(listElement.id)
                #       if (countPlayersInEvent(groups, events, listElement.event) >= events[eventInd].min
                #       && phantomEvents.includesEvent(events[eventInd]) === 0) {
                #         // this event is not a phantom event, set M(u) to a
                #         assignment[assignmentInd].assignment = listElement.event
                #         const updatedObjects = updateGroupsAfterAssignment(events, phantomEvents, groups, unassignedGroups, assignment, groups[groupInd], listElement.event, 'real')
                #         groups = updatedObjects.returnGroups
                #         events = updatedObjects.returnEvents
                #         deficit = updatedObjects.returnDeficit
                #         unassignedGroups = updatedObjects.returnUnassignedGroups
                #         phantomEvents = updatedObjects.returnPhantomEvents
                #         assignment = updatedObjects.returnAssignment
                #       }

                #       if (countPlayersInEvent(groups, events, listElement.event) >= events[eventInd].min
                #       && phantomEvents.includesEvent(events[eventInd]) === 1) {
                #         // this event is a phantom event but has now enough players to be a real event
                #         assignment[assignmentInd].assignment = listElement.event
                #         const updatedObjects = updateGroupsAfterAssignment(events, phantomEvents, groups, unassignedGroups, assignment, groups[groupInd], listElement.event, 'phantomToReal')
                #         groups = updatedObjects.returnGroups
                #         events = updatedObjects.returnEvents
                #         deficit = updatedObjects.returnDeficit
                #         unassignedGroups = updatedObjects.returnUnassignedGroups
                #         phantomEvents = updatedObjects.returnPhantomEvents
                #         assignment = updatedObjects.returnAssignment
                #       }

                #       // Update list LL if there was no assignment
                #       if (assignment[assignmentInd].assignment === -1) {
                #         list = updateL(
                #           {
                #             groups,
                #             events,
                #             assignment,
                #             unassignedGroups,
                #             deficit,
                #             list,
                #             groupId: listElement.id,
                #           },
                #         )
                #       }
                #     }
                #   }

                #   return assignment
                # }

                # module.exports = { padgOpt }

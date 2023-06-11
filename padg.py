from utils import (count_players_currently_in_event,
                   count_players_in_event,
                   count_players_in_events,
                   count_unassigned_players,
                   initialize_assignment,
                   update_after_assignment)


def padg(input):
    groups, events, gain_list = input.values()
    assignments = initialize_assignment(groups)

    phantom_events = []

    deficit = 0

    # unassigned_groups = groups.copy()

    gain_list.sort(key=lambda x: x['gain'], reverse=True)

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

        # check if there are enough people signed up for this game
        # in order to avoid matching some group with this event
        # without hope of this event ever happening

        num_players_signed_to_event = next(
            (item['num_players'] for item in num_players_signed_to_events if item["id"] == gain_list_item['event']), None)
        print(gain_list_item)
        print(current_group)
        if (gain_list_item['gain'] > 0 and num_players_signed_to_event >= current_event['min']):
            # consider only cases where adding u to event increases happiness
            # and those where there is even theoretically possible to have
            # minimum number of players
            current_num_players_in_event = count_players_in_event(groups, current_event)
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
                        deficit = deficit + (current_event['min'] - current_group['size'])
                        if current_event['id'] not in phantom_events:
                            phantom_events.append(current_event['id'])
                        # else the event is already a phantom event
                        # Phantom events are checked below and they can become real events

                elif current_event['id'] in phantom_events:
                    # Event has players no need to put it in phantom events
                    deficit = deficit - current_group['size']

                # Next we put the group to the event since there is place for it
                if current_group['id'] not in events[event_ind]['groups']:
                    events[event_ind]['groups'].append(current_group['id'])

                # Now check if the putting the current group to this event pushed to event to have minimum number of players
                # and thus not being a phantom event anymore

                if current_num_players_in_event + current_group['size'] >= current_event['min']\
                        and current_event['id'] in phantom_events:

                    # This event was a phantom event but is not anymore

                    assignments[assignment_ind]['assignment'] = current_event['id']

                    # Update the assignment also for the other groups

                    events, phantom_events, assignments, deficit = update_after_assignment(events,
                                                                                        phantom_events,
                                                                                        groups,
                                                                                        assignments,
                                                                                        current_event,
                                                                                        current_group,
                                                                                        phantom_to_real=True)
                    
                elif current_num_players_in_event + current_group['size'] >= current_event['min']\
                        and current_num_players_in_event + current_group['size'] <= current_event['max']\
                        and current_event['id'] not in phantom_events:
                    assignments[assignment_ind]['assignment'] = current_event['id']
                    if current_group['id'] not in current_event['groups']:
                        # If the event starts without ever being a phantom event (first group size > event min)
                        events[event_ind]['groups'].append(current_group['id'])
                    events, phantom_events, assignments, deficit = update_after_assignment(events,
                                                                                        phantom_events,
                                                                                        groups,
                                                                                        assignments,
                                                                                        current_event,
                                                                                        current_group,
                                                                                        phantom_to_real=False)
            print(assignments)
            print(events)
            print(phantom_events)    

    return assignments
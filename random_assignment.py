import numpy as np
from utils import (count_players_currently_in_event,
                   count_players_in_event,
                   count_players_in_events,
                   count_unassigned_players,
                   initialize_assignment,
                   update_after_assignment,
                   find_index_in_list_of_dicts,
                   find_groups_with_certain_preference)

def random_assignment(input):
    groups, events, _ = input.values()
    assignments = initialize_assignment(groups)

    num_players_in_events = count_players_in_events(groups, events)
    for event in events:
        event_ind_in_num_players = find_index_in_list_of_dicts(num_players_in_events, 'id', event['id'])
        groups_to_this_event = find_groups_with_certain_preference(groups, event['id'])
        if num_players_in_events[event_ind_in_num_players]['num_players'] >= event['min']:
            num_players_to_this_event = 0
            max_num_loops = 10
            num_loops = 0
            assigned_groups = []
            while num_players_to_this_event < event['max'] and num_loops < max_num_loops and len(groups_to_this_event)>0:
                random_group_ind = np.random.randint(0,len(groups_to_this_event))
                group_ind = find_index_in_list_of_dicts(groups, 'id', groups_to_this_event[random_group_ind])
                if groups[group_ind]['size'] + num_players_to_this_event <= event['max']:
                    assigned_groups.append(groups[group_ind]['id'])
                    num_players_to_this_event = num_players_to_this_event + groups[group_ind]['size']
                    groups_to_this_event.remove(groups[group_ind]['id'])
                else:
                    num_loops = num_loops + 1
                
            if num_players_to_this_event >= event['min']:
                for group_id in assigned_groups:
                    group_ind = find_index_in_list_of_dicts(groups, 'id', group_id)

                    assignment_ind = find_index_in_list_of_dicts(assignments, 'id', group_id)

                    assignments[assignment_ind]['assignment'] = event['id']
                    groups = list(filter(lambda x: x['id'] != group_id, groups))

    return assignments

def score_assignment(assignments, gain_list):
    score = 0
    for assignment in assignments:
        if assignment != -1:
            score = score + next((list_item['gain'] for (_, list_item) in enumerate(gain_list) if list_item['id'] == assignment['id'] and list_item['event'] == assignment['assignment']), None)
    return score

def run_random_assignment(input):
    num_rounds = 300
    best_score = -100
    best_assignments = []

    for i in range(num_rounds):
        new_assignments = random_assignment(input)
        new_score = score_assignment(new_assignments, input['gain_list'])

        if new_score > best_score:
            best_score = new_score
            best_assignments = new_assignments

    return best_assignments
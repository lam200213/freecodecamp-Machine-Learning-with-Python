#lam200213
def player(prev_play):
    if not hasattr(player, 'state'):
        player.state = {
            'opponent_history': [],
            'my_history': [],
            'play_order': [{'RR':0, 'RP':0, 'RS':0, 'PR':0, 'PP':0, 'PS':0, 'SR':0, 'SP':0, 'SS':0}],
            'scores': {'quincy':0, 'mrugesh':0, 'kris':0, 'abbey':0},
            'identified_bot': [None],
            'round_counter': 0
        }

    state = player.state
    state['round_counter'] += 1

    if state['round_counter'] % 1000 == 1:
        state['opponent_history'] = []
        state['my_history'] = []
        state['play_order'] = [{'RR':0, 'RP':0, 'RS':0, 'PR':0, 'PP':0, 'PS':0, 'SR':0, 'SP':0, 'SS':0}]
        state['scores'] = {'quincy':0, 'mrugesh':0, 'kris':0, 'abbey':0}
        state['identified_bot'] = [None]

    if prev_play:
        state['opponent_history'].append(prev_play)

    current_round = len(state['opponent_history']) + 1

    move = ['R', 'P', 'S']
    beat_move = {'R': 'P', 'P': 'S', 'S': 'R'}
    choices = ['R', 'R', 'P', 'P', 'S']

    def predict_quincy(round_num):
        return choices[round_num % 5]

    def predict_kris(round_num):
        if round_num == 1:
            return 'P'
        return beat_move[state['my_history'][round_num - 2]]

    def predict_mrugesh(round_num):
        if round_num == 1:
            return 'R'
        last_ten = state['my_history'][max(0, round_num - 11):round_num - 1]
        if not last_ten:
            return 'P'
        counts = {'R': 0, 'P': 0, 'S': 0}
        for move in last_ten:
            counts[move] += 1
        most_frequent = max(counts, key=lambda x: counts[x])
        return beat_move[most_frequent]

    def predict_abbey(round_num):
        my_prev_play = 'R' if round_num == 1 else state['my_history'][round_num - 2]
        potential_plays = [my_prev_play + m for m in ['R', 'P', 'S']]
        sub_order = {k: state['play_order'][0].get(k, 0) for k in potential_plays}
        prediction = max(sub_order, key=sub_order.get)[-1]
        return beat_move[prediction]

    if current_round > 1:
        prev_round = current_round - 1
        if predict_quincy(prev_round) == prev_play:
            state['scores']['quincy'] += 1
        if predict_kris(prev_round) == prev_play:
            state['scores']['kris'] += 1
        if predict_mrugesh(prev_round) == prev_play:
            state['scores']['mrugesh'] += 1
        if predict_abbey(prev_round) == prev_play:
            state['scores']['abbey'] += 1

    if current_round == 21 and not state['identified_bot'][0]:
        max_score = max(state['scores'].values())
        print(state['scores'])
        if max_score >= 15:
            state['identified_bot'][0] = max(state['scores'], key=state['scores'].get)

    if current_round < 21:
        guess = 'R' if current_round <= 10 else move[(current_round - 11) % 3]
    elif not state['identified_bot'][0]:
        guess = move[(current_round - 1) % 3]
    else:
        identified_bot = state['identified_bot'][0]
        if identified_bot == 'quincy':
            quincy_play = predict_quincy(current_round)
            guess = beat_move[quincy_play]
        elif identified_bot == 'kris':
            kris_play = beat_move[state['my_history'][-1]] if state['my_history'] else 'R'
            guess = beat_move[kris_play]
        elif identified_bot == 'mrugesh':
            last_ten = state['my_history'][-10:] if len(state['my_history']) >= 10 else state['my_history']
            most_frequent = 'S' if not last_ten else max(set(last_ten), key=last_ten.count)
            guess = beat_move[beat_move[most_frequent]]  # Double-beat to counter
        elif identified_bot == 'abbey':
            my_prev_play = 'R' if current_round == 21 else state['my_history'][-1]
            potential_plays = [my_prev_play + m for m in ['R', 'P', 'S']]
            sub_order = {k: state['play_order'][0].get(k, 0) for k in potential_plays}
            my_predicted_move = max(sub_order, key=sub_order.get)[-1]  # What Abbey predicts I’ll play
            abbey_play = beat_move[my_predicted_move]
            guess = beat_move[abbey_play]
        else:
            guess = 'R'

    state['my_history'].append(guess)
    if len(state['my_history']) >= 2:
        last_two = ''.join(state['my_history'][-2:])
        state['play_order'][0][last_two] = state['play_order'][0].get(last_two, 0) + 1

    return guess
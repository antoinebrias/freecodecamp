import random
from collections import defaultdict
from itertools import combinations_with_replacement


# The example function below keeps track of the opponent's history and plays whatever the opponent played two plays ago. It is not a very good player so you will need to change the code to pass the challenge.

# def player(prev_play, opponent_history=[]):
#     opponent_history.append(prev_play)

#     guess = "R"
#     if len(opponent_history) > 2:
#         guess = opponent_history[-2]

#     return guess

def player(prev_play, opponent_history=[]):
    opponent_history.append(prev_play)
    #print(opponent_history)
    guess = ''
    if len(opponent_history) <10:
        guess = random.choice(['R', 'P', 'S'])
    else:
        #guess = opponent_history[-2]

            # Fonction pour générer les combinaisons possibles de longueur n
        def generate_combinations(states, n):
            return [''.join(combination) for combination in combinations_with_replacement(states, n)]


        # Définir la longueur de la séquence d'états précédents
        n = 4

        sequence = opponent_history[1:]
    
        #window_size = 200
        #sequence = opponent_history[max(len(opponent_history)-window_size,1):]
        #sequence = opponent_history[1:]

        # Extraire tous les états uniques de la séquence
        states = sorted(set(sequence))
        state_to_index = {state: i for i, state in enumerate(states)}

        # Initialisation d'un dictionnaire pour stocker les transitions
        transition_matrix = defaultdict(lambda: defaultdict(int))

        # Comptage des transitions
        for i in range(n, len(sequence)):
            prev_states = sequence[i - n:i]
            next_state = sequence[i]
            transition_matrix[''.join(prev_states)][next_state] += 1

        # # Affichage de la matrice de transition
        # print("Matrice de transition:")
        # print(generate_combinations(states, n))
        # for prev_states in generate_combinations(states, n):
        #     print(f"{' '.join(prev_states)}: ", end="")
        #     total_transitions = sum(transition_matrix[prev_states].values())
        #     for next_state in transition_matrix[prev_states]:
        #         transition_prob = transition_matrix[prev_states][next_state] / total_transitions
        #         print(f"{next_state}({transition_prob:.2f})", end=" ")
        #     print()

        # Créer une matrice de transition pleine avec epsilon
        epsilon = 0.001
        num_states = len(states)
        transition_matrix_full = [[epsilon] * num_states for _ in range(num_states ** n)]

        # Remplir la matrice de transition pleine à partir de transition_matrix
        for prev_states, transitions in transition_matrix.items():
            prev_states_index = sum(state_to_index[state] * num_states ** (n - 1 - i) for i, state in enumerate(prev_states))
            for next_state, count in transitions.items():
                next_state_index = state_to_index[next_state]
                transition_matrix_full[prev_states_index][next_state_index] += count


        # Normaliser la matrice de transition pleine
        transition_matrix_full_normalized = [
            [count / sum(row) for count in row] for row in transition_matrix_full
        ]

        # Afficher la matrice de transition pleine normalisée
        # print("Matrice de transition pleine normalisée:")
        #for row in transition_matrix_full_normalized:
        #    print(row)

            # Fonction pour effectuer un tirage à partir de la matrice de transition
        def random_transition(prev_states, transition_matrix):
            prev_states_index = sum(state_to_index[state] * num_states ** (n - 1 - i) for i, state in enumerate(prev_states))
            probabilities = transition_matrix[prev_states_index]
            next_state_index = random.choices(range(len(states)), weights=probabilities)[0]
            return states[next_state_index]

        # Fonction pour trouver l'état suivant avec la probabilité de transition maximale
        def max_transition(prev_states, transition_matrix):
            prev_states_index = sum(state_to_index[state] * num_states ** (n - 1 - i) for i, state in enumerate(prev_states))
            probabilities = transition_matrix[prev_states_index]
            next_state_index = probabilities.index(max(probabilities))
            return states[next_state_index]

        # Récupérer l'état initial (les n derniers états de la séquence)
        initial_states = sequence[-n:]

        # Trouver l'état suivant avec la probabilité de transition maximale
        next_state = max_transition(initial_states, transition_matrix_full_normalized)

        # Effectuer un tirage à partir de la matrice de transition pleine normalisée
        #next_state = random_transition(initial_states, transition_matrix_full_normalized)

        if next_state == "P":
            guess = "S"
        if next_state == "R":
            guess = "P"
        if next_state == "S":
            guess = "R"
        
        # Afficher l'état suivant tiré aléatoirement
        # print("Etat actuel:")
        # print(initial_states)
        # print("État suivant tiré aléatoirement à partir de la matrice de transition pleine normalisée:", next_state)

    #mylist = ["apple", "banana", "cherry"]
    
#print(random.choices(mylist, weights = [10, 1, 1], k = 14)) 

    return guess

    
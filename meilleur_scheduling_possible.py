# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 08:33:14 2024

@author: laure
"""

from itertools import permutations

# Définition des tâches
task = [
    [11, 2, 10],
    [21, 3, 10],
    [31, 2, 20],
    [41, 2, 20],
    [51, 2, 40],
    [61, 2, 40],
    [71, 3, 80]]

# Créer les jobs nous-mêmes
number_task = 3
hyperperiod = 20
print('Here at no task')
jobs = []
for i in range(0, number_task):
    print('Here in the loop')
    num_jobs = hyperperiod / task[i][2]
    print(num_jobs)
    for j in range(0, int(num_jobs)):
        print('Here in the second loop')
        job_name = 10 * (i + 1) + (j + 1)
        print(job_name)

        job_arrival = j * task[i][2]
        job_deadline = (j + 1) * task[i][2]

        job = [job_name, task[i][1], job_arrival, job_deadline]
        jobs.append(job)
        print('Here at the end of second loop')
        print(j)


def schedulable_or_not(job_schedule, allow_task_id=None, max_missed_deadlines=1):
    """
    Vérifie si une permutation donnée des tâches est schedulable.
    Renvoie aussi le temps d'attente total si schedulable.
    """
    print('in the function')
    current_time = 0
    waiting_time = 0
    missed_deadlines = 0
    
    for j in job_schedule:
        job_id, exec_time, arrival_time, deadline = j

        # Attendre si la tâche n'est pas encore arrivée
        if current_time < arrival_time:
            current_time = arrival_time

        # Calculer le temps d'attente pour cette tâche
        waiting_time += current_time - arrival_time

        # Vérifier si on dépasse la deadline
        if current_time + exec_time > deadline:
            if allow_task_id and job_id // 10 == allow_task_id:
                # Incrémenter les deadlines manquées si c'est une tâche autorisée
                missed_deadlines += 1
                if missed_deadlines > max_missed_deadlines:
                    return False, float('inf')  # Échec si on dépasse le seuil autorisé
            else:
                return False, float('inf')  # Échec si une tâche non autorisée dépasse sa deadline

        # Mettre à jour le temps courant après exécution
        current_time += exec_time
        print(j)

    return True, waiting_time  # Succès si toutes les tâches respectent leur deadline


# Générer toutes les permutations possibles
all_permutations = permutations(jobs)

# Vérifier les permutations normales (sans dépassement de deadline)
valid_schedules_final = []
total_waiting_time = float('inf') # Borne infinie
best_schedule = None

# Parcourir toutes les permutations 
for i in all_permutations:
    schedulable, waiting_time = schedulable_or_not(i)
    # Si la fonction renvoie True 
    if schedulable:
        valid_schedules_final.append((i, waiting_time))
        # Trouver le meilleur waiting time 
        if waiting_time < total_waiting_time:
            total_waiting_time = waiting_time
            best_schedule = i

# Vérifier les permutations en autorisant tau5 à manquer une deadline
minus_task_5 = []

for i in all_permutations:
    schedulable, waiting_time = schedulable_or_not(i, allow_task_id=5, max_missed_deadlines=1)
    if schedulable:
        minus_task_5.append((i, waiting_time))
        
# Meilleur scheduler global
if valid_schedules_final:
    print("Schedulers valides avec temps d'attente total :")
    for schedule, waiting_time in valid_schedules_final:
        print(f"Ordre: {[job[0] for job in schedule]} | Temps d'attente: {waiting_time}")

    print("\nMeilleur scheduler :")
    print(f"Ordre: {[job[0] for job in best_schedule]} | Temps d'attente minimal: {total_waiting_time}")
else:
    print("Aucun scheduler valide.")

# Meilleur scheduler avec tau5 pouvant manquer une deadline
if minus_task_5:
    best_schedule_tau5 = min(minus_task_5, key=lambda x: x[1])
    print("\nMeilleur scheduler (tau5 peut manquer une deadline) :")
    print(f"Ordre: {[job[0] for job in best_schedule_tau5[0]]} | Temps d'attente minimal: {best_schedule_tau5[1]}")
else:
    print("\nAucun scheduler valide pour tau5 permettant de manquer une deadline.")


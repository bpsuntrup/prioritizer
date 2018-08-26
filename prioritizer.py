''' prioritizer.py
takes a list of tasks and aids in prioritization of tasks.

TODO: test
TODO: extend so that priorities are saved in database
TODO: add gui
TODO: add api for easily adding tasks
TODO: add ability to remove tasks found uninteresting
TODO: add ability to back up database, or even to version control it
TODO: Get q-tip a github account
'''
import itertools
import sqlite3
from sqlite3 import Error
from os.path import expanduser, join
import random
from copy import copy

def bite(i, n=2, fill=None):
    ''' Takes iterator i and bite size (defaults to 2), and returns iterator
    returning "bite"-sized tuples of items from iterator. Iterator i can be
    infinite. Returns tuple stuffed with Nones if iterator size is not divisible
    by n.'''
    while True:
        items = []
        for _ in range(n):
            try:
                items.append(next(i))
            except StopIteration:
                if len(items) == 0:
                    raise StopIteration
                else:
                    number_of_Nones = n = len(items)
                    for _ in range( number_of_Nones ):
                        items.append(fill)
                    break
        yield tuple(items)

def unzip(it):
    ''' inverse function of zip. depends on itertools.tee '''
    lit, rit = itertools.tee(it)
    def left():
        for i in lit:
            yield i[0]
    def right():
        for i in rit:
            yield i[1]
    return left(), right()

# Please make this even for now
tasks = [
    'write story',
    'learn to cook',
    'do dishes',
    'feed poor people',
    'go on an adventure',
    'invest money',
    'learn a new language',
    'apply for a job',
    'teach my child something new',
    'talk to my wife',
    'develop an app',
]

def get_tasks_from_db():
    ''' gets list of tasks from sqlite3 database.
        returns list of (id, task) tuples '''
    try:
        db_path = join(expanduser('~'),'.priorities.db')
        connection = sqlite3.connect(db_path)
        c = connection.cursor()
        c.execute('SELECT id, task, priority FROM tasks;')
        tasks = c.fetchall()
    except Error as e:
        print(e)
    finally:
        connection.close()
    return tasks

def save_tasks_to_db(tasks):
    ''' tasks is a dict of task ids with task name and priority '''
    try:
        db_path = join(expanduser('~'),'.priorities.db')
        connection = sqlite3.connect(db_path)
        c = connection.cursor()
        for task in tasks:
            c.execute('''
                UPDATE tasks
                SET priority = ?
                WHERE id = ?
            ''', task['priority'], task)
        connection.commit()
    except Error as e:
        print(e)
    finally:
        connection.close()

def at_priority(tasks, priority):
    ''' tasks must be a dict of id: {'task': task, 'priority': priority}
    returns dict of tasks at priority level given, or empty dict '''
    return {task: val for task, val in tasks.items() if val['priority'] == priority}

def worst(tasks):
    ''' tasks must be a dict of id: {'task': task, 'priority': priority} '''
    worst_score = float('inf')
    worsts = {}
    for task, val in tasks.items():
        if val['priority'] < worst_score:
            worsts = {
                task: copy(val),
            }
            worst_score = val['priority']
        elif val['priority'] == worst_score:
            worsts[task] = val
    return worsts

def best(tasks):
    ''' tasks must be a dict of id: {'task': task, 'priority': priority} '''
    best_score = 0
    bests = {}
    for task, val in tasks.items():
        if val['priority'] > best_score:
            bests = {
                task: copy(val),
            }
            best_score = val['priority']
        elif val['priority'] == best_score:
            bests[task] = val
    return bests

def compare_tasks(task1, task2, tasks):
    ''' task1 and task2 must be a dict of priority, task ,id'''
    ''' tasks is the global that contains all tasks '''
    chosen_task = None

    print('')
    print('Would you rather: ')
    print('1. {}'.format(task1['task']))
    print('2. {}'.format(task2['task']))
    print('3. Save.')
    print('4. Quit and exit.')
    while True:
        try:
            answer = int(input('> '))
            if answer not in [1,2,3,4]:
                raise ValueError
            break
        except ValueError:
            print('Input must be 1, 2, 3, or 4.')
    if answer == 1:
        print('You chose: \"{}\"'.format(task1['task']))
        tasks[task1['id']]['priority'] = max(task2['priority'] + 1, task1['priority'])
    elif answer == 2:
        print('you chose: {}'.format(task2))
        tasks[task2['id']]['priority'] = max(task1['priority'] + 1, task2['priority'])
    elif answer == 3:
        print('')
        print('Saving...')
        save_tasks_to_db(tasks)
    else:
        best_task = best(tasks)
        print ( 'Results: {}'.format(best_task))
        print ('You should \"{}\"'.format(list(best_task.values())[0]['task']))
        exit(0)

def prioritize(tasks):
    ''' tasks is a list of (id, task_string) tuples
    -- first, take the worst tasks, and if there are better tasks, compare each
       of the worst tasks with a representative from better tasks with each
       higher priority
    -- then, take the best tasks and pit them against each other in a competition
    '''
    tasks = { id: {'task': task, 'priority': priority} for id, task, priority in tasks}
    dangling_task = None
    num_options = 2 # number of options to prioritize at once, reserved for future

    # if all of the tasks are of not of the same priority, we take the lowest
    # priority tasks and give'm a rank
    if not len(best(tasks).items()) == len(tasks.items()):
        worsts = worst(tasks)
        for task in worsts:
            priority = worsts[task]['priority']
            n = 1
            while True:
                priority_tasks = at_priority(tasks, priority + n)
                if not priority_tasks:
                    break
                id, val = random.choice(priority_tasks.items())
                val['id'] = id
                tasks[task]['id'] = task
                compare_tasks(rand_task, tasks[task], tasks)
                n += 1


    while len(best(tasks).items()) > 1:
        i = iter(best(tasks))
        if dangling_task is not None:
            i = itertools.chain(i, [dangling_task,])
            dangling_task = None
        for task1, task2 in bite(i,2,None):
            if task2 is None:
                dangling_task = task1
                break

            # Now get user input
            print('')
            print('Would you rather: ')
            print('1. {}'.format(tasks[task1]['task']))
            print('2. {}'.format(tasks[task2]['task']))
            print('3. Save.')
            print('4. Quit and exit.')
            while True:
                try:
                    answer = int(input('> '))
                    if answer not in [1,2,3,4]:
                        raise ValueError
                    break
                except ValueError:
                    print('Input must be 1, 2, 3, or 4.')
            if answer == 1:
                print('You chose: \"{}\"'.format(tasks[task1]['task']))
                tasks[task1]['priority'] = max(tasks[task2]['priority'] + 1, tasks[task1]['priority'])
            elif answer == 2:
                print('you chose: {}'.format(task2))
                tasks[task2]['priority'] = max(tasks[task1]['priority'] + 1, tasks[task2]['priority'])
            elif answer == 3:
                print('')
                print('Saving...')
                save_tasks_to_db(tasks)
            else:
                best_task = best(tasks)
                print ( 'Results: {}'.format(best_task))
                print ('You should \"{}\"'.format(list(best_task.values())[0]['task']))
                exit(0)

    best_task = best(tasks)
    print ( 'Results: {}'.format(best_task))
    print ('You should \"{}\"'.format(list(best_task.values())[0]['task']))
    while True:
        choice = input('Save? (y/n)')
        choice = choice.upper()
        if choice not in ['Y', 'N']:
            print ('Invalid input.')
            continue
        elif choice == 'Y':
            print('')
            print('Saving...')
            save_tasks_to_db(tasks)
            break
        else:
            break

if __name__ == '__main__':
    tasks = get_tasks_from_db()
    prioritize(tasks)

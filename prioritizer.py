''' prioritizer.py
takes a list of tasks and aids in prioritization of tasks.

TODO: test
TODO: extend so that priorities are saved in database
TODO: add gui
TODO: add api for easily adding tasks
TODO: add ability to remove tasks found uninteresting
TODO: add ability to back up database, or even to version control it
'''
import itertools

def bite(iterable, n=2, fillvalue=None):
    "Collect data into fixed-length chunks or blocks"
    # bite('ABCDEFG', 3, 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return itertools.zip_longest(*args, fillvalue=fillvalue)

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


def best(tasks):
    """ tasks must be a dict of tasks and non-negative integers """
    best_score = 0
    bests = {}
    for task, val in tasks.items():
        if val > best_score:
            bests = {
                task: val,
            }
            best_score = val
        elif val == best_score:
            bests[task] = val
    return bests

def prioritize(tasks):
    tasks = { task: 0 for task in tasks}
    dangling_task = None

    while len(best(tasks).items()) > 1:
        i = iter(best(tasks))
        if dangling_task is not None:
            i = itertools.chain(i, [dangling_task,])
            dangling_task = None
        for task1, task2 in bite(i):
            if task2 is None:
                dangling_task = task1
                break

            # Now get user input
            print('')
            print('Would you rather: ')
            print('1. {}'.format(task1))
            print('2. {}'.format(task2))
            print('3. Quit and exit.')
            while True:
                try:
                    answer = int(input('> '))
                    if answer not in [1,2,3]:
                        raise ValueError
                    break
                except ValueError:
                    print('Input must be 1, 2, or 3.')
            if answer == 1:
                print('You chose: \"{}\"'.format(task1))
                tasks[task1] = max(tasks[task2] + 1, tasks[task1])
            elif answer == 2:
                print('you chose: {}'.format(task2))
                tasks[task2] = max(tasks[task1] + 1, tasks[task2])
            else:
                best_task = best(tasks)
                print ( 'Results: {}'.format(best_task))
                print ('You should \"{}\"'.format(best_task.keys()[0]))
                exit(0)

    best_task = best(tasks)
    print ( 'Results: {}'.format(best_task))
    print ('You should \"{}\"'.format(list(best_task.keys())[0]))

if __name__ == '__main__':
    prioritize(tasks)

''' Program for entering tasks into database '''
import sqlite3
from sqlite3 import Error
import itertools
from os.path import expanduser, join
from pprint import pprint


print('Enter tasks: ')
print('''
("commit" to commit to db,
"clear" to delete tasks in buffer,
"print" to show tasks in buffer,
Ctrl-C to quit)''')
print('')

tasks = []
try:
    while True:
        line = input('> ')
        if line == 'commit':
            try:
                db_path = join(expanduser('~'),'.priorities.db')
                connection = sqlite3.connect(db_path)
                c = connection.cursor()
                c.execute('''
                    CREATE TABLE IF NOT EXISTS tasks (
                        id integer PRIMARY KEY,
                        priority integer NOT NULL,
                        status integer,
                        task text
                    );
                ''')
                for task in tasks:
                    c.execute('''
                        INSERT INTO tasks (task, priority, status)
                        VALUES (?, 0, 0);
                    ''', (task,))
                connection.commit()
                tasks = []
            except Error as e:
                print(e)
            finally:
                connection.close()
        elif line == 'print':
            pprint(tasks)
        elif line == 'clear':
            while True:
                choice = input('Clear buffer? (y/n) ')
                choice = choice.upper()
                if choice in ['Y', 'N']:
                    if choice == 'Y':
                        tasks = []
                    break
                else:
                    print('Invalid input. "y" or "n".')
        elif line == '':
            pass
        else:
            tasks.append(line)
except KeyboardInterrupt:
    print('')
    print(tasks)
    print('')
    



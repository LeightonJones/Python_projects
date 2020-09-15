from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

engine = create_engine('sqlite:///todo.db?check_same_thread = False')

Base = declarative_base()


class Table(Base):
    # creates an empty table named 'task'
    __tablename__ = 'task'
    id = Column(Integer, primary_key=True)
    task = Column(String)
    deadline = Column(Date, default=datetime.today())

    def __repr__(self):
        return self.task


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

session = Session()

today = datetime.today()
week_day = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday',
            4: 'Friday', 5: 'Saturday', 6: 'Sunday'}

table_options = {1: "Today's tasks", 2: "Week's tasks", 3: "All tasks",
                 4: "Missed tasks", 5: "Add task", 6: "Delete task", 0: "Exit"}


def add_task():
    entry = Table(task=input('Enter task \n'),
                  deadline=datetime.strptime(input('Enter deadline\n>'),
                                             '%Y-%m-%d'))
    session.add(entry)
    session.commit()
    print('The task has been added!\n')


def tasks_today():
    if not session.query(Table).all():
        print(f"Today {today.day} {today.strftime('%b')}:\nNothing to do!\n")
    else:
        rows = session.query(Table).filter(Table.deadline == today.date()).all()
        if not rows:
            print(
                f"Today {today.day} {today.strftime('%b')}:\nNothing to do!\n")
        else:
            print(f"Today {today.day} {today.strftime('%b')}")
            for idx, val in enumerate(rows):
                print(f"{idx + 1}. {val}")
            print("")


def weeks_tasks():
    if not session.query(Table).all():
        for i in range(7):
            target_date = today + timedelta(days=i)
            print(f"{week_day[target_date.weekday()]} {target_date.day}"
                  f" {target_date.strftime('%b')}:\n"
                  f"Nothing to do!\n")
    else:
        # define the date range (today to today+7)
        for i in range(7):
            target_date = today + timedelta(days=i)
            rows = session.query(Table).filter(
                Table.deadline == target_date.date()).all()
            print(f"{week_day[target_date.weekday()]} {target_date.day}"
                  f" {target_date.strftime('%b')}:")

            if not rows:
                print('Nothing to do!\n')
            else:
                for idx, val in enumerate(rows):
                    print(f'{idx + 1}. {val}')
                print("")


def all_tasks():
    if not session.query(Table).all():
        pass
    else:
        rows = session.query(Table).order_by(Table.deadline).all()
        for idx, val in enumerate(rows):
            print(f"{idx + 1}. {val}. {val.deadline.day} "
                  f"{val.deadline.strftime('%b')}")
        print("")


def missed_tasks():
    print("Missed tasks:")
    if not session.query(Table).filter(
            Table.deadline < today).order_by(
            Table.deadline).all():
        print("Nothing is missed!\n")
    else:
        rows = session.query(Table).filter(
            Table.deadline < today).order_by(
            Table.deadline).all()
        for idx, val in enumerate(rows):
            print(f"{idx + 1}. {val}. {val.deadline.day} "
                  f"{val.deadline.strftime('%b')}")
        print("")


def delete_task():
    if not session.query(Table).all():
        print("Nothing to delete")
    else:
        rows = session.query(Table).order_by(Table.deadline).all()
        print("Choose the number for the task you want to delete:")
        for idx, val in enumerate(rows):
            print(f"{idx + 1}. {val}. {val.deadline.day} "
                  f"{val.deadline.strftime('%b')}")

        del_sel = rows[int(input())-1]
        session.delete(del_sel)
        session.commit()

        print('The task has been deleted!\n')


while True:
    print(f'1) {table_options[1]}\n'
          f'2) {table_options[2]}\n'
          f'3) {table_options[3]}\n'
          f'4) {table_options[4]}\n'
          f'5) {table_options[5]}\n'
          f'6) {table_options[6]}\n'
          f'0) {table_options[0]}')
    user_sel = int(input(''))
    print("")
    try:
        if table_options[user_sel] == 'Exit':
            print('Bye!')
            break
        elif table_options[user_sel] == "Today's tasks":
            tasks_today()
        elif table_options[user_sel] == "Week's tasks":
            weeks_tasks()
        elif table_options[user_sel] == "All tasks":
            all_tasks()
        elif table_options[user_sel] == "Missed tasks":
            missed_tasks()
        elif table_options[user_sel] == 'Add task':
            add_task()
        elif table_options[user_sel] == "Delete task":
            delete_task()

    except KeyError:
        print('Invalid selection, please try again')

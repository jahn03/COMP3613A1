import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate, get_all_competitions
from App.models import User
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, create_competition, get_all_competitions, get_all_competitions_json, create_result, get_all_results, get_all_results_json, import_competitions_result_from_file, initialize )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the command
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

#-----------------------------------------------------------------------------
# COMPETITION COMMANDS

competition_cli = AppGroup('competition', help='Competition object commans')

@competition_cli.command("create", help="Creates competition")
@click.argument("name")
@click.argument("date")
@click.argument("description")

# 1: create competition
def create_competition_command(name, date, description):
    create_competition(name, date, description)
    print(f'Competiition {name} created!')

# 3: view competitions list
@competition_cli.command("list", help="View competitions list")
@click.argument("format", default="string")

def list_competition_command(format):
    if format == 'string':
        print(get_all_competitions())
    else:
        print(get_all_competitions_json())

app.cli.add_command(competition_cli)




# RESULT COMMANDS

result_cli = AppGroup('result', help='Result object commans')

@result_cli.command("create", help="Creates a result")
@click.argument("competition_id")
@click.argument("student_name")
@click.argument("score")

# create results
def create_result_command(competition_id, student_name, score):
    create_result(competition_id, student_name, score)
    print(f'Result for {student_name} created')

# 4: View competition results
@result_cli.command("list", help="Lists competition results")
@click.argument("format", default="string")

def list_result_command(format):
    if format == 'string':
        print(get_all_results())
    else:
        print(get_all_results_json())

# 2: Import competition results from file
@result_cli.command("import", help="Import competition results from file")
@click.argument("file_path")

def import_result_command(file_path):
    import_competition_results_from_file(file_path)
    print(f'Competition results imported from {file_path}')

app.cli.add_command(result_cli)
#-----------------------------------------------------------------------------
'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)
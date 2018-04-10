from auth import (authenticate, add_user, read_pwdb, write_pwdb, pwhash, get_salt)
import pathlib
import pytest
import tempfile

#create database as fixture
@pytest.fixture
def pwdb_path():
    USERNAME = "admin"
    PASSWORD = "admin"
    SALT =  'HwIqH8YdT}'
    pwdb = {}
    pwdb[USERNAME] = (pwhash(PASSWORD,SALT), SALT)
    FILEPATH = tempfile.gettempdir() / pathlib.Path('test_pwdb.pkl')
    with open(FILEPATH, 'wb+') as pwdbfile:
        write_pwdb(pwdb, pwdbfile)
    return(FILEPATH)

def test_read_pwdb(pwdb_path):

    username = 'admin'
    salt = 'HwIqH8YdT}'
    hashed_password = 11215
    try:
        pwdb_file = open(pwdb_path, 'rb+')
    except FileNotFoundError:
        pwdb_file = open(pwdb_path, 'wb+')

    pwdb = read_pwdb(pwdb_file)

    assert username in pwdb
    assert pwdb[username][1] == salt
    assert pwdb[username][0] == hashed_password



def test_pwhash():
    password = 'admin'
    salt = 'HwIqH8YdT}'
    hashed_password = 11215

    assert pwhash(password, salt) == hashed_password



def test_authenticate_user_in_database(pwdb_path):
    username = 'admin'
    password = 'admin'

    try:
        pwdb_file = open(pwdb_path, 'rb+')
    except FileNotFoundError:
        pwdb_file = open(pwdb_path, 'wb+')

    pwdb = read_pwdb(pwdb_file)

    assert authenticate(username, password, pwdb)

def test_authenticate_user_not_in_database(pwdb_path):
    username = 'user'
    password = 'admin'

    try:
        pwdb_file = open(pwdb_path, 'rb+')
    except FileNotFoundError:
        pwdb_file = open(pwdb_path, 'wb+')

    pwdb = read_pwdb(pwdb_file)

    assert not authenticate(username, password, pwdb)

def test_authenticate_wrong_password(pwdb_path):
    username = 'admin'
    password = 'admin1'

    try:
        pwdb_file = open(pwdb_path, 'rb+')
    except FileNotFoundError:
        pwdb_file = open(pwdb_path, 'wb+')


    pwdb = read_pwdb(pwdb_file)

    assert not authenticate(username, password, pwdb)


def test_add_user(pwdb_path):
    username = 'user1'
    password = 'password1'

    try:
        pwdb_file = open(pwdb_path, 'rb+')
    except FileNotFoundError:
        pwdb_file = open(pwdb_path, 'wb+')

    pwdb = read_pwdb(pwdb_file)
    TEST_PWDB_FLNAME_COPY = tempfile.gettempdir() / pathlib.Path('test_pwdb_copy.pkl')
    pwdb_file_copy = open(TEST_PWDB_FLNAME_COPY, 'wb+')

    # creating a copy of the original test database
    # so that changes don't affect the original test database
    add_user(username, password, get_salt(), pwdb, pwdb_file_copy)

    assert username in pwdb

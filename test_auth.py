import auth
import getpass
import pathlib
import pickle
import random
import string
import tempfile

PWDB_FLNAME = pathlib.Path('test_pwdb.pkl')

def test_right_name_right_password():
    salt = auth.get_salt()
    password = 'real_password'
    pwdb = {'real_name':  (auth.pwhash(password,salt), salt)}
    username = 'real_name'
    pass_text = 'real_password'
    assert auth.authenticate(username, pass_text, pwdb)

def test_right_name_wrong_password():
    salt = auth.get_salt()
    password = 'real_password'
    pwdb = {'real_name':  (auth.pwhash(password,salt), salt)}
    username = 'real_name'
    pass_text = 'wrong_password'
    assert not auth.authenticate(username, pass_text, pwdb)

def test_wrong_name_right_password():
    salt = auth.get_salt()
    password = 'real_password'
    pwdb = {'real_name':  (auth.pwhash(password,salt), salt)}
    username = 'wrong_name'
    pass_text = 'real_password'
    assert not auth.authenticate(username, pass_text, pwdb)

def test_wrong_name_wrong_password():
    salt = auth.get_salt()
    password = 'real_password'
    pwdb = {'real_name':  (auth.pwhash(password,salt), salt)}
    username = 'wrong_name'
    pass_text = 'wrong_password'
    assert not auth.authenticate(username, pass_text, pwdb)

def test_empy_database():
    salt = auth.get_salt()
    pwdb = {}
    username = 'some_name'
    pass_text = 'some_password'
    assert not auth.authenticate(username, pass_text, pwdb)


def test_user_already_exists():
    username = 'old_name'
    password = 'old_password'
    salt = auth.get_salt()
    pwdb = {'old_name':  (auth.pwhash('old_password',salt), salt)}
    pwdb_path = tempfile.gettempdir() / PWDB_FLNAME
    pwdb_file = open(pwdb_path, 'wb')
    pickle.dump(pwdb, pwdb_file)
    salt = auth.get_salt()
    try:
        auth.add_user(username, password, salt, pwdb, pwdb_file)
        assert False
    except:
        assert True


def test_user_not_exists():
    username = 'new_name'
    password = 'new_password'
    salt = auth.get_salt()
    pwdb = {'old_name':  (auth.pwhash('old_password',salt), salt)}
    pwdb_path = tempfile.gettempdir() / PWDB_FLNAME
    with open(pwdb_path, 'wb+') as pwdb_file:
        pickle.dump(pwdb, pwdb_file)
    salt = auth.get_salt()
    try:
        with open(pwdb_path, 'wb+') as pwdb_file:
            auth.add_user(username, password, salt, pwdb, pwdb_file)
        with open(pwdb_path, 'rb+') as pwdb_file:
            pwdb = pickle.load(pwdb_file)
        print(pwdb)
        assert pwdb[username] == (auth.pwhash(password,salt), salt)
    except:
        assert False

from auth import *
import pytest


#pwdb_path = tempfile.gettempdir() / PWDB_FLNAME
pwdb_path = 'pwdb.pkl'
try:
    pwdb_file = open(pwdb_path, 'rb+')
except FileNotFoundError:
    pwdb_file = open(pwdb_path, 'wb+')

def test_get_salt():
    salt = get_salt()
    assert len(salt) == 10
    assert all(c in CHARS for c in salt)

def test_authenticate():
    salt = get_salt()
    name = 'user'
    wrong_name = 'not_a_user'
    valid_pw = 'valid'
    invalid_pw = 'invalid'
    pwdb = {name:(pwhash(valid_pw,salt),salt)}
    assert authenticate(name,valid_pw,pwdb)
    assert not authenticate(name,invalid_pw,pwdb)
    assert not authenticate(wrong_name,valid_pw,pwdb)

def test_read_write():
    salt = get_salt()
    name = 'user'
    pw = 'password'
    pwdb = {name:(pwhash(pw,salt),salt)}
    write_pwdb(pwdb,pwdb_file)
    pwdb_read = read_pwdb(pwdb_file)
    assert pwdb == pwdb_read

def test_add_user():
    pwdb = {}
    salt = get_salt()
    name = 'user'
    pw = 'password'
    pwdb_added = {name:(pwhash(pw,salt),salt)}
    add_user(name,pw,salt,pwdb,pwdb_file)
    assert pwdb == pwdb_added
    pwdb_read = read_pwdb(pwdb_file)
    assert pwdb == pwdb_read
    with pytest.raises(Exception):
        add_user(name,pw,salt,pwdb_added,pwdb_file)

def test_hash():
    pw1 = 'pw1'
    pw2 = 'pw2'
    pw1_shuff = '1wp'
    salt1 = get_salt()
    salt2 = get_salt()
    assert not salt1 == salt2
    hash11 = pwhash(pw1,salt1)
    hash22 = pwhash(pw2,salt2)
    hash21 = pwhash(pw2,salt1)
    hash1_shuff = pwhash(pw1_shuff,salt1)
    hash12 = pwhash(pw1,salt2)
    assert not hash11 == hash22
    assert not hash11 == hash12
    assert not hash11 == hash1_shuff
    assert not hash11 == hash21

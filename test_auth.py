from auth import *

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

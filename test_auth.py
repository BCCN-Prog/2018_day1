import auth as au
import pytest
import os

def test_authenticate_no_user():

    res = au.authenticate( "John Doe", "password", {} )

    assert not res


def test_authenticate_wrong_pass():

    salt  = "SALT"

    hash_ = au.pwhash( "qwerty", salt )

    res = au.authenticate( "John Doe", "1234", { "John Doe" : [hash_, salt] } )

    assert not res



def test_authenticate_valid():

    salt  = "SALT"

    hash_ = au.pwhash( "password", salt )

    res = au.authenticate( "John Doe", "password", { "John Doe" : [hash_, salt] } )

    assert res


def test_add_user_user_exists():
    with pytest.raises( Exception ) as e_info:
        au.add_user( "John Doe", None, None, { "John Doe" : ["", ""] }, None )
        assert str( e_info.value ) == 'Username already exists [John Doe]'


def test_add_user_new_user():
    pwdb = {}
    with au.tempfile.TemporaryFile() as tmp_f:
        au.add_user( "John Doe", "password", "SALT", pwdb, tmp_f )
        assert pwdb == { "John Doe" : (au.pwhash( "password", "SALT"), "SALT" ) }


def test_read_pwdb_no_file():
    with au.tempfile.TemporaryFile() as tmp_f:
        assert au.read_pwdb( tmp_f ) == {}

# doesn't work
def test_read_pwdb_file():
    with au.tempfile.TemporaryFile() as tmp_f:
        pwdb = { "John Doe" : ("HASH", "SALT") }
        au.pickle.dump( pwdb, tmp_f )
        tmp_f.seek(0) 
        assert au.read_pwdb( tmp_f ) == pwdb

# doesn't work
def test_write_pwd():
    with au.tempfile.TemporaryFile() as tmp_f1:
        with au.tempfile.TemporaryFile() as tmp_f2:

            pwdb = { "John Doe" : ("HASH", "SALT") }

            au.pickle.dump( pwdb, tmp_f1 )
            tmp_f1.seek(0)
            au.pickle.dump( pwdb, tmp_f2 )
            tmp_f2.seek(0)
            assert au.read_pwdb( tmp_f1 ) == au.read_pwdb( tmp_f2 )
            

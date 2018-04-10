import auth

def test_get_salt():
    salts = [auth.get_salt() for i in range(100)]
    assert all([len(salt) == 10 for salt in salts]), 'Some are not 10 characters long'
    assert len(set(salts)) == len(salts), 'Tested 100 salts are not unique'

import auth

db = list()
db.append(('daniel', 'vargas', '=2od%]1*9Q', 9966))
db.append(('nadine', 'heere', 'j=U]V.n`l\\', 10976))
db.append(('mayar', 'ali', 'PJM0~RD*|&', 6986))
db.append(('marc', 'vischer', 'nL*E~T&az1', 13112))
db.append(('pooja', 'subramaniam', '%9<:%fSN$}', 18453))

db_dict = dict()
for user in db:
    db_dict[user[0]] = (user[3], user[2])

def test_get_salt():
    salts = [auth.get_salt() for i in range(100)]
    assert all([len(salt) == 10 for salt in salts]), 'Some are not 10 characters long'
    assert len(set(salts)) == len(salts), 'Tested 100 salts are not unique'


def test_pwhash():
    for user in db:
        assert auth.pwhash(user[1], user[2]) == user[3]

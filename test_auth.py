import auth

('daniel', 'vargas', '=2od%]1*9Q', 9966)
('nadine', 'heere', 'j=U]V.n`l\\', 10976)
('mayar', 'ali', 'PJM0~RD*|&', 6986)
('marc', 'vischer', 'nL*E~T&az1', 13112)
('pooja', 'subramaniam', '%9<:%fSN$}', 18453)

def test_get_salt():
    salts = [auth.get_salt() for i in range(100)]
    assert all([len(salt) == 10 for salt in salts]), 'Some are not 10 characters long'
    assert len(set(salts)) == len(salts), 'Tested 100 salts are not unique'

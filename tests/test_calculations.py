import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds


#file name and func have to start with "test.." prefix
#dont have to call the test func in the end (test_add()) also works
#'x, num2, result' is a variable defined by you


#@pytest.fixture : fixture is a func provided by pytest library, which will be run first before all of the remainig funcs
@pytest.fixture
def zero_bank_account_fixture():
    '''returning default starting_balance (0)'''
    return BankAccount()

@pytest.fixture
def bank_account_fixture():
    '''returning stated balance'''
    return BankAccount(50)




@pytest.mark.parametrize('x, num2, result', [(3,2,5), (7,1,8), (12,4,16)])    #make you dont have to repeat calling the func if you wanna test multiple number
def test_add(x,num2,result):
    print("testing add function")
    assert add(x,num2) == result

# def test_add():
#     print("testing add function")
#     assert add(5,3) == 8



def test_subtract():
    assert subtract(9,4) == 5

def test_multiply():
    assert multiply(4,3) == 12

def test_divide():
    assert divide(20,5) == 4


#fixture
def test_bank_set_initial_amount(bank_account_fixture):
    assert bank_account_fixture.balance == 50
# def test_bank_set_initial_amount():     #this is normal assigning class object
#     bank_account = BankAccount(50)
#     assert bank_account.balance == 50


#fixture
def test_bank_default_amount(zero_bank_account_fixture):   #pass the fixture func zero_bank_account as a parameter, py will go find out this func first and continue the works
    assert zero_bank_account_fixture.balance == 0          #with this func we no longer have to keep giving an instance:bank_account = BankAccount()
# def test_bank_default_amount():
#     bank_account = BankAccount()
#     assert bank_account.balance == 0


def test_bank_withdraw(bank_account_fixture):    
    bank_account_fixture.withdraw(20)
    assert bank_account_fixture.balance == 30
# def test_bank_withdraw():    #this is normal assigning class object
#     bank_account = BankAccount(50)
#     bank_account.withdraw(20)
#     assert bank_account.balance == 30



def test_bank_deposit(bank_account_fixture):
    bank_account_fixture.deposit(30)
    assert bank_account_fixture.balance == 80


def test_bank_collect_interest(bank_account_fixture):
    bank_account_fixture.collect_interest()
    assert round(bank_account_fixture.balance,6) == 55

#fixture & parametrize
@pytest.mark.parametrize('deposited, withdrew, expected', [(200,100,100), (50,10,40), (1200,200,1000)])#,(10,50,-40)]) expected can be any amount as it gonna raise the exception and op will error
def test_bank_transaction(zero_bank_account_fixture,deposited,withdrew,expected):
    zero_bank_account_fixture.deposit(deposited)
    zero_bank_account_fixture.withdraw(withdrew)
    assert zero_bank_account_fixture.balance == expected


def test_insufficient(bank_account_fixture):   
    with pytest.raises(InsufficientFunds):      #go check the BankAccounnt classes's withdraw, if withdraaw more than the balance, tell pytest to except/raise the exception from that method
        bank_account_fixture.withdraw(200)
# def test_insufficient(bank_account_fixture):   
#     with pytest.raises(Exception):      #go check the BankAccounnt classes's withdraw, if withdraaw more than the balance, tell pytest to except/raise the exception from that method
#         bank_account_fixture.withdraw(200)

#test_add()
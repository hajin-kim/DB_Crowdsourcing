from django.shortcuts import render
from django.http import HttpResponse
from basicdb.models import Account


# Create your views here.
def insertAccount(request, 
    acc_id, 
    password, 
    name, 
    contact, 
    birth, 
    gender, 
    address, 
    role):
    """
    insert an account into DB
    """

    Account(
        acc_id=acc_id,
        password=password,
        name=name,
        contact=contact,
        birth=birth,
        gender=gender,
        address=address,
        role=role
    ).save()

    # return render(request, 'basicdb/mypage.html',
    #               { 'welcome_text': "successfully inserted a new account with user name " + name })
    return HttpResponse("successfully inserted a new account with user name " + name)



def printAccount(request, acc_id=None):
    """
    print account(s)
    
    acc_id: account id for selection
        if not given, print all accounts in db
    """
    result = "something stub!"
    if acc_id == None:
        result = str(list(Account.objects.values()))
    else:
        result = str(list(Account.objects.filter(acc_id=acc_id)[0]))
    # return render(request, 'basicdb/mypage.html',
    #               { 'welcome_text': "see the console" })
    print(result)
    return HttpResponse("<html><body>"+result+"</body></html>")
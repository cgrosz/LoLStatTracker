from django.shortcuts import render, HttpResponse, redirect
from .models import User
# validation v
from django.contrib import messages
import bcrypt
import requests
import json

def index(request):
    request.session['id'] = 0
    if request.method=="POST":
        redirect('/register')
    return render(request,'login_reg_app/index.html')

def index_register(request):
    errors = User.objects.validations(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hash_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        x = User.objects.create(first_name=request.POST['first_name'],last_name=request.POST['last_name'],email=request.POST['email'],password=hash_password)
        request.session['id'] = x.id
        return redirect("/success")

def index_login(request):
    errors = User.objects.validations(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        x = User.objects.get(email=request.POST['email'])
        request.session['id'] = x.id
        request.session['summoner_name'] = x.summoner_name
        return redirect("/success")

def index_success(request):
    #cn also save user data in session
    if request.method=="POST" or request.session != 0:
        x = User.objects.get(id=request.session['id'])
    
        context = {
            "name": x.first_name,
            "api" : testAPI(),
        }
        return render(request,'login_reg_app/index_success.html',context)
    else:
        return redirect("/")

def index_logout(request):
    request.session['id'] = 0
    return redirect("/")

def display_player(request, player):
    response = requests.get(f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/{player}?api_key=RGAPI-6a5e29a3-ea42-41fd-a605-18d536715a9a")
    test = json.loads(response.text)
    summoner_name = test['name']
    account_id = test['accountId']
    match_history = requests.get(f"https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}?api_key=RGAPI-6a5e29a3-ea42-41fd-a605-18d536715a9a")
    match_history_json = json.loads(match_history.text)
    matches = []
    for i in range (0,15,1):
        matches.append(match_history_json['matches'][i])
    context= {
        "summoner_name" : summoner_name,
        "matches" : matches
    }
    return render(request,'login_reg_app/display_player.html', context)

def account(request):
    player = User.objects.get(id=request.session['id'])
    print(player.summoner_name)
    response = requests.get(f"https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/iluumiz?api_key=RGAPI-6a5e29a3-ea42-41fd-a605-18d536715a9a")
    test = json.loads(response.text)
    print(test)
    account_id = test['accountId']
    match_history = requests.get(f"https://na1.api.riotgames.com/lol/match/v4/matchlists/by-account/{account_id}?api_key=RGAPI-6a5e29a3-ea42-41fd-a605-18d536715a9a")
    match_history_json = json.loads(match_history.text)
    matches = []
    for i in range (0,15,1):
        matches.append(match_history_json['matches'][i])
    context = {
        "name" : "iluumiz",
        "first_name" : player.first_name,
        "matches" : matches
    }
    return render(request,'login_reg_app/account.html', context)



def testAPI():
    #API Key: RGAPI-8ff98b9d-08f1-40a5-8038-403961a9b817
    #response = requests.get("https://na.api.pvp.net/api/lol/na/v1.4/summoner/by-name/Teemo?api_key=RGAPI-a59ac154-0db1-4d68-be05-649e7aed70b6") 
    response = requests.get("https://na1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key=RGAPI-6a5e29a3-ea42-41fd-a605-18d536715a9a")
    test = json.loads(response.text)
    test2 = test['entries']
    #return test2[0]['summonerName']
    #return test2[0]
    challengerList = []
    for i in range(0,99,1):
        summoner_name = test2[i]['summonerName']
        challengerList.append([f"{test2[i]['summonerName']} [LP={test2[i]['leaguePoints']} wins={test2[i]['wins']} loses={test2[i]['losses']}]",summoner_name])
    return challengerList
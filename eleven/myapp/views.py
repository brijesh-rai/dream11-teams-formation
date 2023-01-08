from django.shortcuts import render
from django.http import HttpResponse
from . import models
from itertools import combinations as com,permutations as perm
from numpy import random

# For Index Page
def index(request):    
    a = models.Team.objects.all()
    return render(request,'index.html',{"a":a})

# For Team Details Page
def teams(request):
    try:
        team_a_code = request.GET.get('team_a')
        team_a_name = models.Team.objects.filter(team_code=team_a_code)
        team_b_code = request.GET.get('team_b')
        team_b_name = models.Team.objects.filter(team_code=team_b_code)
        players_a = models.Player.objects.filter(team_code=team_a_code,is_playing=True)
        players_b = models.Player.objects.filter(team_code=team_b_code,is_playing=True)

        return render(request,'teams.html',{
            "team_a_code":team_a_code,
            "team_b_code":team_b_code,
            "team_name_a":team_a_name,
            "team_name_b":team_b_name,
            "players_a":players_a,
            "players_b":players_b
        })
    except Exception as e:
        print(e)
        return render(request,'error.html')

# For All Final Teams
def finalteam(request):
    try:
        team_a_code = request.GET.get('team_a')
        team_b_code = request.GET.get('team_b')
        players_a = models.Player.objects.filter(team_code=team_a_code,is_playing=True)
        players_b = models.Player.objects.filter(team_code=team_b_code,is_playing=True)

        pl_a_detail = []
        pl_b_detail = []
        for j in players_a:
            temp = []
            temp.append(j.name)
            temp.append(j.credit)
            temp.append(str(j.pos))
            temp.append(j.cap)
            temp.append(j.v_cap)
            pl_a_detail.append(temp)
        for j in players_b:
            temp = []
            temp.append(j.name)
            temp.append(j.credit)
            temp.append(str(j.pos))
            temp.append(j.cap)
            temp.append(j.v_cap)
            pl_b_detail.append(temp)

        team_a_len = len(pl_a_detail)
        team_b_len = len(pl_b_detail)
        
        # For All (4,7),(5,6),(6,5),(7,4) Combination
        y=4
        z=7
        final_without_c_vc=[]
        
        while True:
            if(y>7):
                break 
            com_a = tuple(com(range(team_a_len), y))
            com_b = tuple(com(range(team_b_len), z))
            
            for i in com_a:
                temp_a = []
                for j in i:
                    temp_a.append(pl_a_detail[j])
                for l in com_b:
                    temp_b=[]
                    for j in l:
                        temp_b.append(pl_b_detail[j])
                        
                    temp=[]
                    temp.extend(temp_a)
                    temp.extend(temp_b)

                    wk,bat,all,bowl,credit = 0,0,0,0,0
                
                    for k in temp:
                        credit += k[1]
                        if(k[2] == 'WK'):
                            wk += 1
                        elif(k[2] == 'BAT'):
                            bat += 1
                        elif(k[2] == 'ALL'):
                            all += 1
                        elif(k[2] == 'BOWL'):
                            bowl += 1
                    
                    if(credit <= 100):
                        if((wk>=1 and wk<=4) and (bat>=3 and bat<=6) and (all>=1 and all<=4) and (bowl>=3 and bowl<=6)):
                            final_without_c_vc.append(temp)
            y+=1
            z-=1
        
        
        final_without_c_vc = tuple(final_without_c_vc)
        final_with_c_vc = []

        for i in final_without_c_vc:
            for j in range(len(i)):
                if(i[j][3] == True):
                    for k in range(len(i)):
                        if(j !=k ):
                            if(i[k][4] == True):
                                temp = []
                                WK=[]
                                BAT=[]
                                ALL=[]
                                BOWL=[]
                                c = i[j][0]+"-"+i[j][2]+"(C)"
                                vc = i[k][0]+"-"+i[k][2]+"(Vc)"
    
                                for l in range(len(i)):
                                    x = i[l][0]+"-"+i[l][2]
                                    if(i[l][2] == "WK"):
                                        if(l==j):
                                            WK.append(c)
                                        elif(l==k):
                                            WK.append(vc)
                                        else:
                                            WK.append(x)
                                    elif(i[l][2] == "BAT"):
                                        if(l==j):
                                            BAT.append(c)
                                        elif(l==k):
                                            BAT.append(vc)
                                        else:
                                            BAT.append(x)
                                    elif(i[l][2] == "ALL"):
                                        if(l==j):
                                            ALL.append(c)
                                        elif(l==k):
                                            ALL.append(vc)
                                        else:
                                            ALL.append(x)
                                    elif(i[l][2] == "BOWL"):
                                        if(l==j):
                                            BOWL.append(c)
                                        elif(l==k):
                                            BOWL.append(vc)
                                        else:
                                            BOWL.append(x)
                                temp.extend(WK)
                                temp.extend(BAT)
                                temp.extend(ALL)
                                temp.extend(BOWL)        
                                final_with_c_vc.append(temp)

        print(len(final_with_c_vc))
        
        # For Randomly selecting Teams
        siz = request.GET.get('team_size')
        if(siz):
            siz = int(siz)
            while True:    
                random_val = random.randint(len(final_with_c_vc),size=siz)
                random_val = set(random_val)
                if(len(random_val) == siz):
                    break

            final_team = []

            for i in random_val:
                final_team.append(final_with_c_vc[i])
                
        #  For Finding DREAM TEAM

        # playerlst = ["S Billings-WK", "S Iyer-BAT", "R Uthappa-BAT", "A Rayudu-BAT", "A Rahane-BAT", "N Rana-BAT", "U Yadav-BOWL", "V Chakravarthy-BOWL", "R Jadeja-ALL"] 
        # cap =  "D Bravo-BOWL"
        # vcap = "MS Dhoni-WK"
        # dt = []
        # for i in final_with_c_vc:
        #     if(i[0]== cap and i[1]==vcap):
        #         alll = True
        #         for j in playerlst:
        #             if j not in i:
        #                 alll = False
        #                 break
                
        #         if(alll):    
        #             dt.append(i)
        #             break
                
        # print(len(dt))   
            return render(request,'finalteams.html',{
                "final_team":final_team
            })                           
           
        else:
            return render(request,'finalteams.html',{
                "final_team":final_with_c_vc
            })
            
    except Exception as e:
        print(e)
        return render(request,'error.html')

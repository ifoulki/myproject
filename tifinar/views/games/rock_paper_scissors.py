from django.shortcuts import render

def rps_game(request):
    return render(request, 'tifinar/rock_paper_scissors.html')
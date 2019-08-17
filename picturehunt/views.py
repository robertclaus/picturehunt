import random

from django.shortcuts import render
from django.shortcuts import redirect

from picturehunt.models import Clue, User, Path, Team


def next_clue(team):
    old_clue = team.current_clue
    if old_clue:
        old_clue_index = old_clue.order_index
        segment = old_clue.segment
    else:
        old_clue_index = -1
        segment = team.path.segment_order.first().segment
    next_clues = Clue.objects.filter(order_index__gt=old_clue_index, segment=segment).order_by('order_index')

    if len(next_clues) > 0:  # Clues left in this segment
        return next_clues[0]
    else:  # Start next segment
        path = team.path
        old_segment = old_clue.segment
        old_segment_index = path.segment_order.get(segment=old_segment).index

        next_segment_orders = path.segment_order.filter(index__gt=old_segment_index).order_by('index')

        if len(next_segment_orders) > 0:
            new_segment_order = next_segment_orders[0]
            clues = new_segment_order.segment.clues.all().order_by('order_index')
            return clues[0]
        else:
            return None


def index(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect(login)

    user = User.objects.get(id=user_id)

    if request.method == "POST":
        solution = request.POST.get("solution")
        if solution.lower() == user.current_team.current_clue.solution.lower():
            new_clue = next_clue(user.current_team)
            user.current_team.current_clue = new_clue
            user.current_team.save()
            return render(request, "index.html", {'clue': new_clue})
    else:
        clue = user.current_team.current_clue
        return render(request, "index.html", {'clue': clue})


def login(request):
    if request.method == "POST":
        default_path = random.choice(Path.objects.all())

        team, created_team = Team.objects.get_or_create(name=request.POST.get("team"), defaults={'path': default_path})
        user, created = User.objects.get_or_create(name=request.POST.get("name"), current_team=team, defaults={'logged_in': True})

        user.logged_in = True
        user.save()

        if created_team:
            team.current_clue = next_clue(team)
            team.save()

        request.session["user_id"] = user.id
        request.session["user_name"] = user.name
        request.session["team_name"] = user.current_team.name
        return redirect(index)

    users = User.objects.all()

    return render(request, "login.html", {"users": users})


def logout(request):
    user = User.objects.get(id=request.session["user_id"])
    user.logged_in = False
    user.save()

    del request.session["user_id"]
    del request.session["user_name"]
    del request.session["team_name"]
    return redirect(login)

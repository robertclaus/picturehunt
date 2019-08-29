from datetime import datetime
import random

from django.shortcuts import render
from django.shortcuts import redirect

from picturehunt.models import Clue, User, Path, Team, CompletedClue


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
    try:
        user = User.objects.get(id=user_id)
    except Exception:
        return redirect(logout)

    if request.method == "POST":
        solution = request.POST.get("solution")
        is_correct = solution.lower().lstrip().rstrip() in user.current_team.current_clue.solution.lower().split(";")

        CompletedClue.objects.create(
            clue=user.current_team.current_clue,
            team=user.current_team,
            time=datetime.now(),
            guess=solution,
            correct=is_correct,
        )

        if is_correct:
            new_clue = next_clue(user.current_team)
            user.current_team.current_clue = new_clue
            user.current_team.save()
            return render(request, "index.html", {'clue': new_clue, 'message': 'Congratulations, here is your next clue!'})
        else:
            return render(request, "index.html", {'clue': user.current_team.current_clue, 'message': 'That solution was not correct.'})
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
    try:
        user = User.objects.get(id=request.session["user_id"])
        user.logged_in = False
        user.save()
    except Exception:
        pass

    del request.session["user_id"]
    del request.session["user_name"]
    del request.session["team_name"]
    return redirect(login)

def dashboard(request):
    user_id = request.session.get("user_id")
    if not user_id:
        return redirect(login)
    try:
        user = User.objects.get(id=user_id)
    except Exception:
        return redirect(logout)

    if not user.is_admin:
        return redirect(index)

    teams = Team.objects.all()

    context = {'team_context': []}

    for team in teams:

        team_member_names = list(team.user_set.all().value_list('name', flat=True))

        current_clue = team.current_clue
        current_guesses = CompletedClue.objects.all().filter(team=team, clue=current_clue).count()
        time_to_clue = datetime.now() - CompletedClue.objects.all().latest('time').time
        next_clue = next_clue(current_clue)

        #previous_clue = previous_clue(current_clue)
        #previous_guesses = CompletedClue.objects.all().filter(team=team, clue=previous_clue).count()

        team_context = {
            'name': team.name,
            'team_member_names': team_member_names,
            'current_clue': current_clue,
            'next_clue': next_clue,
            'current_question': current_clue.question,
            'current_solution': current_clue.solution,
            'current_image': current_clue.img_content,
            'current_guesses': current_guesses,
            'time_to_clue': time_to_clue,
            'next_image': next_clue.img_content,

        }
        context['teams'].append(team_context)

    render(request, "dashboard.html", context)

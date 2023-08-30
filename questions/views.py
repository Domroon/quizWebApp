import random

from django.shortcuts import render, get_list_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User

from .models import Question, Round, Statistic


def index(request):
    question_list = get_list_or_404(Question)
    return HttpResponse(f'Total amount of stored Questions: {len(question_list)}')


def get_random_questions(questions, qty, playing_user, topic=None):
    search_limit = qty * 10
    random_questions = set()
    loop_count = 0
    while True:
        if len(random_questions) == qty:
            break
        if loop_count >= search_limit:
            break
        random_num = random.randint(0, len(questions)-1)
        question = questions[random_num]
        already_asked = False
        for user in question.already_asked.all():
            if playing_user.id == user.id:
                already_asked = True
                print("Question: ", question)
                print("playing_user.id: ", playing_user.id)
                print("user.id: ", user.id)
                print()
                break
        if already_asked:
            loop_count += 1
            continue
        if topic:
            if topic != question.topic:
                loop_count += 1
                continue
        random_questions.add(question)
        question.already_asked.add(playing_user)
        question.save()
    return random_questions
        

# choose modus and start quiz
def round_menu(request):
    # get modus (M or T) from Form via POST Request
    modus = "M"
    questions = get_list_or_404(Question)
    # get logged in user
    user = User.objects.get(username='domroon')
    random_questions = get_random_questions(questions, 5, user)
    statistic = Statistic()
    statistic.save()
    user_round = Round(modus=modus, user=user, statistic=statistic)
    user_round.save()
    for question in random_questions:
        user_round.questions.add(question)
    user_round.save()
    return redirect('questions:round')
    
    # when no POST-Request happens do this:
    return HttpResponse(f'In Round Menu')


def round(request):
    # get logged in user!!!
    user = User.objects.get(username='domroon')
    user_round = Round.objects.filter(user__id=user.id).order_by("-created_at")[0]
    questions = user_round.questions.all()
    question_num = user_round.statistic.answered_questions_count
    if question_num == len(questions):
        return HttpResponse("All questions are answered. Redirect to final result")
    question = questions[question_num]
    user_round.statistic.answered_questions_count = question_num + 1
    # check if the answer is correct
    # if the answer is correct: +1 to right_answers count
    user_round.statistic.save()
    return HttpResponse(question)


def result(request):
    # get logged in user!!!
    user = User.objects.get(username='domroon')
    user_round = Round.objects.filter(user__id=user.id).order_by("-created_at")[0]
    questions = user_round.questions.all()
    question_num = user_round.statistic.answered_questions_count


def final_result(request):
    pass


def statistics(request):
    # search all statistic rows for a user and 
    # add all answered_question_count and 
    # right_answers together
    pass


def user_settings(request):
    pass


def questions_editor(request):
    pass


def login(request):
    pass


def logout(request):
    pass
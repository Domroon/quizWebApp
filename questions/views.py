import random

from django.shortcuts import render, get_list_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User

from .models import Question, Round, Statistic, BasicAnswer


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
    # get logged in user
    user = User.objects.get(username='domroon')
    questions = get_list_or_404(Question)
    random_questions = get_random_questions(questions, 5, user)
    user_round = Round(modus=modus, user=user)
    user_round.save()
    for question in random_questions:
        user_round.questions.add(question)
    user_round.save()
    return redirect('questions:round')
    
    # when no POST-Request happens do this:
    return HttpResponse(f'In Round Menu')


# USE ANSWER IDs damit man antworten vergleichen kann
# durch auswahl des users im UI erzeugt dieser ein answer objekt 
# anhand der id, welche im form-field mitgeliefert wird
# NEIN besser nur die id im UI, KEIN Objekt erstellen 
# sondern anhand der answer-ID aus dem form-UI nach answer suchen
# zu jeder ID wird true/false oder ein antwort-text geliefert!
def check_answer(user, question, user_answer_ids):
    db_answers = BasicAnswer.objects.filter(question=question)
    answer_correct = False
    if question.question_type == "TR":
        # only one answer in db_answers and user_answer_ids with true or false
        if db_answers[0].is_true == user_answer_ids[db_answers[0].id]:
            answer_correct = True
    elif question.question_type == "MU":
        for db_answer in db_answers:
            answer_correct = True
            if db_answer.is_true != user_answer_ids[db_answer.id]:
                answer_correct = False
    elif question.question_type == "SI":
        for db_answer in db_answers:
            if db_answer.is_true:
                if user_answer_ids[db_answer.id] == True:
                    answer_correct = True
    elif question.question_type == "TE":
        db_answer = db_answer[0]
        if db_answer.answer_text == user_answer_ids[db_answer.id]:
            answer_correct = True 
    statistic = Statistic(question=question, user=user, right_answered=answer_correct)
    statistic.save()


def round(request):
    # get logged in user!!!
    user = User.objects.get(username='domroon')
    user_round = Round.objects.filter(user__id=user.id).order_by("-created_at")[0]
    questions = user_round.questions.all()
    question_num = user_round.answered_questions_count
    if question_num == len(questions):
        user_round.completed = True
        user_round.save()
        return HttpResponse("All questions are answered. Redirect to final result")
    question = questions[question_num]
    if request.method == "POST":
        data = request.POST
        user_answer_ids = data.get("user_answer_ids")
        check_answer(user, question, user_answer_ids)
        user_round.answered_questions_count = question_num + 1
        user_round.save()

    # TEST
    # user = User.objects.get(username='domroon')
    # question = Question.objects.get(id=1)
    # user_answer_ids = {
    #     1 : False,
    #     2 : True,
    #     3 : False,
    #     4 : False,
    # }
    # check_answer(user, question, user_answer_ids)

    return HttpResponse(question)


def result(request):
    # get logged in user!!!
    user = User.objects.get(username='domroon')
    user_round = Round.objects.filter(user__id=user.id).order_by("-created_at")[0]
    latest_stat = Statistic.objects.filter(user__id=user.id).order_by("-created_at")[0]
    questions = user_round.questions.all()
    
    return HttpResponse(f'{latest_stat.question.question_text} - right_answered: {latest_stat.right_answered}') 


def final_result(request):
    # get logged in user!!!
    user = User.objects.get(username='domroon')
    last_user_round = Round.objects.filter(user__id=user.id).order_by("-created_at")[0]
    if not last_user_round.completed:
        return redirect('questions:round')
    total_questions = len(last_user_round.questions.all())
    right_questions_counter = 0
    for question in last_user_round.questions.all():
        statistic = Statistic.objects.get(question__id=question.id, user__id=user.id)
        if statistic.right_answered:
            right_questions_counter += 1

    return HttpResponse(f'Question Count: {total_questions} - Right Questions: {right_questions_counter}')


def user_statistic(request):
    # get logged in user!!!
    user = User.objects.get(username='domroon')
    rounds = Round.objects.filter(user=user)
    # questions = Question.objects.filter(already_asked=user)
    statistic = Statistic.objects.filter(user=user)
    answered_questions = Question.objects.filter(already_asked=user)

    played_rounds = len(rounds)
    total_answered_questions = len(statistic)
    total_right_questions = len(statistic.filter(right_answered=True))
    geography_count = len(answered_questions.filter(topic="GE"))
    entertainment_count = len(answered_questions.filter(topic="EN"))
    history_count = len(answered_questions.filter(topic="HI"))
    art_lit_count = len(answered_questions.filter(topic="AL"))
    sci_tech_count = len(answered_questions.filter(topic="ST"))
    sp_pl_count = len(answered_questions.filter(topic="SP"))

    return HttpResponse(f'played rounds: {played_rounds} - total_answered_quesitions: {total_answered_questions}')
    

def total_statistic(request):
    # for all questions
    # total questions count
    # questions count per topic
    # questions count per type
    # total registered users count
    # answered questions
    # right answered questions
    return


def user_settings(request):
    pass


def questions_editor(request):
    # paginator necessary
    pass


def login(request):
    pass


def logout(request):
    pass
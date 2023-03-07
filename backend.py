import csv, os, fnmatch, random, json
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)

birds_img_list = fnmatch.filter(os.listdir('static/birds'), '*.jpg')
birds_list = [x.split(".")[0] for x in birds_img_list]

mammals_img_list = fnmatch.filter(os.listdir('static/mammals'), '*.jpg')
mammals_list = [x.split(".")[0] for x in mammals_img_list]

frogs_img_list = fnmatch.filter(os.listdir('static/frogs'), '*.jpg')
frogs_list = [x.split(".")[0] for x in frogs_img_list]

insects_img_list = fnmatch.filter(os.listdir('static/insects'), '*.jpg')
insects_list = [x.split(".")[0] for x in insects_img_list]

animals_done = []

def make_fact_dict():
    f_dict = {}
    with open('facts.csv', encoding='utf8') as csvfile:
        reader = csv.reader(csvfile, delimiter="|")
        for row in reader:
            f_dict[row[0]] = row[1]
    return f_dict

# fact_dict = make_fact_dict()
# print(fact_dict)

def get_animals(animals_list):
    global animals_done
    # print(animals_done)
    sampled_animals = random.sample(animals_list, 3)
    option1 = sampled_animals[0]
    option2 = sampled_animals[1]
    option3 = sampled_animals[2]
    answer = random.choice(sampled_animals)
    while answer in animals_done:
        sampled_animals = random.sample(animals_list, 3)
        option1 = sampled_animals[0]
        option2 = sampled_animals[1]
        option3 = sampled_animals[2]
        answer = random.choice(sampled_animals)
    return option1, option2, option3, answer

@app.route("/", methods=('GET', 'POST',))
def menu():
    if request.method == 'POST':
        no_rounds = int(request.form['rounds'])
        return redirect(url_for('game', num_rounds=no_rounds, curr_round=1, score=0))
    return render_template("menu.html")

@app.route("/game/<int:num_rounds>/<int:curr_round>/<int:score>", methods=('GET', 'POST',))
def game(num_rounds, curr_round, score=0):
    global animals_done
    # print("entered game")
    if request.method == 'POST':
        chosen = request.form['options']
        ans = request.form['answer']
        if chosen == ans:
            score += 1
        curr_round += 1
        return redirect(url_for('game', num_rounds=num_rounds, curr_round=curr_round, score=score))
    if curr_round <= num_rounds:
        ch = random.randint(0, 3)
        if ch == 0:
            option1, option2, option3, answer = get_animals(birds_list)
            sampled_folder = 'birds'
        elif ch == 1:
            option1, option2, option3, answer = get_animals(mammals_list)
            sampled_folder = 'mammals'
        elif ch == 2:
            option1, option2, option3, answer = get_animals(frogs_list)
            sampled_folder = 'frogs'
        else:
            option1, option2, option3, answer = get_animals(insects_list)
            sampled_folder = 'insects'
        animals_done.append(answer)
        try:
            fact = fact_dict[answer]
        except:
            fact = " "
        return render_template("game.html", sampled_folder=sampled_folder, option1=option1, option2=option2, option3=option3, answer=answer, curr_round=curr_round, rounds=num_rounds, score=score, fact=fact)
    else:
        animals_done = []
        return render_template("game_over.html", score=score)

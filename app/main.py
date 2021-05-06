#!/usr/bin/python3
"""
The following script is based on
* [https://github.com/stg7/bottle_docker_kit](https://github.com/stg7/bottle_docker_kit)
* [https://github.com/Telecommunication-Telemedia-Assessment/avrateNG](https://github.com/Telecommunication-Telemedia-Assessment/avrateNG)
"""
import json
import logging
import os
import sys
import glob
import random
import datetime
import time

import bottle
from bottle import Bottle
from bottle import auth_basic
from bottle import route
from bottle import run
from bottle import install
from bottle import template
from bottle import request
from bottle import redirect
from bottle import response
from bottle import error
from bottle import static_file
from bottle_sqlite import SQLitePlugin
from bottle_config import ConfigPlugin

app = application = bottle.Bottle()


def check_credentials(username, password):
    config = ConfigPlugin._config
    validName = config["http_user_name"]
    validPassword = config["http_user_password"]
    return password == validPassword and username == validName


@app.route('/stats')
@auth_basic(check_credentials)
def stats(config, db):
    '''
    Show some test statitics, not sure if this works if there are only a few ratings
    '''
    if not db.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='ratings'").fetchone():
        return "no stats to show"

    max_id = int(db.execute('select max(user_ID) from ratings').fetchone()[0])
    total_ratings = int(db.execute('select count(*) from ratings where rating <> -1').fetchone()[0])
    num_users = int(db.execute('select count(distinct(user_id)) from ratings where rating <> -1').fetchone()[0])
    average_rating_count = float(db.execute('select avg(c) from (select count(*) as c from (select * from ratings where rating <> -1) group by stimuli_file)').fetchone()[0])

    # create the rating count data
    hist = {}
    for row in db.execute('select c, count(c) as h from (select count(*) as c from ratings group by stimuli_file) group by c'):
        hist[row["c"]] = row["h"]

    # can be used instead of the hist_dia
    hist_str = json.dumps(hist, indent=4, sort_keys=True)

    hist_dia = ""
    for k in sorted(hist.keys()):
        hist_dia += f"{k:>3d}: {hist[k]*'#'} : {hist[k]} \n"

    return f"""<pre>
stats:
    max_id = {max_id}
    users_who_rated = {num_users}
    total_ratings = {total_ratings}
    average ratings per stimuli_file = {average_rating_count}

</pre>"""
#     rating count hist per stimuli_file:
# {hist_dia}

@app.error(404)
def error404(error):
    return 'he is dead jim'


@app.route('/static/<filename:path>')
def static(filename):
    '''
    Serve static files
    '''
    return bottle.static_file(filename, root='./static')


@app.route('/stimuli/<filename:path>')
def static(filename):
    '''
    Serve stimuli files
    '''
    return bottle.static_file(filename, root='./stimuli')


@app.route('/train/<filename:path>')
def static(filename):
    '''
    Serve stimuli files
    '''
    return bottle.static_file(filename, root='./train')


def get_user_id_playlist(db, config):
    """ read user id from database """
    if not db.execute("SELECT * FROM sqlite_master WHERE type='table' AND name='ratings'").fetchone():
        user_id = 1 # if ratings table does not exist: first user_id = 1
    else:
        user_id = int(db.execute('SELECT max(user_ID) from ratings').fetchone()[0]) + 1  # new user_ID is always old (highest) user_ID+1

    playlist = [x for x in range(len(config["playlist"]))]
    random.shuffle(playlist)
    playlist = playlist[0:config["max_stimuli"]]

    db.execute('CREATE TABLE IF NOT EXISTS user_playlist (user_ID INTEGER PRIMARY KEY, playlist TEXT, timestamp TEXT);')
    db.execute('INSERT INTO user_playlist VALUES (?,?,?);',(user_id, json.dumps(playlist), create_timestamp()))

    # here the current user id is included in the ratings table,
    # to make sure that it is not used by anyone else
    db.execute('CREATE TABLE IF NOT EXISTS ratings (user_ID INTEGER, stimuli_ID TEXT, stimuli_file TEXT, rating_type TEXT, rating TEXT, timestamp TEXT);')
    db.execute('INSERT INTO ratings VALUES (?,?,?,?,?,?);',(user_id, -1, "", "user_registered", -1, create_timestamp()))
    db.commit()


    return user_id, playlist


@app.route('/questionair')
def questionair(config, db):
    """
    show demographics_form if required
    """
    check_if_test_was_done_already(request, config)
    user_id, playlist = get_user_id_playlist(db, config)

    response.set_cookie("user_id", str(user_id), path="/")
    response.set_cookie("stimuli_done", "0", path="/")
    response.set_cookie("session_state", "0", path="/")
    response.set_cookie("training_done", "0", path="/")

    return template(
        config["template_folder"] + "/questionair.tpl",
        title=config["title"],
        stimuli=[config["playlist"][x] for x in playlist],
        dev=request.get_cookie("dev") == "1"
    )



@app.route('/questionair', method='POST')
def questionair(db, config):
    """
    saves questionair info into sqlite3 table,
    all user information (user_id is key in tables) are stored as JSON string
    """
    user_id = int(request.get_cookie("user_id"))

    db.execute('CREATE TABLE IF NOT EXISTS questionair (user_ID INTEGER PRIMARY KEY, answers_json TEXT);')
    db.execute('INSERT INTO questionair VALUES (?,?);',(user_id, json.dumps(dict(request.forms))))
    db.commit()

    redirect('/instructions')


@app.route('/instructions')
def instructions(config, db):
    check_if_test_was_done_already(request, config)
    user_id, playlist = get_user_id_playlist(db, config)

    return template(
        config["template_folder"] + "/instructions.tpl",
        title=config["title"],
        stimuli=[config["playlist"][x] for x in playlist]
    )


@app.route('/about')
def about(config, db):
    return template(
        config["template_folder"] + "/about.tpl",
        title=config["title"]
    )


@app.route('/start_test')
def start_test(config, db):
    check_if_test_was_done_already(request, config)
    user_id, playlist = get_user_id_playlist(db, config)

    return template(
        config["template_folder"] + "/start_test.tpl",
        title=config["title"],
        stimuli=[config["playlist"][x] for x in playlist]
    )


@app.route('/training/<stimuli_idx>')
@app.route('/training/<stimuli_idx>', method="POST")
def training(config, db, stimuli_idx):

    check_if_test_was_done_already(request, config)
    user_id = int(request.get_cookie("user_id"))
    stimuli_idx = int(stimuli_idx)

    if len(config["training"]) == 0:
        #TODO redirect
        redirect('/rate/0')
        return
    if stimuli_idx >= len(config["training"]):
        redirect('/start_test')
        return
    return bottle.template(
        config["template_folder"] + "/rate.tpl",
        title=config["title"],
        train=True,
        rating_template=config["rating_template"],
        stimuli_done=stimuli_idx,
        stimuli_idx=stimuli_idx,
        stimuli_file=config["training"][stimuli_idx],
        stimuli_count=len(config["training"]),
        user_id=user_id,
        dev=request.get_cookie("dev") == "1"
    )


@app.route('/rate/<stimuli_idx>')  # Rating screen with stimuli_idx as variable
def rate(db, config, stimuli_idx):
    """
    show rating screen for one specific stimuli
    """
    check_if_test_was_done_already(request, config)
    stimuli_done = int(request.get_cookie("stimuli_done"))

    user_id = int(request.get_cookie("user_id"))
    session_state = int(request.get_cookie("session_state"))

    playlist = json.loads(db.execute("SELECT playlist FROM user_playlist WHERE user_ID=?", (user_id,)).fetchone()["playlist"])

    stimuli_idx = playlist[stimuli_done]

    return bottle.template(
        config["template_folder"] + "/rate.tpl",
        title=config["title"],
        rating_template=config["rating_template"],
        stimuli_done=stimuli_done,
        stimuli_idx=stimuli_idx,
        stimuli_file=config["playlist"][stimuli_idx],
        stimuli_count=config["max_stimuli"],
        user_id=user_id,
        dev=request.get_cookie("dev") == "1"
    )


@app.route('/save_rating', method='POST')
def save_rating(db, config):
    """
    save rating for watched stimuli
    """
    stimuli_idx = request.query.stimuli_idx  # extract current stimuli_idx from query
    timestamp = create_timestamp()

    user_id = int(request.get_cookie("user_id"))
    stimuli_done = int(request.get_cookie("stimuli_done")) + 1
    response.set_cookie("stimuli_done", str(stimuli_done), path="/")

    # get POST data ratings and write to DB
    request_data_pairs = {}
    for item in request.forms:
        request_data_pairs[item] = request.forms.get(item)

    stimuli_ID = request_data_pairs["stimuli_idx"]
    stimuli_file = request_data_pairs["stimuli_file"]
    excluded = ["stimuli_idx", "stimuli_file"]

    db.execute('CREATE TABLE IF NOT EXISTS ratings (user_ID INTEGER, stimuli_ID TEXT, stimuli_file TEXT, rating_type TEXT, rating TEXT, timestamp TEXT);')

    for item in filter(lambda x: x not in excluded , request_data_pairs):
        db.execute(
            'INSERT INTO ratings VALUES (?,?,?,?,?,?);',
            (user_id, stimuli_ID, stimuli_file, item, request_data_pairs[item], timestamp)
        )

    db.commit()

    if stimuli_done >= config["max_stimuli"]:
        redirect('/finish')

    redirect('/rate/' + str(stimuli_done))


@app.route('/finish', method='POST')
def save_feedback(db, config):
    uuid = int(request.forms["user_id"])
    feedback = request.forms["feedback"]

    user_id = int(request.get_cookie("user_id"))
    if uuid == user_id:
        db.execute('CREATE TABLE IF NOT EXISTS feedback (user_ID INTEGER PRIMARY KEY, feedback TEXT);')
        db.execute(
            'INSERT INTO feedback VALUES (?,?);',
            (user_id, feedback)
        )
        db.commit()

    return template(
        config["template_folder"] + "/finish.tpl",
        title=config["title"],
        user_id=user_id,
        text="Thank you for participating!",
        feedback=False
    )


@app.route('/finish')
def finish(db, config):
    """
    will be shown after test was completly done
    """
    done = request.get_cookie("test_done") == config["cookie_secret"]
    response.set_cookie("test_done", config["cookie_secret"], path="/")

    user_id = int(request.get_cookie("user_id"))
    db.execute('INSERT INTO ratings VALUES (?,?,?,?,?,?);',(user_id, -1, "", "user_done", -1, create_timestamp()))
    db.commit()

    return template(
        config["template_folder"] + "/finish.tpl",
        title=config["title"],
        user_id=user_id,
        text="Thank you for participating!" if not done else "You already attended this test, thank you!",
        feedback=True
    )


def check_if_test_was_done_already(request, config):
    """
    checks if test was done,
    to force that someone can do the test again change
    config["cookie_secret"]
    """
    if request.get_cookie("test_done") == config["cookie_secret"]:
        redirect('/finish')


@app.route('/')
def main(db, config):
    """
    The front welcome page
    """
    check_if_test_was_done_already(request, config)

    return bottle.template(
        config["template_folder"] + "/welcome.tpl",
        title=config["welcome_msg"],
        training=config["do_training"]
    )


@app.route('/reset_cookies')
@app.route('/rc')
def reset_cookies(db, config):
    """
    perfrom a reset of the cookies, this is only for internal usage,
    in case avrateNG needs to be resetted
    """
    for cookie in request.cookies:
        response.set_cookie(cookie, '', expires=0)
    redirect('/')


@app.route('/dev')
def dev(db, config):
    """
    perfrom a reset of the cookies, this is only for internal usage,
    in case avrateNG needs to be resetted
    """
    response.set_cookie("dev", "1", path="/")
    redirect('/')


class StripPathMiddleware(object):
    def __init__(self, app):
        self.app = app
    def __call__(self, e, h):
        e['PATH_INFO'] = e['PATH_INFO'].rstrip('/')
        return self.app(e, h)


def create_timestamp():
    return str(datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S %f'))  # define timestamp


def read_file(x):
    """ read a file """
    with open(x) as xfp:
        return "".join(xfp.readlines())


def setup():
    """ read config and register plugins """
    this_path = os.path.dirname(os.path.realpath(__file__))
    try:
        config = json.loads(read_file(this_path + "/config.json"))
    except Exception as e:
        logging.error("configuration file 'config.json' is corrupt (not json conform). Error: " + str(e))
        sys.exit(-1)
    config["template_folder"] = "./templates"

    config["playlist"] = sorted(list(glob.glob("./stimuli/*")))
    config["training"] = sorted(list(glob.glob("./train/*")))
    config["do_training"] = len(config["training"]) > 0

    print(f"""training: {config["do_training"]}; {len(config["training"])}""")
    print(f"""stimuli: {len(config["playlist"])}""")

    if "max_stimuli" not in config or config["max_stimuli"] > len(config["playlist"]):
        config["max_stimuli"] = len(config["playlist"])

    app.install(SQLitePlugin(
            dbfile=os.path.join(
                os.path.dirname(__file__),
                'ratings.db'
            )
        )
    )
    app.install(ConfigPlugin(config))


def run_local_server():
    """ run local development server """
    bottle.run(
        app=StripPathMiddleware(app),
        host='0.0.0.0',
        port=8081,
        debug=True,
        reloader=True
    )


# add additional modules and read config
setup()

if __name__ == '__main__':
    run_local_server()



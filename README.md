# AvrateVoyager

AvrateVoyager is an online based image/video/audio quality testing framework.
The docker part is based on [bottle_docker_kit](https://github.com/stg7/bottle_docker_kit).
The rating part is based on [avrateNG](https://github.com/Telecommunication-Telemedia-Assessment/avrateNG).
If you want to perform a lab test, then you should use [avrateNG](https://github.com/Telecommunication-Telemedia-Assessment/avrateNG).
The core idea of AvrateVoyager is to playout the stimuli within a webbrowser and this creates limitations for the 


## Requirements
* linux based system with docker and docker-compose installed
* for local development and export scripts you need python3 with numpy and pandas 


## Preparation
Before you can perform your test some steps are required.
The template syntax used is SimpleTemplate Engine, please checkout their [guide](https://bottlepy.org/docs/dev/stpl.html).

### General config
The main config for the test system can be adapted in `app/config.json`:

```
{
    "welcome_msg": "video quality",  // welcome message used in the welcome screen
    "rating_template": "rating/acr.tpl", // used template for rating
    "title": "video quality", // page title
    "max_stimuli": 150,  // in case you have more than max_stimuli files only max_stimuli files are presented to a participant
    "cookie_secret": "x-files-forever",  // cookie to check whether the test has been done already
    "http_user_name": "stg7",  // username for the /stats route
    "http_user_password": "test" // password for the /stats route
}
```


### Start page
For your specific test you should adapt the start page, so change the test in the `app/templates/welcome.tpl` file.

### Questionnaire
The first page after the welcome page is the questionnaire, here questions regarding the background of the participant are collected.
The questions can be adapted in the file `app/templates/questionnaire.tpl`, there are already examples provided, e.g. adapt the given question array to your needs.
```python
questions = [
    {
        'type': 'choice', 
        'question': 'What is your age?', 
        'qkey': 'user_age_range', 
        'options': 
                [
                    '', 
                    '< 18', 
                    '18 to 24', 
                    '25 to 29', 
                    '30 to 39', 
                    '40 to 49', 
                    '50 to 59', 
                    '60 to 69', 
                    '70+'
                ]
    },
    ....
]

```
`choice` and `input` fields are currently supported, important is that you define a unique `qkey`.
`qkey` is used to store the result of the question.



### Instructions
Please change the instructions according to your test design, see template file `app/templates/instructions.tpl`.

On the questionnaire and instructions pages the stimuli for the user are precached to avoid loading during the conduction of the test, however this must be checked and verified and can result in long loading times for these pages.

The test system continues either with the training or rating.
Training is performed in case you have training files in the `app/train` folder, otherwise it will be skipped.


### Rating template
The rating template consists of two parts,
the first part is the presentation of the stimuli `app/templates/stimuli.tpl`, and the second part is the rating method.

The `app/templates/stimuli.tpl` template is currently only for audio and video files, thus for images adaption are required.
Adaption for video and audio tests are still required for the template, depending on the specific test design, e.g. playing the video in full screen or with a fixed resolution.


The rating method is defined using the `app/config.json` file, modify the key `rating_template`.
Currently only `rating/multi_slider.tpl` and `rating/acr.tpl` are supported.

* `rating/multi_slider.tpl`: implements several slides for rating, just for demonstration
* `rating/acr.tpl`: implements ACR rating scale



### Stimuli files
All videos/image/audio files in the folder `app/stimuli` are used in the test.
In case you add files to the `app/train` folder a training (where the results are not stored) with the files in this folder is performed before the tests starts.


## Start (for development)

Build the docker container with
```bash
docker build -t avrateVoyager .
```

Afterwards, you can run the service with
```bash
docker-compose up -d
```

Now your web-server is running at [http://localhost:8080](http://localhost:8080), remove `-d` flag for a non permanent service.

In case you have python and the required libraries installed you can also run `app/main.py` directly without docker, this approach is just recommended for development.

## General online test hints
* make sure the videos play with firefox and chrome, consider that most participants will not have high end equipment
* try to reduce the overall file size of all stimuli, e.g. approx 500MB for 180 stimuli where only 30 were asked per participant was ok in some of our tests


## Behind the scene tricks
In case you want to perform a test run in the system without filling the forms, open `<baseurl>/dev` before, in most of the templates a second submission button will be shown which now enables you to skip the filling of the forms.

To see some basic statistics of your currently running test you can open `<baseurl>/stats` and login with the specified password and username in the `config.json`.

If you want to redo the test or had some other troubles, a simple `<baseurl>/rc` will reset the cookies that prevent you from doing the test again.

These magic routes should be removed/disabled for a production environment.


# Production deployment
Use the docker-compose approach to get the services started.

Default settings are performing python autoload, thus the service will reload in case the `main.py` is changed.
For a production setup this should be changed (check `app/uwsgi.ini` and comment `py-autoreload = 2` line).
In addition for a real production system HTTPS is recommended, here [caddyserver](https://caddyserver.com/) could be used with e.g. a configuration `Caddyfile` in the following way:
```
your.test.domain.name {
    reverse_proxy 127.0.0.1:<PORT>
}
```
where `<PORT>` is the configured port in the `docker-compose.yml` file of AvrateVoyager, the default value is 8080.
You should further check the firewall settings on the production server.


## Developers
* [Steve Göring](https://github.com/stg7)

If you like this software you can also [donate me a :coffee:](https://ko-fi.com/binarys3v3n)

## Contributors
* Maximilian Schaab
* Serge Molina
* Anton Schubert
* John Dumke and Margaret Pinson (questionnaire form)


## Acknowledgments
If you use this software in your research, please include a link to the repository and reference one of the following paper.

```
@inproceedings{rao2021crowd,
  title={Towards High Resolution Video Quality Assessment in the Crowd},
  author={Rakesh {Rao Ramachandra Rao} and Steve G\"oring and Alexander Raake},
  booktitle={Thirteenth International Conference on Quality of Multimedia Experience (QoMEX)},
}

@inproceedings{goering2021voyager,
  title={AVRate Voyager: an open source online testing platform},
  author={Steve G\"oring and Rakesh {Rao Ramachandra Rao} and Alexander Raake},
  booktitle={MMSP},
  note={under review}
}
```

## License
GNU General Public License v3. See [LICENSE](LICENSE) file in this repository.


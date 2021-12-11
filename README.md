# Timetrack

A simple tool for creating reports from tracking time in Google calendar. It is
inspired by the Google Sheet extension 
[TimeSheet](https://workspace.google.com/u/0/marketplace/app/timesheet/6002835623).
I wanted to have a more flexible approach which can be run every week and send
a report to my email. Is it a good idea to use Google calendar for time 
tracking? Probably not, but it works fine for me.

## Setup

First you need to create an OAuth 2.0 app in the 
[Google API Console](https://console.developers.google.com/). See this 
[documentation](https://developers.google.com/identity/protocols/oauth2)
for details. 

Now clone this repository using `git clone`.

### Using the source code

Make sure you have all dependencies installed:
```bash
pip install -r requirements.txt
```

Run the command using
```bash
python -m timetrack
```

### Using pip

Run `pip install .` in the root directory of this repository. Now you should be 
able to call this program using the `timetrack` command. The configuration is 
done using environment variables (see below).

### docker

1. Build this image by running following command:
```bash
$ docker build -t timetrack .
```
2. List all calendar ids you have access to:
```bash
$ docker run -it --rm --name timetrackcontainer \
  -e GOOGLE_CLIENT_ID=XXX \
  -e GOOGLE_CLIENT_SECRET=XXX \
  -e GOOGLE_PROJECT_ID=XXX \
  timetrack calendar
```
See below for which environment variables you can set.

3. If you know the IDs of the calendars you can run 
```bash
$ docker run -it --rm --name timetrackcontainer \
  -e GOOGLE_CLIENT_ID=XXX \
  -e GOOGLE_CLIENT_SECRET=XXX \
  -e GOOGLE_PROJECT_ID=XXX \
  -e CALENDAR_TRACK=XXX \
  -e CALENDAR_WORKTIME=XXX \
  -v $(pwd)/data:/data \
  timetrack report 2021-11-01 2021-11-01 2021-12-01 /data/report.html
```
See below for which cli parameters you can set or run the command with `--help`.
The generated report will be placed in the `data` directory.

### docker-compose
Modify the `docker-compose.yml` according to your needs.

Run the script using `docker-compose run timetrack --help`

For example: `docker-compose run timetrack report 2021-11-01 2021-11-01 2021-12-01 /data/report.html`

## Configuration

The configuration is done using environment variables. If you use a shell you
can set them using `VARIABLE=VALUE`.

| Variable                      | Default                                    | Description                                                                                                             |
|-------------------------------|--------------------------------------------|-------------------------------------------------------------------------------------------------------------------------|
| GOOGLE_CLIENT_ID              |                                            | Project client id retrieved from Google API console                                                                     |
| GOOGLE_PROJECT_ID             |                                            | Project id retrieved from Google API console                                                                            |
| GOOGLE_AUTH_URL               | https://accounts.google.com/o/oauth2/auth  |                                                                                                                         |
| GOOGLE_TOKEN_URI              | https://oauth2.googleapis.com/token        |                                                                                                                         |
| GOOGLE_AUTH_PROVIDER_CERT_URL | https://www.googleapis.com/oauth2/v1/certs |                                                                                                                         |
| GOOGLE_CLIENT_SECRET          |                                            | Project client secret retrieved from Google API console                                                                 |
| GOOGLE_REDIRECT_URI           | http://localhost                           |                                                                                                                         |
| CALENDAR_TRACK                |                                            | Calendar ids separated by commas which contain the events which will be considered as tracked time                      |
| CALENDAR_WORKTIME             |                                            | Calendar ids separated by commas which contain the events which will be considered as expected working hours (optional) |
| TOKEN_FILE                    | current working directory                  | Place where the oauth token will be stored.                                                                             |
If you just want to sum up your tracked time, you do not need to provide 
CALENDAR_WORKTIME. It's only necessary if you want to check your overtime.

## Command line options

There are two commands `calendar` and `report`. `calendar` has no options and 
will just list all calendar ids.

`report` has more options and will be used to generate an HTML report containing
all tracked times.

```bash
$ timetrack report --help
usage: __main__.py report [-h]
                          [--plot-daily {tracked_time,tracked_time_sum,working_time,overtime,overtime_sum}]
                          [--plot-weekly {tracked_time,tracked_time_sum,working_time,overtime,overtime_sum}]
                          [--plot-monthly {tracked_time,tracked_time_sum,working_time,overtime,overtime_sum}]
                          [--title TITLE]
                          start view-start view-end outfile

positional arguments:
  start                 retrieve events from Google calendar starting with
                        this date. Fo rmat YYYY-MM-DD (e.g. 2021-12-24)
  view-start            only include events after (>=, including) this event
                        in the repo rt. Format YYYY-MM-DD (e.g. 2021-12-24)
  view-end              only include events before (<=, including) this event
                        in the rep ort. Format YYYY-MM-DD (e.g. 2021-12-25)
  outfile               file report is written to

optional arguments:
  -h, --help            show this help message and exit
  --plot-daily {tracked_time,tracked_time_sum,working_time,overtime,overtime_sum}
  --plot-weekly {tracked_time,tracked_time_sum,working_time,overtime,overtime_sum}
  --plot-monthly {tracked_time,tracked_time_sum,working_time,overtime,overtime_sum}
  --title TITLE         report title

```

## License

This project is licensed under the AGPLv3. See `LICENSE` for details.
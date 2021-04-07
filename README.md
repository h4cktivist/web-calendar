# web-calendar

### :date: Simple RESTful Web Calendar made on Python with Flask framework by [JetBrains Academy's Python Developer course](https://hyperskill.org/tracks/2)

## With this app you can:
1. Create new event in your calendar (by POST on `/event`)
2. Get all events or just single event by it's ID (by GET on `/event` or `/event/id` for single)
3. Get all events by date range (by set params `start_time` and `end_time` to `/event`)
4. Get all todays events (by GET on `/event/today`)
5. Delete single event using it's ID (by DELETE on `/event/id`)

## Install
```sh
git clone https://github.com/h4cktivist/web-calendar.git
cd web-calendar
pip install -r requirements.txt
```

## Run
```sh
cd web-calendar
python app.py
```
or just (if Python is added to your PATH)
```sh
cd web-calendar
app.py
```

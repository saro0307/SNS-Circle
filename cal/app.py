from flask import Flask, render_template
import calendar
from datetime import datetime

app = Flask(__name__)

@app.route('/')
@app.route('/<int:year>/<int:month>')
def index(year=None, month=None):
    if year is None or month is None:
        now = datetime.now()
        year = now.year
        month = now.month
    calendar_html = generate_calendar(year, month)
    return render_template('index.html', calendar_html=calendar_html, year=year, month=month)

def generate_calendar(year, month):
    cal = calendar.HTMLCalendar(calendar.SUNDAY)
    return cal.formatmonth(year, month)

if __name__ == '__main__':
    app.run(debug=True)

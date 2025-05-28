import argparse
import sqlite3
from datetime import datetime, timedelta
import os

DB_PATH = 'attendance.db'
TABLE_SCHEMA = '''\
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    start_time TEXT NOT NULL,
    end_time TEXT
)
'''

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.execute(TABLE_SCHEMA)
    return conn

def clock_in():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT * FROM attendance WHERE end_time IS NULL')
    if cur.fetchone() is not None:
        print('Already clocked in')
        return
    now = datetime.now().isoformat()
    cur.execute('INSERT INTO attendance(start_time) VALUES (?)', (now,))
    conn.commit()
    print(f'Clocked in at {now}')


def clock_out():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT id,start_time FROM attendance WHERE end_time IS NULL')
    row = cur.fetchone()
    if row is None:
        print('Not currently clocked in')
        return
    now = datetime.now().isoformat()
    cur.execute('UPDATE attendance SET end_time=? WHERE id=?', (now, row[0]))
    conn.commit()
    print(f'Clocked out at {now}')


def status():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT start_time FROM attendance WHERE end_time IS NULL')
    row = cur.fetchone()
    if row:
        print(f'Currently clocked in since {row[0]}')
    else:
        cur.execute('SELECT start_time,end_time FROM attendance ORDER BY id DESC LIMIT 1')
        row = cur.fetchone()
        if row:
            print(f'Last session: {row[0]} - {row[1]}')
        else:
            print('No attendance records')


def report():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute('SELECT start_time,end_time FROM attendance WHERE end_time IS NOT NULL')
    rows = cur.fetchall()
    totals = {}
    for start, end in rows:
        start_dt = datetime.fromisoformat(start)
        end_dt = datetime.fromisoformat(end)
        date = start_dt.date()
        duration = end_dt - start_dt
        totals[date] = totals.get(date, timedelta()) + duration
    for date, total in sorted(totals.items()):
        hours = total.total_seconds() / 3600
        print(f'{date}: {hours:.2f} hours')


def main():
    parser = argparse.ArgumentParser(description='Simple attendance tracker')
    parser.add_argument('command', choices=['clock-in', 'clock-out', 'status', 'report'])
    args = parser.parse_args()
    {
        'clock-in': clock_in,
        'clock-out': clock_out,
        'status': status,
        'report': report,
    }[args.command]()

if __name__ == '__main__':
    main()

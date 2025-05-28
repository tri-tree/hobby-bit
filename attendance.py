import argparse
import sqlite3
from datetime import datetime, timedelta
import os
import tkinter as tk
from tkinter import messagebox

DB_PATH = os.path.join(os.path.dirname(__file__), 'attendance.db')
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


def generate_report_string():
    """Return formatted report lines for GUI."""
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
    lines = []
    for date, total in sorted(totals.items()):
        hours = total.total_seconds() / 3600
        lines.append(f'{date}: {hours:.2f} hours')
    if not lines:
        lines.append('No attendance records')
    return '\n'.join(lines)


def create_ui():
    """Launch a simple Tkinter interface for attendance."""

    root = tk.Tk()
    root.title('Attendance Tracker')

    status_var = tk.StringVar()

    def refresh_status():
        conn = get_conn()
        cur = conn.cursor()
        cur.execute('SELECT start_time FROM attendance WHERE end_time IS NULL')
        row = cur.fetchone()
        if row:
            status_var.set(f'Clocked in since {row[0]}')
        else:
            status_var.set('Not clocked in')
        conn.close()

    def do_clock_in():
        clock_in()
        refresh_status()

    def do_clock_out():
        clock_out()
        refresh_status()

    def show_report():
        messagebox.showinfo('Report', generate_report_string())

    tk.Label(root, textvariable=status_var).pack(pady=5)
    tk.Button(root, text='Clock In', command=do_clock_in).pack(fill='x')
    tk.Button(root, text='Clock Out', command=do_clock_out).pack(fill='x')
    tk.Button(root, text='Report', command=show_report).pack(fill='x')

    refresh_status()
    root.mainloop()


def main():
    parser = argparse.ArgumentParser(description='Simple attendance tracker')
    parser.add_argument(
        'command', nargs='?', default='gui',
        choices=['clock-in', 'clock-out', 'status', 'report', 'gui'],
        help='Action to perform (default: gui)'
    )
    args = parser.parse_args()
    {
        'clock-in': clock_in,
        'clock-out': clock_out,
        'status': status,
        'report': report,
        'gui': create_ui,
    }[args.command]()

if __name__ == '__main__':
    main()

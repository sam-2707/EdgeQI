#!/usr/bin/env python3
"""Produce periodic short reports combining trainer log tail, GPU samples and ETA.
Appends to models/continuous_report.out by default (and prints to stdout).
"""
import time
import os
import sys
from datetime import datetime
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(ROOT)
TRAIN_LOG = os.path.join(ROOT, 'train.log')
LOGS_DIR = os.path.join(REPO, 'logs')
GPU_CSV = os.path.join(LOGS_DIR, 'gpu_usage.csv')
OUT = os.path.join(ROOT, 'continuous_report.out')
INTERVAL = int(os.environ.get('CONTINUOUS_REPORT_INTERVAL', '30'))

def tail(path, n=40):
    if not os.path.exists(path):
        return [f'-- missing file: {path} --']
    try:
        return subprocess.check_output(['tail','-n',str(n), path], text=True, stderr=subprocess.DEVNULL).splitlines()
    except Exception:
        # fallback naive
        with open(path, 'r', errors='ignore') as f:
            lines = f.read().splitlines()
            return lines[-n:]

def last_csv_rows(path, n=8):
    if not os.path.exists(path):
        return [f'-- missing file: {path} --']
    try:
        return subprocess.check_output(['tail','-n',str(n), path], text=True, stderr=subprocess.DEVNULL).splitlines()
    except Exception:
        with open(path, 'r', errors='ignore') as f:
            lines = f.read().splitlines()
            return lines[-n:]

def run_estimator():
    est = os.path.join(ROOT, 'estimate_progress.py')
    if not os.path.exists(est):
        return '-- estimator missing --'
    try:
        out = subprocess.check_output([sys.executable, est], text=True, stderr=subprocess.STDOUT, timeout=20)
        return out.strip().splitlines()
    except subprocess.CalledProcessError as e:
        return [f'-- estimator error: {e.returncode} --'] + (e.output or '').splitlines()
    except Exception as e:
        return [f'-- estimator exception: {e} --']

def make_report():
    ts = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')
    parts = []
    parts.append(f'=== REPORT {ts} ===')
    parts.append('\n-- train.log tail --')
    parts.extend(tail(TRAIN_LOG, n=40))
    parts.append('\n-- gpu_usage.csv last rows --')
    parts.extend(last_csv_rows(GPU_CSV, n=8))
    parts.append('\n-- estimator --')
    parts.extend(run_estimator())
    parts.append('\n')
    return '\n'.join(parts)

def main():
    # ensure out exists
    with open(OUT, 'a'):
        pass
    while True:
        try:
            rpt = make_report()
            with open(OUT, 'a', encoding='utf-8') as f:
                f.write(rpt + '\n')
            # also print to stdout for immediate nohup output
            print(rpt)
        except Exception as e:
            with open(OUT, 'a', encoding='utf-8') as f:
                f.write(f'-- reporter exception: {e}\n')
        time.sleep(INTERVAL)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('continuous_reporter: stopped')

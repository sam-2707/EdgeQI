#!/usr/bin/env python3
"""Estimate remaining training time by parsing the latest Ultralytics/YOLO train log.
Writes a short summary to stdout.
"""
import os
import re
import sys
from statistics import median

ROOT = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(os.path.dirname(ROOT), 'logs')

def find_latest_log():
    # prefer latest file in logs/, else fall back to train.log next to script
    if os.path.isdir(LOGS_DIR):
        # ignore GPU monitor files when selecting the training log
        files = sorted([f for f in os.listdir(LOGS_DIR) if os.path.isfile(os.path.join(LOGS_DIR, f)) and 'gpu' not in f.lower() and 'monitor' not in f.lower()], key=lambda x: os.path.getmtime(os.path.join(LOGS_DIR, x)), reverse=True)
        if files:
            return os.path.join(LOGS_DIR, files[0])
    candidate = os.path.join(ROOT, 'train.log')
    if os.path.exists(candidate):
        return candidate
    return None

def tail_lines(path, n=2000):
    try:
        with open(path, 'rb') as f:
            f.seek(0, os.SEEK_END)
            end = f.tell()
            size = 8192
            data = b''
            while end > 0 and data.count(b"\n") <= n:
                toread = min(size, end)
                f.seek(end - toread)
                data = f.read(toread) + data
                end -= toread
            return data.decode('utf-8', errors='ignore').splitlines()[-n:]
    except Exception:
        return []

def parse(lines):
    it_s_vals = []
    epoch = None
    epoch_total = None
    current_iter = None
    iters_per_epoch = None
    # look for patterns
    for ln in lines:
        # it/s
        m = re.search(r'([0-9]+(?:\.[0-9]+)?)\s*it/s', ln)
        if m:
            try:
                it_s_vals.append(float(m.group(1)))
            except Exception:
                pass
        # s/it -> convert
        m2 = re.search(r'([0-9]+(?:\.[0-9]+)?)\s*s/it', ln)
        if m2:
            try:
                s=float(m2.group(1));
                if s>0: it_s_vals.append(1.0/s)
            except Exception:
                pass
        # Epoch like 'Epoch 3/100'
        mev = re.search(r'Epoch\s*(\d+)\s*/\s*(\d+)', ln)
        if mev:
            epoch = int(mev.group(1)); epoch_total=int(mev.group(2))
        # patterns like [ 12/456 ] or 'train: 12/456'
        mbrs = re.findall(r'\[?\s*(\d+)\s*/\s*(\d+)\s*\]?', ln)
        for mbr in mbrs:
            try:
                a=int(mbr[0]); b=int(mbr[1]);
                if b == 100:
                    epoch = a; epoch_total = b
                elif 10 < b < 20000:
                    current_iter=a; iters_per_epoch=b
            except Exception:
                pass
    return it_s_vals, epoch, epoch_total, current_iter, iters_per_epoch

def estimate(it_s_vals, epoch, epoch_total, current_iter, iters_per_epoch):
    if not it_s_vals:
        return None
    # use median of last values
    med = median(it_s_vals)
    if med <= 0:
        return None
    # if we have epoch info and iters per epoch
    if epoch is not None and epoch_total is not None and iters_per_epoch is not None and current_iter is not None:
        epochs_left = max(0, epoch_total - epoch)
        iters_left = epochs_left * iters_per_epoch + max(0, iters_per_epoch - current_iter)
        secs = iters_left / med
        return secs
    # fallback: if we can find an approximate remaining count by searching for 'Epoch X/Y' and assume default iters
    if epoch is not None and epoch_total is not None:
        # guess: use average iterations per epoch from log if unknown; assume 200 iters
        guessed_iters = iters_per_epoch if iters_per_epoch is not None else 200
        epochs_left = max(0, epoch_total - epoch)
        secs = (epochs_left * guessed_iters) / med
        return secs
    # last fallback: can't estimate
    return None

def pretty_secs(s):
    if s is None:
        return 'unknown'
    s = int(s)
    h = s//3600; s%=3600; m=s//60; s%=60
    return f"{h}h {m}m {s}s"

def main():
    log = find_latest_log()
    if not log:
        print('No log found (checked logs/ and train.log)')
        return 2
    lines = tail_lines(log, n=2000)
    it_s_vals, epoch, epoch_total, current_iter, iters_per_epoch = parse(lines)
    secs = estimate(it_s_vals, epoch, epoch_total, current_iter, iters_per_epoch)
    print('log:', log)
    print('detected_it_s_samples:', len(it_s_vals))
    if it_s_vals:
        from statistics import median, mean
        print('it/s median:', round(median(it_s_vals),3), 'mean:', round(mean(it_s_vals),3))
    print('epoch:', epoch, 'of', epoch_total)
    print('current_iter (in epoch):', current_iter, 'iters_per_epoch:', iters_per_epoch)
    print('estimated_remaining:', pretty_secs(secs))
    return 0

if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""Prepare bounded, sanitized native notification payloads; no GUI or credentials."""
import importlib.util
import json
from pathlib import Path
import sys
from xml.sax.saxutils import escape

spec = importlib.util.spec_from_file_location('exporter', Path(__file__).resolve().parents[1] / 'scripts/export-codex-session.py')
exporter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(exporter)
SOUNDS = {'SUCCESS': 'Asterisk', 'WARNING': 'Exclamation', 'FAILED': 'Hand'}


def prepare(status, title, message):
    if status not in SOUNDS:
        raise ValueError('Unsupported notification status')
    title = ' '.join(exporter.sanitize(str(title)).split())[:80]
    message = ' '.join(exporter.sanitize(str(message)).split())[:240]
    xml = '<toast><visual><binding template="ToastGeneric"><text>' + escape(title) + '</text><text>' + escape(message) + '</text></binding></visual><audio silent="true"/></toast>'
    return {'status': status, 'title': title, 'message': message, 'xml': xml, 'sound': SOUNDS[status]}


if __name__ == '__main__':
    try:
        value = json.load(sys.stdin)
        print(json.dumps(prepare(value['status'], value['title'], value['message']), ensure_ascii=True))
    except (ValueError, KeyError, TypeError):
        print('Notification payload rejected', file=sys.stderr)
        raise SystemExit(1)

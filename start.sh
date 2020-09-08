export LC_ALL=C.UTF-8
export PYTHONIOENCODING=utf8

/home/deploy/okr-extraction/venv/bin/gunicorn main:app -b 0.0.0.0:6789
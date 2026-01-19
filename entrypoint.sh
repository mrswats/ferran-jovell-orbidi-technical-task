#!/usr/bin/env bash

set -euox

main () {
    gunicorn "orbidi.wsgi:application"
}

main "$@"

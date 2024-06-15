#!/bin/bash
find . -name 'coverage.txt' -delete
poetry run pytest --cov-report term --cov snapp_mle_task tests/ >>.logs/coverage.txt

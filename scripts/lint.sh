#!/usr/bin/env sh

set -o errexit
set -o nounset

run_checkers() {
  black --check .

  mypy .

  flake8 .

  xenon --max-absolute A \
        --max-modules A \
        --max-average A \
        --exclude src/jnt_django_graphene_toolbox/helpers/values.py,src/jnt_django_graphene_toolbox/fields/model_connection.py,src/jnt_django_graphene_toolbox/types/model.py \
        .

  # Checking `pyproject.toml` file contents:
  poetry check

  # Checking dependencies status:
  pip check

  # Checking if all the dependencies are secure and do not have any
  # known vulnerabilities:
#  safety check --bare --full-report
}

run_checkers

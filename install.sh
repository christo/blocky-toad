#!/usr/bin/env bash

which pipenv >/dev/null || (echo pipenv not found, install it. && exit 1)
pipenv install --pre


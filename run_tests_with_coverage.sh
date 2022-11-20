#!/bin/bash

coverage run --branch -m pytest src
coverage html

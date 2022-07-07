# -*- coding: utf-8 -*
from flask import Blueprint
blue_test = Blueprint('blue_test',__name__)
@blue_test.route('/blue_test')
def new_blue_test():
    return "success"
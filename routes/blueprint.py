# Routes of the main app

from flask import Blueprint
from controllers.timers_controller import get_timer, set_timer

blueprint = Blueprint('main_app', __name__)

# URLs are already relative to main /timers
blueprint.route('/', methods=['POST'])(set_timer)
blueprint.route('/<int:timer_id>', methods=['GET'])(get_timer)

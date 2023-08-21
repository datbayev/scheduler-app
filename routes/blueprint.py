# Routes of the main app

from flask import Blueprint
from controllers.timers_controller import get_timer, set_timer, ping

blueprint = Blueprint('main_app', __name__)

# URLs are already relative to main /timers
blueprint.route('/', methods=['POST'])(set_timer)
blueprint.route('/<int:timer_id>', methods=['GET'])(get_timer)
blueprint.route('/ping/<int:ping_id>', methods=['POST'])(ping)  # endpoint for testing purposes to validate that scheduled jobs indeed do hit the url

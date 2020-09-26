from flask import Flask
app = Flask(__name__)



# import codeitsuisse.routes.contact_tracing
# import codeitsuisse.routes.inventory_management
# import codeitsuisse.routes.social_distancing
# import codeitsuisse.routes.babylon
# import codeitsuisse.routes.contact_tracing
# import codeitsuisse.routes.inventory_management

# 1: 2005, SEP26
# 2: 2033, SEP26
# 3: 2047, SEP26
# 4: 2128, SEP26
# 5: 2148, SEP26

import codeitsuisse.routes.contact_tracing
# 1 400
import codeitsuisse.routes.revisitGeometry
# 1 400
import codeitsuisse.routes.SaladSpree
# 1 500
import codeitsuisse.routes.social_distancing

# 4 400
import codeitsuisse.routes.inv_management

# 3 500
import codeitsuisse.routes.cluster

import codeitsuisse.routes.gmo_engg

# 2 500
import codeitsuisse.routes.clean_floor

import codeitsuisse.routes.magical_fruit
import codeitsuisse.routes.optimized_portfolio
import codeitsuisse.routes.snake_mirror
import codeitsuisse.routes.bored_scribe
import codeitsuisse.routes.driverless_car

# 5 700
import codeitsuisse.routes.olympiad_babylon
import codeitsuisse.routes.swap_hedging



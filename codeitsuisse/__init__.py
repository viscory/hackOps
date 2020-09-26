from flask import Flask
app = Flask(__name__)



# import codeitsuisse.routes.contact_tracing
# import codeitsuisse.routes.inventory_management
# import codeitsuisse.routes.social_distancing
# import codeitsuisse.routes.babylon
# import codeitsuisse.routes.contact_tracing
# import codeitsuisse.routes.inventory_management

# 1: 2005, SEP26

# 1 264
import codeitsuisse.routes.contact_tracing
# 1 400
import codeitsuisse.routes.revisitGeometry
#1 400
import codeitsuisse.routes.SaladSpree
#1 500s
import codeitsuisse.routes.social_distancing

import codeitsuisse.routes.inv_management
import codeitsuisse.routes.cluster
import codeitsuisse.routes.gmo_engg
import codeitsuisse.routes.clean_floor
import codeitsuisse.routes.magical_fruit
import codeitsuisse.routes.optimized_portfolio
import codeitsuisse.routes.snake_mirror
import codeitsuisse.routes.bored_scribe
import codeitsuisse.routes.driverless_car
import codeitsuisse.routes.olympiad_babylon
import codeitsuisse.routes.swap_hedging



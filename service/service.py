import service.db_functions as db

from service.simulations import run_simulations
from service.ml_networks.generator import run_generator
from service.ml_networks.regressor import run_regressor
from service.ml_networks.results import run_results

def run_service(user_name, project_name):
    info = f'User: {user_name}\tProject: {project_name}\t'
    search_conditions = db.get_search_conditions(user_name, project_name)
    project_settings = db.get_columns(search_conditions, db.PROJECT_SETTINGS,)

    if project_settings[db.SIMULATION_SETTINGS][db.RUN]:
        run_simulations(user_name, project_name, project_settings, info, search_conditions)

    if project_settings[db.REGRESSOR_SETTINGS][db.RUN]:
        run_regressor(project_settings, info, search_conditions)
        
    if project_settings[db.GENERATOR_SETTINGS][db.RUN]:
        run_generator(project_settings, info, search_conditions)

    if project_settings[db.RESULTS][db.RUN]:
        run_results(project_settings, info, search_conditions)
from service.helper import np, pd, create_simulation_dir, logger
from service import db_functions as db

from probabilistic import ProbabilisticEnergyPrediction
from probabilistic import ProbabilisticParameters

from service.energy_model_simulations import generate_simulation_results, get_run_periods
from service.ml_networks import train_generator, train_regressor, predict, get_scaling_parameters

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
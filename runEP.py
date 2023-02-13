#!/usr/bin/python3
import os
import multiprocessing
from multiprocessing import Queue, Process, Pool, Value
from functools import partial
from datetime import datetime
import shutil
import sys
import subprocess
from subprocess import DEVNULL
import ctypes
from unittest.loader import VALID_MODULE_NAME
# libgcc_s = ctypes.CDLL('libgcc_s.so.1') #uncomment for running on Windows

try:
    processors = int(sys.argv[2]) #provide input if cpu_count cannot be determined, automatically
except:
    processors = multiprocessing.cpu_count()
    
try:
    home_directory = os.environ['HOME']
except:
    home_directory = "C:/"

temp_dir = 'Temp'
temp_dir_pre = 'EP_'
ex_executable = 'ExpandObjects'
ep_executable = 'energyplus'
read_var_eso_executable = 'PostProcess/ReadVarsESO'
temp_idf_name = 'in.idf'
temp_epw_name = 'in.epw'
temp_eplus_out = 'eplusout'
temp_eplus_out_eso = 'eplusout.eso'
temp_eplus_out_err = 'eplusout.err'
temp_eplus_out_csv = 'eplusout.csv'
temp_eplus_out_dxf = 'eplusout.dxf'
temp_expanded_file = 'expanded.idf'
csv_extension = '.csv'
dxf_extension = '.dxf'
idf_extension = '.idf'
epw_extension = '.epw'
err_extension = '.err'

building = 'Building'
err_file = 'sim_err.txt'
err_extension = '.err'
json_extension = '.json'

error_warnings = ['CalculateZoneVolume']

known_warnings = [
                    'Output:PreprocessorMessage',
                    'Site:GroundTemperature:BuildingSurface',
                    'ProcessScheduleInput',
                    'CheckUsedConstructions',
                    'Report Variables were requested but not generated',
                    'CheckConvexity',
                    'DXFOut',
                    'GetVertices',
                    'GetSurfaceData',
                    'DetermineShadowingCombinations',
                    'FixViewFactors'
                 ]

ep_dir = os.path.join(home_directory, [x for x in os.listdir(home_directory) if 'EnergyPlus' in x][0])

start_time = datetime.now()

def create_temp_folder(full_name, temp_EP_dirs, epw_file):
    """
    Creates temporary folder for EP simulation.
    """
    os.makedirs(full_name)
    os.chdir(full_name)
    shutil.copy(epw_file, temp_epw_name)
    temp_EP_dirs.put(full_name)

def get_IDF_files(idf_folder):
    """
    Searches IDF files in the folder and its subfolders.
    """
    idf_files = []
    print ("Searching IDF Files...")
    for root, dirs, files in os.walk(idf_folder):
        for f in files:
            if f.endswith(idf_extension):
                csv_file = os.path.join(root, f[:-4] + csv_extension)
                if (not os.path.isfile(csv_file)):
                    idf_files.append(os.path.join(root, f))
    idf_files.sort()
    print (f'{len(idf_files)} IDF files found!')
    return idf_files

def get_EPW_files(idf_folder):
    """
    Returns the first EPW file in the folder/subfolders.
    """
    for root, dirs, files in os.walk(idf_folder):
        for f in files:
            if f.endswith(epw_extension): return os.path.join(root, f)

def simulate(idf_file, temp_dir):
    """
    Simulates the IDF file using EnergyPlus.
    """
    os.chdir(temp_dir)
    shutil.copy(idf_file, temp_idf_name)
    
    subprocess.call([os.path.join(ep_dir, ex_executable)], stdout=DEVNULL, stderr=DEVNULL)
    shutil.move(temp_expanded_file, temp_idf_name)

    subprocess.call([os.path.join(ep_dir, ep_executable)], stdout=DEVNULL, stderr=DEVNULL)
    subprocess.call([os.path.join(ep_dir, read_var_eso_executable), ' ', 'N'], stdout=DEVNULL, stderr=DEVNULL)

    shutil.copy(temp_eplus_out + csv_extension, idf_file[:-4] + csv_extension)
    shutil.copy(temp_eplus_out + err_extension, idf_file[:-4] + err_extension)
    shutil.copy(temp_eplus_out + dxf_extension, idf_file[:-4] + dxf_extension)

def run_simulation(idf_file, temp_EP_dirs, processed_files, total_files):
    """
    Calls the simulate function on the IDF file.
    """
    temp_dir = temp_EP_dirs.get()
    
    simulate(idf_file, temp_dir)

    processed_files.value += 1
    if processed_files.value % processors == 0:
        t = datetime.now()
        processing_time_file = (t - start_time) / float(processed_files.value)
        etl = processing_time_file * (total_files - processed_files.value)
        finish_time = (datetime.now() + etl).strftime("%H:%M:%S")
        sys.stdout.write(f'\nTotal Files:\t\t{total_files}' +
                        f'\nFiles Remaining:\t{total_files - processed_files.value}' +
                        f'\nFiles Processed:\t{processed_files.value}' +
                        f'\nLast Processed:\t\t{idf_file}' +
                        f'\nEstimated Finish Time:\t{finish_time} ({etl})' + 
                        f'\n')
    temp_EP_dirs.put(temp_dir)

def delete_temp_folder(idf_folder):
    temp_dir_name = os.path.join(idf_folder, temp_dir)
    if os.path.exists(temp_dir_name): shutil.rmtree(temp_dir_name)

def contains_error(file):
    with open(file) as f:
        error = False
        line = f.readline()
        if not line.startswith('Program Version,EnergyPlus'):
            return False
        
        while line:
            if '** Warning **' in line and all([x not in line for x in known_warnings]):
                return True
            line = f.readline()
    return error

def get_err_files(temp_folder):
    err_files = []
    print ("Searching error files...")
    for root, dirs, files in os.walk(temp_folder):
        for f in files:
            if f.endswith(err_extension) and contains_error(os.path.join(root, f)):
                err_files.append(f[:-4])
    err_files.sort()
    print (f'Error Files: \t{len(err_files)}')
    return err_files

def write_err_files(temp_folder):
    with open (f'{temp_folder}/{err_file}', 'w') as f:
        for l in get_err_files(temp_folder):
            f.write(f'{l}\n')

if __name__ == '__main__':
    idf_folder = sys.argv[1] #input("Enter the full path to look for IDF files:\n")

    temp_EP_dirs = Queue()
    processed_files = Value('d', 0)
    delete_temp_folder(idf_folder)

    epw_file = get_EPW_files(idf_folder) 
    epw_file_input = epw_file
    
    if (epw_file_input != ''):
        epw_file = epw_file_input
    
    if (not os.path.isfile(epw_file)):
        print (f"Invalid Weather File: {epw_file}")
        sys.exit()

    print (f'Weather File: {epw_file}')
    idf_files = get_IDF_files(idf_folder)

    # print (idf_files)

    temp_dirs = [os.path.join(idf_folder, temp_dir, f'{temp_dir_pre}{i}') for i in range (min(processors, len(idf_files)))]
    
    processes = [Process(target=create_temp_folder, args=(x, temp_EP_dirs, epw_file)) for x in temp_dirs]
    # Run processes
    for p in processes:
        p.start()

    # Exit the completed processes
    for p in processes:
        p.join()

    take = processors * 4
    n_files = len(idf_files)
    start = 0
    while start < n_files:
        upto = min (n_files, start + take)
        processes = [Process(target=run_simulation, 
                             args=(x, temp_EP_dirs, processed_files, n_files)) for x in idf_files[start:upto]]
        # Run processes
        for p in processes:
            p.start()

        # Exit the completed processes
        for p in processes:
            p.join()

        start = upto
    # with Pool(processes=processors) as pool:
    #     par_func = partial(run_simulation, temp_EP_dirs=temp_EP_dirs, processed_files=processed_files, total_files=n_files)
    #     pool.map(par_func, idf_files)

    delete_temp_folder(idf_folder)
    write_err_files(idf_folder)

    print (f'---finished processing {len(idf_files)} files in {(datetime.now() - start_time)}---')
    with open(f'{idf_folder}/sim.txt', 'w') as f:
        f.write(f'---finished processing {len(idf_files)} files in {(datetime.now() - start_time)}---')
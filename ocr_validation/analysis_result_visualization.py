"""
Visualization of ocromore input, groundtruth and
results iteratively over files. Can be used for
output analysis. 
"""


from configuration.configuration_handler import ConfigurationHandler
from akf_corelib.database_handler import DatabaseHandler
from pathlib import Path
from tableparser import TableParser
from time import sleep


CODED_CONFIGURATION_PATH_VOTER = './configuration/voter/config_akftest_js.conf'  # configuration which is not given with cli args
CODED_CONFIGURATION_PATH_DB_READER = './configuration/to_db_reader/config_read_akftest.conf'  # configuration which is not given with cli args

config_handler = ConfigurationHandler(first_init=True, fill_unkown_args=True,\
                                      coded_configuration_paths=[CODED_CONFIGURATION_PATH_VOTER, CODED_CONFIGURATION_PATH_DB_READER])


config = config_handler.get_config()
tableparser = TableParser(config)

dh = DatabaseHandler(dbdir=str(Path(config.DB_DIR_VOTER).absolute()))
dh.set_dirpos(tablename_pos=config.TABLENAME_POS, ocr_profile_pos=config.OCR_PROFILE_POS, ocr_pos=config.OCR_POS, dbname_pos=config.DBPATH_POS)
dh.fetch_files(config.INPUT_FILEGLOB, config.INPUT_FILETYPES)
dh.fetch_gtfiles(config.GROUNDTRUTH_FILEGLOB, gtflag=True)
if config.VISUALIZE_MSA:
    dh.fetch_outputfiles(config.OUTPUT_ROOT_PATH,"sql_akf_new_msa_best")
if config.VISUALIZE_NDIST:
    dh.fetch_outputfiles(config.OUTPUT_ROOT_PATH,"sql_akf_ndist_keying")

# filestructs = dh.get_files()
filestructs_gt = dh.get_groundtruths()
filestructs_output = dh.get_outputfiles()

firstcall = True
for db in filestructs_output:
    print("Parsing database:", db)

    files = filestructs_output[db]
    files_gt = filestructs_gt[db]

    #if db != "1976": continue


    for file in files:
        filestruct = files[file]
        foundgt = None
        for gt_key in files_gt:
            gt_file = files_gt[gt_key]
            if gt_key in file:
                foundgt = gt_file.path

        if foundgt is not None:
            print("do comparison here")

            fs_path = filestruct.path
            foundgt_path = foundgt
            if config.SHOW_REDUCED_RESULTS:
                fs_path += ".red"
                foundgt_path += ".red"


            process = tableparser.display_stuff(fs_path, foundgt_path, firstcall=firstcall)
            if firstcall is True:
                sleep(0.100)  # sleep for 100ms until meld finally appeared
            firstcall = False



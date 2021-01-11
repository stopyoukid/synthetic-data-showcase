import time
import datetime
import json
import sys
import logging
import argparse
from os import path, mkdir
from synthetic_data import runPipeline

def main():
    """Executes pipeline according to config file and command line arguments.
    """
    parser = argparse.ArgumentParser(description='proxy-data')
    parser.add_argument('config', metavar='config', type=str, help='path to config file')
    parser.add_argument("--verbose", '--v', action='count',  default=0)
    parser.add_argument('--aggregate', '--agg', action='store_true', help='aggregate sensitive microdata', default=False)
    parser.add_argument('--generate', '--gen', action='store_true', help='generate synthetic microdata', default=False)
    parser.add_argument('--evaluate', '--eval', action='store_true', help='evaluate synthetic microdata', default=False)
    parser.add_argument('--navigate', '--nav', action='store_true', help='navigate privacy-preserving datasets', default=False)
    args = parser.parse_args()
    config_path = args.config 

    if args.verbose > 0:
        logging.basicConfig(format="%(funcName)s: %(message)s", level=logging.INFO)
    else:
        logging.basicConfig(format="%(funcName)s: %(message)s", level=logging.WARN)

    logging.info('using config %s' %config_path)
    
    try:
        config = json.load(open(config_path))
        config['aggregate'] = args.aggregate if args.aggregate != None else False
        config['generate'] = args.generate if args.generate != None else False
        config['evaluate'] = args.evaluate if args.evaluate != None else False
        config['navigate'] = args.navigate if args.navigate != None else False

        # if no cmd options set, we do everyting     
        if not config['aggregate'] and not config['generate'] and not config['evaluate'] and not config['navigate']:
            config['aggregate'] = True
            config['generate'] = True
            config['evaluate'] = True
            config['navigate'] = True

         # set based on the number of cores/memory available
        config['parallel_jobs'] = config.get('parallel_jobs', 1)
        config['memory_limit_pct'] = config.get('memory_limit_pct', 80)

        # numeric parameters controlling synthesis and aggregation
        config['use_columns'] = config.get('use_columns', [])
        config['record_limit'] = config.get('record_limit', -1) # use all sensitive records
        config['reporting_length'] = config.get('reporting_length', 3) # support any 2 selections
        config['reporting_threshold'] = config.get('reporting_threshold', 10) # only allow/report counts >= this
        config['reporting_precision'] = config.get('reporting_precision', 10) # only report counts to the closest precision

        # parameters affecting the representation and interpretation of values
        config['sensitive_zeros'] = config.get('sensitive_zeros', [])
        config['seeded'] = config.get('seeded', True)

        # specified parameters affecting file I/O
        config['prefix'] = config.get('prefix', 'my')
        config['output_dir'] = config.get('output_dir', './')
        config['sensitive_microdata_path'] = config.get('sensitive_microdata_path', None)
        config['sensitive_microdata_delimiter'] = config.get('sensitive_microdata_delimiter', ',')

        # derived parameters affecting file I/O
        config['reportable_aggregates_path'] = path.join(config['output_dir'], config['prefix'] + '_reportable_aggregates.tsv')
        config['synthetic_microdata_path'] = path.join(config['output_dir'], config['prefix'] + '_synthetic_microdata.tsv')
        config['sensitive_aggregates_path'] = path.join(config['output_dir'], config['prefix'] + '_sensitive_aggregates.tsv')

        if not path.exists(config['output_dir']):
            mkdir(config['output_dir'])

        runPipeline(config)

    except Exception as e:
        logging.exception(e)



if __name__ == '__main__':
    main( )

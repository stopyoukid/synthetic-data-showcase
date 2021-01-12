from synthetic_data.generator import generate
from synthetic_data.evaluator import evaluate
from synthetic_data.aggregator import aggregate
from synthetic_data.navigator import Navigator
import json
import logging

from os import path

def runPipeline(config):
    """Sets internal arguments from the config file and runs pipeline stages accordingly.

    Args:
        config: options from the json config file, else default values.
    """
    
    if config['aggregate']:
        aggregate(config)
    
    if config['generate']:
        generate(config)

    if config['evaluate']:
        if not path.exists(config['sensitive_aggregates_path']):
            logging.info(f'Missing sensitive aggregates; aggregating...')
            aggregate(config)
        if not path.exists(config['synthetic_microdata_path']):
            logging.info(f'Missing synthetic microdata; generating...')
            generate(config)
        evaluate(config)

    if config['navigate']:
        if not path.exists(config['sensitive_aggregates_path']):
            logging.info(f'Missing sensitive aggregates; aggregating...')
            aggregate(config)
        if not path.exists(config['synthetic_microdata_path']):
            logging.info(f'Missing synthetic microdata; generating...')
            generate(config)
            
        navigator = Navigator(config)
        navigator.process()

    json.dump(config, open(path.join(config['output_dir'], config['prefix'] + '_config.json'), 'w'), indent=1)

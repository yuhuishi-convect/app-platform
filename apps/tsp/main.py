from typing import Dict, Any
import os
import argparse
import json
from tsp import main as tsp_main

class App:
    """
    Class to wrap the main program.
    It supports the following method:
    - schema: return the input data schema the main program expec
    - spec: return the configuration spec the main program expect
    - run: invoke the main program
    """

    def __init__(self, input_db_path: str, config_path: str) -> None:
        with open(config_path, 'r') as f:
            config = json.load(f)

        self.config = config
        self.input_db_path = input_db_path
        

    @staticmethod
    def schema() -> str:
        """
        Return the input data schema the main program expect.
        """
        # load ddl.sql and return the content
        ddl_path = os.path.join(os.path.dirname(__file__), 'resources/ddl.sql')
        with open(ddl_path, 'r') as f:
            return f.read()
        
    @staticmethod
    def spec() -> str:
        """
        Return the configuration spec the main program expect.
        """
        # load resources/config.json and return the content
        config_path = os.path.join(os.path.dirname(__file__), 'resources/config.json')
        with open(config_path, 'r') as f:
            return f.read()


    def run(self) -> str:
        """
        Invoke the main program
        """
        tsp_main(input_db_path=self.input_db_path, config=self.config)



def launcher():
    """
    Cli program that supports the following commands
    - schema: return the input data schema
    - spec: return the configuration spec
    - run: invoke the main program
    """
    # create an argument parser that supports schema, spec, run subcommands
    arg_parser = argparse.ArgumentParser()

    # add a subcommand run that supports the following arguments
    # - input_db_path: the path to the input database
    # - config: the configuration
    sub_parsers = arg_parser.add_subparsers(dest="command")
    run_parser = sub_parsers.add_parser('run')

    run_parser.add_argument('--input-db-path', required=True)
    run_parser.add_argument('--config', required=True)

    sub_parsers.add_parser('schema')
    sub_parsers.add_parser('spec')

    # parse the arguments
    args = arg_parser.parse_args()
    if args.command == 'schema':
        print(App.schema())
    elif args.command == 'spec':
        print(App.spec())
    elif args.command == 'run':
        app = App(args.input_db_path, args.config)
        print(app.run())
    else:
        arg_parser.print_help()



if __name__ == '__main__':
    launcher()
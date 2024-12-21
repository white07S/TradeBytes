import argparse
import json
import logging
from typing import List, Dict
from src.barchart_api_client import APIClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_api_choices(config_path: str) -> List[str]:
    """
    Load the list of API names from the configuration JSON file.
    """
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
        return list(config.get("apis", {}).keys())
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from config file: {e}")
        raise

def parse_arguments(api_choices: List[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Market Data API Fetcher")
    parser.add_argument(
        '--api',
        type=str,
        choices=api_choices + ["list"],
        help="Name of the API to fetch data for (as defined in the configuration file). Use 'list' to see all options."
    )
    parser.add_argument(
        '--output',
        type=str,
        default="output_data.json",
        help="Filename for the output JSON data"
    )
    parser.add_argument(
        '--provider',
        type=str,
        required=True,
        choices=['barchart', 'nasdaq'],
        help="Data provider (either 'barchart' or 'nasdaq')"
    )
    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help="Path to the API query configuration JSON file (overrides provider-specific default)"
    )
    return parser.parse_args()

def main():
    # Default configuration path for Barchart
    default_config_path = "config/barchart_apis.json"

    try:
        # Load API choices from the default configuration
        api_choices = load_api_choices(default_config_path)

        # Parse arguments
        args = parse_arguments(api_choices=api_choices)
        api_name = args.api
        output_file = args.output
        provider = args.provider
        config_path = args.config or default_config_path

        # If '--api list' is specified, print all possible APIs and exit
        if api_name == "list":
            logger.info("Available APIs:")
            for api in api_choices:
                print(f"- {api}")
            return

        # Check provider logic
        if provider == "nasdaq":
            logger.error("Nasdaq provider is not implemented.")
            raise NotImplementedError("Nasdaq provider functionality is not implemented yet.")

        # Initialize API client and fetch data
        client = APIClient(config_path=config_path)
        data: Dict[str, Any] = client.fetch_api_data(api_name=api_name)

        # Save data to the output file
        client.save_data_to_json(data=data, filename=output_file)
        logger.info("Data fetching and saving completed successfully.")

    except NotImplementedError as nie:
        logger.error(nie)
    except Exception as e:
        logger.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
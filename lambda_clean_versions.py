import argparse
import os
from shared.boto_connections import BotoSession, LambdaService
from shared.system_log import SystemLogger

MODULE_NAME = __file__.rsplit("/", maxsplit=1)[-1]
LOGGER = SystemLogger(
    MODULE_NAME, f"{os.path.dirname(__file__)}/logs/{MODULE_NAME}", MODULE_NAME
)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List and clean up lambda versions.")
    parser.add_argument("profile_name", help="The AWS profile name to use", type=str)
    parser.add_argument("region_name", help="The AWS region name to use", type=str)
    parser.add_argument("keep_last_x", help="Number of versions to keep", type=int)

    args = parser.parse_args()

    boto_session = BotoSession(
        profile_name=args.profile_name, region_name=args.region_name
    )
    lambda_service = LambdaService(boto_session)

    lambdas = lambda_service.get_lambdas()
    total_lambda_functions = len(lambdas)
    LOGGER.info("Total Lambdas: %s", total_lambda_functions)

    for index, lambda_name in enumerate(lambdas, 1):
        LOGGER.info("Processing lambda %s of %s", index, total_lambda_functions)
        try:
            LOGGER.info("Lambda: %s", lambda_name)
            lambda_versions = lambda_service.get_lambda_versions(lambda_name)
            lambda_service.remove_old_versions(
                lambda_versions, lambda_name, args.keep_last_x
            )
        except Exception as error:
            LOGGER.error("Error processing lambda %s: %s", lambda_name, error)

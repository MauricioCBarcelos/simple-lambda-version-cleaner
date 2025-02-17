import os
import boto3

from shared.system_log import SystemLogger

MODULE_NAME = __file__.rsplit("/", maxsplit=1)[-1]
LOGGER = SystemLogger(
    MODULE_NAME, f"{os.path.dirname(__file__)}/logs/{MODULE_NAME}", MODULE_NAME
)


class BotoSession:
    def __init__(self, **kwargs):
        session_parameters = {}

        profile_name = kwargs.get("profile_name")
        region_name = kwargs.get("region_name")

        if profile_name:
            session_parameters["profile_name"] = profile_name
        if region_name:
            session_parameters["region_name"] = region_name

        self.session = boto3.Session(**session_parameters)

    def get_client(self, module: str) -> boto3.client:
        return self.session.client(module)

    def get_resource(self, module: str) -> boto3.resource:
        return self.session.resource(module)


class LambdaService:
    def __init__(self, aws_boto_session: BotoSession):
        self.lambda_service_client = aws_boto_session.get_client("lambda")

    def get_lambdas(self) -> list:
        list_of_lambda = []
        marker = None
        while True:
            if marker:
                aws_lambda_data = self.lambda_service_client.list_functions(
                    FunctionVersion="ALL", Marker=marker
                )
            else:
                aws_lambda_data = self.lambda_service_client.list_functions(
                    FunctionVersion="ALL"
                )

            if "Functions" in aws_lambda_data:
                list_of_lambda.extend(
                    [function["FunctionName"] for function in aws_lambda_data["Functions"]]
                )

            marker = aws_lambda_data.get("NextMarker")
            if not marker:
                break
        return list_of_lambda

    def get_lambda_versions(self, function_name: str) -> list:
        versions = []
        marker = None

        while True:
            if marker:
                response = self.lambda_service0_client.list_versions_by_function(
                    FunctionName=function_name, Marker=marker, MaxItems=1000
                )
            else:
                response = self.lambda_service_client.list_versions_by_function(
                    FunctionName=function_name, MaxItems=1000
                )

            if "Versions" in response:
                versions.extend(
                    [version["Version"] for version in response["Versions"]]
                )

            marker = response.get("NextMarker")
            if not marker:
                break

        return versions

    def remove_old_versions(
        self,
        versions: list,
        function_name: str,
        number_of_versions_to_keep: int,
    ):
        if len(versions) <= number_of_versions_to_keep:
            LOGGER.info(
                "Number of versions for lambda %s is less than or equal to %s",
                function_name,
                number_of_versions_to_keep,
            )
            return
        versions_to_delete = [
            version
            for version in versions[:-number_of_versions_to_keep]
            if version != "$LATEST"
        ]
        versions_be_maintained = [
            version for version in versions if version not in versions_to_delete
        ]
        LOGGER.info("Versions to delete in %s: %s", function_name, versions_to_delete)
        LOGGER.info(
            "Versions that will be maintained %s: %s",
            function_name,
            versions_be_maintained,
        )
        for version_to_delete in versions_to_delete:
            LOGGER.info(
                "Deleting version %s of lambda %s", version_to_delete, function_name
            )
            self.lambda_service_client.delete_function(
                FunctionName=function_name, Qualifier=version_to_delete
            )

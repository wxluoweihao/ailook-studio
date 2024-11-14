import re

import requests
from requests import Session
from sqlalchemy import create_engine, MetaData
from sqlalchemy.dialects.postgresql import psycopg2
from sqlalchemy.orm import sessionmaker


from marquez_integration.DatasetLineageMapping import DatasetLineageMapping


class DatasetBean:
    def __init__(self, dataset_name:str, dataset_version:str, dataset_type:str):
        self.dataset_name = dataset_name
        self.dataset_version = dataset_version
        self.dataset_type = dataset_type

    def set_dataset_name(self, name):
        self.dataset_name = name

    def set_dataset_version(self, version):
        self.dataset_version = version

    def get_dataset_name(self):
        return self.dataset_name

    def get_dataset_version(self):
        return self.dataset_version


class LineagePath:
    def __init__(self, start_dataset, end_dataset, path):
        self.start_dataset = start_dataset
        self.end_dataset = end_dataset
        self.path = path


class NodeLineage:
    def __init__(self, input_datasets:list[DatasetBean], output_datasets:list[DatasetBean], job_engine, job_state, job_start_time, job_end_time, job_durations):
        self.input_datasets = input_datasets
        self.output_datasets = output_datasets
        self.job_start_time = job_start_time
        self.job_end_time = job_end_time
        self.job_engine = job_engine
        self.job_state = job_state
        self.job_durations = job_durations

    def get_input_datasets(self):
        return self.input_datasets

    def get_output_datasets(self):
        return self.output_datasets

    def generate_lineage_dict(self):
        lineage_dict = {}
        for input_dataset in self.input_datasets:
            lineage_dict[input_dataset] = self.output_datasets
        return lineage_dict

    def get_job_start_time(self):
        return self.job_start_time

    def get_job_end_time(self):
        return self.job_end_time

    def get_job_durations(self):
        return self.job_durations

    def get_job_state(self):
        return self.job_state

    def get_job_engine(self):
        return self.job_engine


class DatasetLineages:
    def __init__(self, input_dataset: DatasetBean, output_datasets: list[DatasetBean], input_node_lineage: NodeLineage):
        self.input_dataset = input_dataset
        self.output_datasets = output_datasets
        self.input_node_lineage = input_node_lineage

    def get_node_lineage(self):
        return self.input_node_lineage

    def get_input_dataset(self):
        return self.input_dataset


class MarquezLineageCollector:
    def __init__(self, host, database, user, password):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        connect_str = "postgresql+psycopg2://marquez-user:mZ7J1F4IYqY6mbIY53Jgu1aL9lqpfjtjdJ5zMRjz9yoC0rL02cweCopEXans2gr4@8.210.27.71:15432/marquez"
        self.engine = create_engine(connect_str)
        self.session = sessionmaker(bind=self.engine)
        self.metadata = MetaData(bind=self.engine)

    def __collect_nodes(self):
        try:
            # Connect to the database
            with self.engine.connect() as connection:
                # Fetch all rows
                rows = connection.execute("""
                select distinct concat_ws(':','job', namespace_name, name) as node_id
                from jobs_view
                """)

                connection.close()

                result_list = [row[0] for row in rows]
                return result_list
        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")

    def __remove_file_extention(self, path:str):
        if "." in path:
            file_name = path.split(".")
            return file_name
        return path

    def __extract_path_parts(self, path:str):
        segments = path.split("/")
        if segments == 1:
            return self.__remove_file_extention(segments)
        else:
            segments[len(segments)-1]

    def __to_dataset_beans_list(self, dataset_versions) -> list[DatasetBean]:
        input_dataset_beans = []
        for input_dataset_version in dataset_versions:
            input_dataset_version = input_dataset_version.get("datasetVersionId")
            namespace = input_dataset_version.get("namespace")
            dataset_name = input_dataset_version.get("name")
            dataset_version = input_dataset_version.get("version")
            dataset_type = "table"
            if namespace.startswith("s3"):
                if dataset_name.startswith("/"):
                    dataset_name = dataset_name.lstrip("/")
                dataset_name = (namespace + "/" + dataset_name)
                # dataset_name = self.__extract_path_parts(dataset_name)
                dataset_type = "parquet"
            input_dataset_beans.append(DatasetBean(dataset_name, dataset_version, dataset_type))
        return input_dataset_beans

    def __get_lineage_as_metadata(self, lineage: DatasetLineages):
        node_lineage = lineage.get_node_lineage()
        return " dataset: {}, dataset_version: {}, engine: {}, latest_run_status：{}, latest_run_start_time:{}, latest_run_end_time:{}, latest_run_duration_milliseconds: {} ".format(
                lineage.get_input_dataset().get_dataset_name(),
                lineage.get_input_dataset().get_dataset_version(),
                node_lineage.get_dataset_version(),
                node_lineage.get_job_engine(),
                node_lineage.get_job_status(),
                node_lineage.get_job_start_time(),
                node_lineage.get_job_end_time(),
                node_lineage.get_job_durations(),
            )

    def __parse_lineage_from_json(self, json) -> list[NodeLineage]:
        if "graph" not in json:
            return None
        json = json.get("graph")
        nodes_lineages = []
        for entity in json:
            if entity.get("type") == "JOB" and entity.get("data").get("latestRun"):
                entity = entity.get("data")
                input_dataset_versions = entity.get("latestRun").get("inputDatasetVersions")
                input_dataset_beans = self.__to_dataset_beans_list(input_dataset_versions)

                output_dataset_versions = entity.get("latestRun").get("outputDatasetVersions")
                out_dataset_beans = self.__to_dataset_beans_list(output_dataset_versions)

                if input_dataset_versions and output_dataset_versions:
                    engine = entity.get("latestRun").get("jobVersion").get("namespace")
                    start_at = entity.get("latestRun").get("startedAt")
                    end_at = entity.get("latestRun").get("endedAt")
                    durations = entity.get("latestRun").get("durationMs")
                    state = entity.get("latestRun").get("state")
                    nodes_lineages.append(NodeLineage(input_dataset_beans, out_dataset_beans, engine, state, start_at, end_at, durations))


        return nodes_lineages

    def __get_node_lineage(self, node_id):
        url = "https://marquez.ack-hk-hackathon.k8s.openprojectx.org/api/v1/lineage?nodeId=" + node_id +"&depth=1000"
        print("collecting lineage from: " + url)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                return self.__parse_lineage_from_json(data)
            else:
                print(f"Error: {response.status_code} - {response.text}")
        except requests.RequestException as e:
            print(f"Request failed: {e}")


    def __remove_dupclicates(self, lst):
        result = []
        for element in lst:
            if element not in result:
                result.append(element)
        return result

    def __multi_ds_lookup(self, input_datasets: list[DatasetBean], output_datasets: list[DatasetBean]):
        valid_combinations = [(a, b) for a in input_datasets for b in output_datasets]
        str_lineages = []
        for combination in valid_combinations:
            input_dataset: DatasetBean = combination[0]
            output_dataset: DatasetBean = combination[1]
            str_lineages.append([input_dataset.get_dataset_name(), output_dataset.get_dataset_name()])
        return str_lineages

    def __flatten_node_lineages(self, node_lineages:list[NodeLineage]):
        str_lineages:list[list[str]] = []
        for node_lineage in node_lineages:
            input_datasets = node_lineage.get_input_datasets()
            output_datasets = node_lineage.get_output_datasets()
            sub_lineages:list[list[str]] = self.__multi_ds_lookup(input_datasets, output_datasets)
            str_lineages.extend(sub_lineages)
        return self.__remove_dupclicates(str_lineages)


    def generate_lineages(self) -> list[DatasetLineageMapping]:
        node_ids = self.__collect_nodes()
        nodes_lineages = []
        for node_id in node_ids:
            node_lineages = self.__get_node_lineage(node_id)
            nodes_lineages.extend(node_lineages)
        flatten_node_lineages = self.__flatten_node_lineages(nodes_lineages)

        session = self.session()
        try:
            # delete all lineage
            sql_query = "DELETE FROM dataset_lineage_mapping"
            session.execute(sql_query)

            # save all lineage
            for lineage in flatten_node_lineages:
                sql = "insert into dataset_lineage_mapping(input_dataset, output_dataset) values('{}', '{}')".format(lineage[0], lineage[1])
                session.execute(sql)

            # Run a SELECT query
            sql_query = "SELECT * FROM dataset_lineage_mapping"
            result = session.execute(sql_query)

            # Map the results to instances of the model class
            rows_as_models = [DatasetLineageMapping(**row) for row in result.fetchall()]
            session.commit()
            return rows_as_models
        except:
            session.rollback()
            raise
        finally:
            session.close()


        for lineage in flatten_node_lineages:
            input_dataset = lineage[0]
            output_dataset = lineage[1]
            session.add(DatasetLineageMapping(input_dataset=input_dataset, output_datset=output_dataset))
        session.commit()
        session.close()

        return flatten_node_lineages
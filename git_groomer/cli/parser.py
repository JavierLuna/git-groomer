import os
from pathlib import Path
from typing import Optional, List

import yaml

from git_groomer.base.objects import Repository
from git_groomer.cli.schemas import CLIRepoSchema, CLIGroomingRuleSchema
from git_groomer.gitlab import GitlabRepository


def _validate_config(config: dict) -> List[dict]:
    repositories = config.get('repositories', [])
    grooming_rules = config.get('grooming_rules', {})

    repo_schema = CLIRepoSchema()
    rule_schema = CLIGroomingRuleSchema()
    all_errors = list()
    all_errors.append(repo_schema.validate(repositories, many=True))
    for rule_name, rule in grooming_rules.items():
        all_errors.append(rule_schema.validate(rule))
    return [error for error in all_errors if error]


def _make_repo(repo_config: dict) -> Repository:
    repo_host = repo_config['host_type'].lower()
    if repo_host == 'gitlab':  # TODO remove this hardcoded bit and make it flexible
        return GitlabRepository(repository_name=repo_config['project_name'], repository_id=repo_config['project_id'],
                                api_token=os.getenv(repo_config['token_from']))
    raise Exception(f"Repository host not recognized: {repo_host}, available repository hosts: [gitlab]")


def _make_config(config: dict) -> dict:
    if 'repository' in config:
        repo_config = config['repository']
        del config['repository']
        config['repositories'] = [repo_config]
        return _make_config(config)
    validation_errors = _validate_config(config)
    if validation_errors:
        raise Exception(f"Configuration not valid: {validation_errors}")

    config['repositories'] = [{'repository': _make_repo(repo_config), 'rules': repo_config.get('grooming_rules', [])}
                              for repo_config in config['repositories']]

    return config


def _read_config_file(config_file: str) -> dict:
    with open(config_file) as input_file:
        document = yaml.safe_load(input_file)
    return document


def _read_default_config_file() -> dict:
    default_config = {}
    default_config_path = str(Path.home().joinpath('.git-groomer.yaml'))
    if os.path.isfile(default_config_path):
        default_config = _read_config_file(default_config_path)

    return default_config


def _read_config_files(config_file: Optional[str]) -> dict:
    resulting_config = _read_default_config_file()

    if config_file:
        custom_config = _read_config_file(config_file)
        custom_config = _make_config(custom_config)

        resulting_config.update(_read_config_file(config_file))

    valid = _make_config(resulting_config)
    print(valid)
    return resulting_config

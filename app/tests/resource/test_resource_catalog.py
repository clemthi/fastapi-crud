import json

from app.resources.catalog import catalog


async def test_load_score_description() -> None:
    score_cat = catalog.get_score_description()
    with open(catalog._file_score_description, encoding='UTF-8') as file:  # pylint: disable=protected-access
        json_content = json.load(file)

    assert len(score_cat) == len(json_content)
    assert score_cat == json_content

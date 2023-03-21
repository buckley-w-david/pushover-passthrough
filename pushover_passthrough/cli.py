import hashlib
import json
from pathlib import Path

from pushover_passthrough.database import Database
from pushover_passthrough.config import Configuration
from pushover_passthrough.pushover import PushoverApplication, PushoverMessage

import jsons
import typer
from xdg_base_dirs import (
    xdg_config_home,
    xdg_data_home,
)

app = typer.Typer()


def serialize(item: PushoverMessage | str) -> str:
    if isinstance(item, str):
        return item
    return json.dumps(jsons.dump(item))


@app.command()
def run(
    db: Path = typer.Option(xdg_data_home() / "pushover-passthrough" / "db.sqlite3"),
    config: Path = typer.Option(
        xdg_config_home() / "pushover-passthrough" / "config.toml"
    ),
):
    db.parent.mkdir(parents=True, exist_ok=True)
    config.parent.mkdir(parents=True, exist_ok=True)

    if not config.exists():
        with open(config, "w") as f:
            f.write('pushover_application_key = ""\npushover_user_token = ""')
        print("Created empty config file: %s" % str(config))
        raise typer.Exit()

    database = Database(db)
    conf = Configuration.load_file(config)
    app = PushoverApplication(conf.pushover_application_key)

    for source in conf.sources:
        items = source.extract()
        for item in items:
            id = hashlib.sha256(serialize(item).encode()).hexdigest()
            if not database.exists(id):
                app.push(conf.pushover_user_token, item)
                database.add(id)

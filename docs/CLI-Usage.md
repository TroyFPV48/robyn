# CLI Usage

## Creating a New Project

To create a new Robyn project, use the `--create` option followed by the desired project type.

python main.py --create --project-type=<project-type>


Replace `<project-type>` with one of the following options:
- `mongo`: Create a MongoDB project
- `postgres`: Create a PostgreSQL project
- `sqlalchemy`: Create a SQLAlchemy project
- `prisma`: Create a Prisma project

**Example:**

To create a new MongoDB project, run:

python main.py --create --project-type=mongo


## Additional Options

Here are some additional options you can use with the `--create` command:

- `--processes`: Choose the number of processes. [Default: 1]
- `--workers`: Choose the number of workers. [Default: 1]
- `--dev`: Enable development mode. It restarts the server based on file changes.
- `--log-level`: Set the log level name. [Default: INFO]
- `--open-browser`: Open the browser on successful server start.

**Example:**

To create a new MongoDB project with 4 processes and 2 workers, and enable development mode, run:

python main.py --create --project-type=mongo --processes=4 --workers=2 --dev

## Docker Configuration

If you want to have Docker in your project, you can add the `--docker` to the `--create` command:

python main.py --create --project-type=<project-type> --docker


**Example:**

To create a new MongoDB project with Docker configuration, run:

python main.py --create --project-type=mongo --docker


Remember to have Docker installed and properly set up on your system.

---
Remember to replace `main.py` with the actual filename of your CLI script. Customize the examples and descriptions based on your specific project's CLI functionality.

Feel free to add more details or sections to the documentation based on the complexity of your CLI and the information you want to convey to users.


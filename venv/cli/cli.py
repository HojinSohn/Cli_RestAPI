import click
import requests

@click.group()
def cli():
    pass

@cli.command()
@click.option('-m', '--method', type=click.Choice(['GET', 'POST', 'PUT', 'DELETE']))
@click.option('-i', '--id', type=int)
@click.option('-t', '--title')
@click.option('-d', '--description')
@click.option('-e', '--timestamp')
def task(method, id, title, description, timestamp):
    args = {}
    print(method, ",", id, ",", title, ",", description, ",", timestamp)
    try:
        if title and description and timestamp:
            args = {
                'title': title,
                'description': description,
                'timestamp': timestamp
            }

        if method == "GET":
            if isinstance(id, int):
                response = requests.get(f'http://127.0.0.1:5000/task/{id}')
                if response.status_code == 200:
                    task = response.json()
                    click.echo(f"Task ID: {task['id']}")
                    click.echo(f"Title: {task['title']}")
                    click.echo(f"Description: {task['description']}")
                    click.echo(f"Timestamp: {task['timestamp']}")
            else:
                response = requests.get('http://127.0.0.1:5000/task')
                if response.status_code == 200:
                    tasks = response.json()
                    for task in tasks:
                        click.echo(f"Task ID: {task['id']}")
                        click.echo(f"Title: {task['title']}")
                        click.echo(f"Description: {task['description']}")
                        click.echo(f"Timestamp: {task['timestamp']}")
                        click.echo("---------")
                else:
                    click.echo("Failed to retrieve tasks.")
        if method == "POST":
            if title and description and timestamp:
                response = requests.post('http://127.0.0.1:5000/task', json=args)
            else:
                click.echo("error")
        if method == "PUT":
            if id:
                if title:
                    args['title'] = title
                if description:
                    args['description'] = description
                if timestamp:
                    args['timestamp'] = timestamp
                response = requests.put(f'http://127.0.0.1:5000/task/{id}', json=args)
            else:
                click.echo("error")
        if method == "DELETE":
            if id:
                response = requests.delete(f'http://127.0.0.1:5000/task/{id}', json=args)
            else:
                click.echo("error")
    except Exception as err:
        click.echo(f"Error: {err}")

    if response.status_code == 200:
        click.echo("success")
    else:
        click.echo("failed")
        click.echo(response.status_code)

if __name__ == '__main__':
    cli()

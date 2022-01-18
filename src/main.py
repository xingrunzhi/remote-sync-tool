import json
import click
import os


@click.command()
@click.option('--setup', is_flag=True, help="Setting up remote directory locations")
def main(setup):
    if setup:
        click.echo('Setting up remote host locations')
    else:
        click.echo('Syncing local files to remote....')
        path = '/Users/xrunzhi/.config/ninja-dev-sync.json'
        with open(path, 'r') as config_file:
            settings = json.load(config_file)
        remote_host = settings['DefaultHost']
        for workspace in settings['Workspaces']:
            sync(workspace, remote_host)


def sync(workspace, remote_host):
    local_dir = workspace['LocalSync']
    remote_dir = workspace['RemoteHost']
    print(local_dir)
    print(remote_dir)

if __name__ == '__main__':
    main()
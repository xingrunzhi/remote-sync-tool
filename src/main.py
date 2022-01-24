import json
import click
import os
import subprocess
import random
import string


@click.command()
@click.option('--setup', is_flag=True, help="Setting up remote directory locations")
def main(setup):
    if setup:
        click.echo('Setting up remote host locations')
    else:
        click.echo('Syncing local files to remote....')
        path = '/Users/xrunzhi/.config/remote-dev-sync.json'
        with open(path, 'r') as config_file:
            settings = json.load(config_file)
        remote_host = settings['DefaultHost']
        for workspace in settings['Workspaces']:
            sync(workspace, remote_host)


def sync(workspace, remote_host):
    local_dir = workspace['LocalSync']
    remote_host = workspace['RemoteHost']
    target_dir = workspace['RemoteSync']
    flags = []
    ssh_flags = [
        "-o", "PasswordAuthentication=no",
        "-o", "ServerAliveInterval=5",
        "-o", "ServerAliveCountMax=2",
        "-o", "ConnectTimeout=10",
        "-o", "ControlMaster=auto",
        "-o", "ControlPersist=30m",
        "-o", "ControlPath=" + get_control_path() + "",
    ]
    ssh_command = ' '.join(['ssh', *ssh_flags])
    rsync(local_dir, remote_host, target_dir, ssh_command, flags)


def get_control_path():
    user_home_dir = os.getenv('HOME')
    letters = string.ascii_lowercase
    random_string = ''.join(random.choice(letters) for i in range(4))
    return user_home_dir + '/.ssh/remote-dev-sync_' + random_string


def rsync(from_host, to_host, target_dir, ssh_command, flags):
    if from_host[-1] != '/':
        from_host += '/'
    target = f'{to_host}:{target_dir}'
    args = ['rsync', '-e', ssh_command, '-rlptzv', '--delete-after', *flags, from_host, target]
    command = subprocess.run(args)
    print(f'rsync [...] {from_host} {target}')


if __name__ == '__main__':
    main()
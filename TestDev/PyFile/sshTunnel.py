import subprocess
import random
import tempfile

class MySshTunnel:

    def __init__(self, remote_host,remote_port,local_host, local_port, user,key):
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.local_host = local_host
        self.local_port = local_port
        self.user = user
        self.key = key


    def start(self):
        pass


class SSHTunnel:

    def __init__(self, host, user, port, key, remote_port):
        self.host = host
        self.user = user
        self.port = port
        self.key = key
        self.remote_port = remote_port
        # Get a temporary file name
        tmpfile = tempfile.NamedTemporaryFile()
        tmpfile.close()
        self.socket = tmpfile.name
        self.local_port = random.randint(10000, 65535)
        self.local_host = '127.0.0.1'
        self.open = False

    def start(self):
        exit_status = subprocess.call(['ssh', '-MfN',
            '-S', self.socket,
            '-i', self.key,
            '-p', self.port,
            '-l', self.user,
            '-L', '{}:{}:{}'.format(self.local_port, self.local_host, self.remote_port),
            '-o', 'ExitOnForwardFailure=True',
            self.host
        ])
        if exit_status != 0:
            raise Exception('SSH tunnel failed with status: {}'.format(exit_status))
        if self.send_control_command('check') != 0:
            raise Exception('SSH tunnel failed to check')
        self.open = True

    def stop(self):
        if self.open:
            if self.send_control_command('exit') != 0:
                raise Exception('SSH tunnel failed to exit')
            self.open = False

    def send_control_command(self, cmd):
        return subprocess.check_call(['ssh', '-S', self.socket, '-O', cmd, '-l', self.user, self.host])

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, type, value, traceback):
        self.stop()


def main():
    with SSHTunnel('localhost', 'eguimard', '9200','','9200') as connect:
        print('conecting')


if __name__ =='__main__':
    main()
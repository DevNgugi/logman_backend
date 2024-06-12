import paramiko
import time

class SSHConnection:
    def __init__(self):
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.log_lines = []
        self.hostname = '165.90.23.196'
        self.port = 8044
        self.username = 'pngugi'
        self.password = 'C0nn4cT140'
        self.read_log()


    def connect(self):
        try:
            self.ssh.connect(self.hostname, port=self.port, username=self.username, password=self.password)
            return True
        except Exception as e:
            print(f"An error occurred while connecting: {e}")
            return False

    def read_log(self):
        try:
            if self.connect():
                command = ('tail -f /var/log/county/ug_county.out.log')
                self.close()
            stdin, stdout, stderr = self.ssh.exec_command(command, get_pty=True)
            while True:
                line = stdout.readline()
                if not line:
                    break
                self.log_lines.append(line.strip())
                print(line.strip())
                time.sleep(0.1)
        except Exception as e:
            print(f"An error occurred while reading log: {e}")

    def close(self):
        self.ssh.close()

# Example usage


if __name__ == "__main__":
    hostname = '165.90.23.196'
    port = 8044
    username = 'pngugi'
    password = 'C0nn4cT140'
    log_reader = SSHLogReader(hostname, port, username, password)
    if log_reader.connect():
        log_reader.read_log('tail -f /var/log/county/ug_county.out.log')
        log_reader.close()
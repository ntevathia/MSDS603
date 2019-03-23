import paramiko
from os.path import expanduser
from user_definition import *


# ## Assumption : Anaconda, Git (configured)

def ssh_client():
    """Return ssh client object"""
    return paramiko.SSHClient()


def ssh_connection(ssh, ec2_address, user, key_file):
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ec2_address, username=user,
                key_filename=expanduser("~") + key_file)
    return ssh


def create_or_update_environment(ssh):
    stdin, stdout, stderr = \
        ssh.exec_command("conda env create -f ~/MSDS603/environment.yml")
    if (b'already exists' in stderr.read()):
        stdin, stdout, stderr = \
            ssh.exec_command("conda env update -f ~/MSDS603/environment.yml")

#msds603_instructor
def git_clone(ssh):
    stdin, stdout, stderr = ssh.exec_command("git --version")
    if (b"" is stderr.read()):
        git_clone_command = "git clone https://github.com/" + \
                            git_user_id + "/" + git_repo_name + ".git"

        git_pull_command = "cd " + git_repo_name + "; git pull origin master"
        
        stdin, stdout, stderr = ssh.exec_command(git_clone_command)
        #print(stdout.read())
        #print(stderr.read())

        a = stderr.read()
    
        if 'fatal' in str(a):
            print("Clone fresh copy!!")
            stdin, stdout, stderr = ssh.exec_command(git_pull_command)
            print(stdout.read())
            print(stderr.read())
    

def main():
    ssh = ssh_client()
    ssh_connection(ssh, ec2_address, user, key_file)
    create_or_update_environment(ssh)
    git_clone(ssh)


if __name__ == '__main__':
    main()

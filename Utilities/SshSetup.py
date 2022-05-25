import os


# don't work again
def setup_ssh_tunnel(port=9200, DNS='test-conformite'):
    if os.system(f'ssh -L {9200}:{DNS}:{port} -Nf {DNS}') == 0:
        return True
    return False


# working
def check_cluster_connected(host='localhost', port=9200):
    if os.system(f'curl {host}:{port}') == 0:
        return True
    return False


'''
if __name__ =='__main__':
    check_cluster_connected()
'''

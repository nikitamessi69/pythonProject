from sem_4.sshcheckers import upload_files, ssh_checkout


def deploy():
    res = []
    upload_files("0.0.0.0", "user2", "assoll1987", "/home/gb/p7zip-full.deb", "/home/user2/p7zip-full.deb")
    res.append(ssh_checkout("0.0.0.0", "user2", "assoll1987", "echo 'assoll1987' | sudo -S dpkg -i "
                                                              "/home/user2/p7zip-full.deb",
                            "Настраивается пакет"))
    res.append(ssh_checkout("0.0.0.0", "user2", "assoll1987", "echo 'assoll1987' | sudo -S dpkg -s p7zip-full",
                            "Status: install ok. installed"))
    return all(res)
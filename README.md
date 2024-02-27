- First, install update the apt repository: 

`sudo apt-get update`

- Next, install mysql-server:

`sudo apt-get install mysql-server`

- Then, create a root user within MYSQL with a password:

`sudo mysql`

`> ALTER USER 'root'@'localhost' IDENTIFIED BY 'MyNewPass';`

- subsequent logins via the CLI as root will be performed using:

`mysql -u root -p`

- allow the root user remote access:

`> GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY 'MyNewPass' WITH GRANT OPTION;`


`> FLUSH PRIVILEGES;`

- Finally, allow mysql to listen on all connections:
  - ensure default port 3306 is allowed:
    `sudo ufw allow 3306`
  - add the following lines to `/etc/mysql/mysql.conf.d/mysql.cnf` and `/etc/mysql/my.cnf`:
    ```
    [mysql]
    bind-address = 0.0.0.0

    [mysqld]
    bind-address = 0.0.0.0
    ```

    ensuring that no other bind-address is set in either file.

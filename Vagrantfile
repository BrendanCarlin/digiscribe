# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "ubuntu/trusty64"
  config.vm.network "forwarded_port", guest: 8000, host: 8000, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 8080, host: 8080, host_ip: "127.0.0.1"
  config.vm.network "forwarded_port", guest: 5000, host: 5000, host_ip: "127.0.0.1"

  # Work around disconnected virtual network cable.
  config.vm.provider "virtualbox" do |vb|
    vb.customize ["modifyvm", :id, "--cableconnected1", "on"]
  end

  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get -qqy update && apt-get -qqy upgrade
    sudo apt-get install -y python-pip
    sudo apt-get install make zip unzip postgresql

    sudo apt-get -qqy install python3
    sudo apt-get -qqy install python3-pip
    sudo pip3 install --upgrade pip
    sudo pip3 install flask
    sudo pip3 install sqlalchemy flask-sqlalchemy psycopg2 bleach

    sudo pip3 install SpeechRecognition
    sudo pip3 install os
    sudo pip3 install csv
    sudo pip3 install sys
    sudo pip3 install subprocess

    wget https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-64bit-static.tar.xz
    tar xvf ffmpeg-git-*.tar.xz
    cd ./ffmpeg-git-*
    sudo cp ff* qt-faststart /usr/local/bin

    vagrantTip="^[[35m^[[1mThe shared directory is located at /vagrant\\nTo access your shared files: cd /vagrant^[[m"
    echo -e $vagrantTip > /etc/motd

    echo "Done installing your virtual machine!"
  SHELL
end

#!/usr/bin/python36


print("content-type:text/html")
print("\n")

import subprocess
import os
import cgi

#VLC 

file4=open("/var/www/cgi-bin/saas_vlc.yml","w")
file4.write(""" - hosts: all
   tasks:
      - yum:
         name: docker-ce
         state: present

      - pip:
         name: docker
         state: latest

      - service:
         name: docker
         state: started

      - copy:
         src: "/root/vlcv2.tar"
         dest: "/root/vlc-v2.tar"

                                                         
      - copy:
         src: "/root/Music/20191113_173646.mp4"
         dest: "/root/Music/test_video.mp4"

      - docker_image:
         name: "vlc:v2"
         load_path: "/root/vlc-v2.tar"
         state: present

      - docker_container:
         name: vlcv2
         image: vlc:v2
         ipc_mode: host
         volumes:
           - /root/:/root/
           - /tmp/.X11-unix:/tmp/.X11-unix                                                #graphical socket sharing
           - /root/Music/test_video.mp4:/root/vid.mp4                                     #random test video file
         devices: /dev/snd:/dev/snd                                                       #audio device sharing
         privileged: yes                                                                  #root user being given the privilege to run vlc
         state: started
         detach: yes
         interactive: yes
         tty: yes

      - command:
         cmd: docker exec vlcv2 sed -i 's/geteuid/getppid/' /usr/bin/vlc


      - command:
         cmd: docker exec vlcv2 bash -c " sed -i \'s/geteuid/getppid/\' /usr/bin/vlc ; vlc"
""")
file4.close()
subprocess.getstatusoutput(" sudo ansible-playbook /var/www/cgi-bin/saas_vlc.yml")





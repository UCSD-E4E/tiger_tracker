#!/bin/bash
bash
#source ~/.bashrc
export CMAKE_PREFIX_PATH="/opt/ros/hydro"
export COLORTERM="gnome-terminal"
export COMPIZ_CONFIG_PROFILE="ubuntu"
export CPATH="/opt/ros/hydro/include"
export DBUS_SESSION_BUS_ADDRESS="unix:abstract=/tmp/dbus-LCPzxBHBtg,guid=13af03dc97c36d8fad015d5600000024"
export DEFAULTS_PATH="/usr/share/gconf/ubuntu.default.path"
export DESKTOP_SESSION="ubuntu"
export DISPLAY=":0.0"
export GDMSESSION="ubuntu"
export GNOME_DESKTOP_SESSION_ID="this-is-deprecated"
export GNOME_KEYRING_CONTROL="/tmp/keyring-r7K3Fh"
export GNOME_KEYRING_PID="2411"
export GPG_AGENT_INFO="/tmp/keyring-r7K3Fh/gpg:0:1"
export HOME="/home/cameratrap"
export LANG="en_US.UTF-8"
export LD_LIBRARY_PATH="/opt/ros/hydro/lib"
export LESSCLOSE="/usr/bin/lesspipe %s %s"
export LESSOPEN="| /usr/bin/lesspipe %s"
export LOGNAME="cameratrap"
export LS_COLORS="rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:su=37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arj=01;31:*.taz=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.zip=01;31:*.z=01;31:*.Z=01;31:*.dz=01;31:*.gz=01;31:*.lz=01;31:*.xz=01;31:*.bz2=01;31:*.bz=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01;31:*.rar=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.jpg=01;35:*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.mpeg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.qt=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=01;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.axv=01;35:*.anx=01;35:*.ogv=01;35:*.ogx=01;35:*.aac=00;36:*.au=00;36:*.flac=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.ogg=00;36:*.ra=00;36:*.wav=00;36:*.axa=00;36:*.oga=00;36:*.spx=00;36:*.xspf=00;36:"
export MANDATORY_PATH="/usr/share/gconf/ubuntu.mandatory.path"
export OLDPWD="/home/cameratrap/Desktop/tiger_tracker"
export PATH="/opt/ros/hydro/bin:/usr/lib/lightdm/lightdm:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games"
export PKG_CONFIG_PATH="/opt/ros/hydro/lib/pkgconfig"
export PWD="/home/cameratrap/Desktop/tiger_tracker/airVision"
export PYTHONPATH="/opt/ros/hydro/lib/python2.7/dist-packages"
export ROSLISP_PACKAGE_DIRECTORIES=""
export ROS_DISTRO="hydro"
export ROS_ETC_DIR="/opt/ros/hydro/etc/ros"
export ROS_MASTER_URI="http://localhost:11311"
export ROS_PACKAGE_PATH="/opt/ros/hydro/share:/opt/ros/hydro/stacks"
export ROS_ROOT="/opt/ros/hydro/share/ros"
export SESSION_MANAGER="local/cameratrap-DX4840:@/tmp/.ICE-unix/2782,unix/cameratrap-DX4840:/tmp/.ICE-unix/2782"
export SHELL="/bin/bash"
export SHLVL="2"
export SSH_AGENT_PID="3452"
export SSH_AUTH_SOCK="/tmp/keyring-r7K3Fh/ssh"
export TERM="xterm"
export UBUNTU_MENUPROXY="libappmenu.so"
export USER="cameratrap"
export WINDOWID="41943046"
export XAUTHORITY="/home/cameratrap/.Xauthority"
export XDG_CONFIG_DIRS="/etc/xdg/xdg-ubuntu:/etc/xdg"
export XDG_CURRENT_DESKTOP="Unity"
export XDG_DATA_DIRS="/usr/share/ubuntu:/usr/share/gnome:/usr/local/share/:/usr/share/"
export XDG_SEAT_PATH="/org/freedesktop/DisplayManager/Seat0"
export XDG_SESSION_COOKIE="e52a6e5097e89548b41e1db50000000f-1383418402.118729-392060290"
export XDG_SESSION_PATH="/org/freedesktop/DisplayManager/Session0"

cd /home/cameratrap/Desktop/tiger_tracker/airVision

python main.py /usr/lib/airvision2/data/videos /media/zoodrive >> /home/cameratrap/Desktop/tiger_tracker/airVision/log.log

#/bin/echo "Hello World" >> /home/cameratrap/cron.log
#/bin/date >> /home/cameratrap/cron.log
#/usr/bin/python /home/cameratrap/Desktop/tiger_tracker/airVision/main.py /usr/lib/airvision2/data/videos /media/zoodrive >> /home/cameratrap/Desktop/tiger_tracker/airVision/log.log



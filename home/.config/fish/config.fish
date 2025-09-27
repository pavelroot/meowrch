#####################################
##==> Variables
#####################################
function shenv
  set -gx $argv
end
source ~/.env

#####################################
##==> Aliases
#####################################
alias cls="clear"
alias g="git"
alias n="nvim"
alias m="micro"

#####################################
##==> Custom Functions
#####################################
function wget
    command wget --hsts-file="$XDG_DATA_HOME/wget-hsts" $argv
end

function nvidia-settings
    mkdir -p $XDG_CONFIG_HOME/nvidia/
    command nvidia-settings --config="$XDG_CONFIG_HOME/nvidia/settings" $argv
end

#####################################
##==> Interactive Session Settings
#####################################
if status is-interactive

end

#####################################
##==> Shell Customization
#####################################
starship init fish | source
set fish_greeting

#####################################
##==> Development Tools
#####################################
##==> Pyenv
pyenv init - | source

#####################################
##==> Fun Stuff
#####################################
pokemon-colorscripts --no-title -s -r 1,3,6

set -U fish_user_paths "$HOME/.local/bin"
set -gx PATH $PATH /home/pavel/flutter/bin
set -gx XCURSOR_THEME Bibata-Modern-Classic
set -gx XCURSOR_SIZE 24
set -gx _JAVA_OPTIONS '-Dawt.useSystemAAFontSettings=on -Dswing.aatext=true -Dswing.defaultlaf=com.sun.java.swing.plaf.gtk.GTKLookAndFeel'
set -gx _JAVA_AWT_WM_NONREPARENTING 1

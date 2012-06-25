###########################################################
###                                                     ###
### Panda3D Configuration File -  User-Editable Portion ###
###                                                     ###
###########################################################

# Uncomment one of the following lines to choose whether you should
# run using OpenGL or DirectX rendering.

load-display pandagl

cursor-hidden 	#f

# These control the placement and size of the default rendering window.

win-origin 50 50
win-size 1024 768

# Uncomment this line if you want to run Panda fullscreen instead of
# in a window.

fullscreen #t

# If you don't object to running OpenGL in software leave the keyword
# "software" in the following line, otherwise remove it to force
# hardware only.

# framebuffer-mode rgba double-buffer depth hardware

# These control the amount of output Panda gives for some various
# categories.  The severity levels, in order, are "spam", "debug",
# "info", "warning", and "fatal"; the default is "info".  Uncomment
# one (or define a new one for the particular category you wish to
# change) to control this output.

notify-level warning
default-directnotify-level warning

# These specify where model files may be loaded from.  You probably
# want to set this to a sensible path for yourself.  $THIS_PRC_DIR is
# a special variable that indicates the same directory as this
# particular Config.prc file.

#model-path    .
#model-path    $THIS_PRC_DIR/..
#model-path    $THIS_PRC_DIR/../models
#sound-path    .
#sound-path    $THIS_PRC_DIR/..
#sound-path    $THIS_PRC_DIR/../models
#texture-path  .
#texture-path  $THIS_PRC_DIR/..
#texture-path  $THIS_PRC_DIR/../models

# This enable the automatic creation of a TK window when running
# Direct.

want-directtools  #f
want-tk           #f

# Enable/disable performance profiling tool and frame-rate meter

want-pstats            #f
show-frame-rate-meter  #f

# Enable audio using the FMod audio library by default:

#audio-library-name fmod_audio

# The new version of panda supports hardware vertex animation, but it's not quite ready

hardware-animated-vertices 0


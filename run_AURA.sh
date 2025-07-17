#!/bin/bash

# Terminal 1 - Start Docker container
gnome-terminal -- bash -c "cd \$HOME/hri_software/docker && ./run.bash; exec bash"
sleep 1

# Terminal 2 - Run MODIM NGINX server
gnome-terminal -- bash -c "cd \$HOME/hri_software/docker && ./run_nginx.bash \$HOME/playground/AURA; exec bash"
sleep 1

# Terminal 3 - Attach to tmux inside container
gnome-terminal -- bash -c "docker exec -it pepperhri tmux a; exec bash"



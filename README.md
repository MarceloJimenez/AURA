# AURA-Care: Human-Robot Interaction System for Elderly Care

## Overview

This project presents **AURA-Care**, a socially intelligent human-robot interaction (HRI) system designed to support elderly individuals in daily health-related tasks, such as medication intake. It incorporates social reasoning, adaptive behaviors, and a multimodal interface. The system was developed and evaluated within the scope of the Human-Robot Interaction and Robot Benchmarking & Competition (HRI & RBC) course at Sapienza University of Rome.

This document provides instructions for deploying and running the AURA-Care system using a Docker container, simulating sensory inputs, and launching the interactive web interface.

---

## 1. Prerequisites

Before building the Docker container, clone the following repository:

```bash
git clone https://bitbucket.org/iocchi/hri_software.git
cd hri_software/docker
```

Ensure to edit the `Dockerfile` by adding the following line before building:

```dockerfile
apt install -y espeak &&
```

This enables simulated speech through the `espeak` synthesizer.

---

## 2. Docker Build and Execution

### 2.1 Build the Docker Image

Follow the instructions provided at:

> [https://bitbucket.org/iocchi/hri\_software/src/7ee6a9cdb3c3d3ebf437b52c2f1ab42050aa829e/docker/README.md](https://bitbucket.org/iocchi/hri_software/src/7ee6a9cdb3c3d3ebf437b52c2f1ab42050aa829e/docker/README.md)

### 2.2 Run the Docker Container

```bash
cd hri_software/docker
./run.bash
```

---

## 3. Inside the Docker Container

Open a new terminal and attach to the running container using:

```bash
docker exec -it pepperhri tmux a
```

You will enter a pre-configured `tmux` session with several windows. To navigate between them, press:

```
Ctrl+b → release → w
```

If needed, new windows can be created, and the following commands should be executed in separate panes:

### 3.1 Launch Naoqi Framework

```bash
cd /opt/Aldebaran/naoqi-sdk-2.5.7.1-linux64
./naoqi
```

### 3.2 Start MODIM Server

```bash
cd ~/src/modim/src/GUI
python ws_server.py -robot pepper
```

---

## 4. Running the Web Server (on Host OS)

To launch the web interface for the custom AURA-Care demo:

```bash
cd hri_software/docker
./run_nginx.bash $HOME/playground/AURA
```

Access it in your browser at:

> [http://localhost](http://localhost)

---

## 5. Launch AURA-Care Demo

Inside the Docker container:

```bash
cd ~/playground/AURA/scripts
python start.py
```

---

## 6. Simulating Sensor Inputs

To simulate the robot's front sonar sensor (in a new tmux window):

```bash
cd $PEPPER_TOOLS_HOME/sonar
python sonar_sim.py --sensor SonarFront --value 0.75
```

To simulate a head touch:

```bash
cd $PEPPER_TOOLS_HOME/touch
python touch_sim.py --sensor HeadMiddle --duration 2.5
```

---

## 7. Docker Utility Commands

Monitor and manage Docker containers with:

```bash
docker ps                  # List running containers
docker container ls        # List all containers
docker stop <container_id> # Stop container
docker rm <container_id>   # Remove container
```

---

## 8. Academic Context

This project was developed by Marcelo Jiménez, Edgar Cancino, and Enrique Favila during the 2024/2025 academic year at Sapienza University of Rome under the guidance of Professors Luca Iocchi and Vincenzo Suriani. The AURA-Care system was evaluated in elderly care scenarios and demonstrated personalized, empathetic behavior through multi-modal interaction channels. The effectiveness of the robot’s social intelligence was assessed experimentally using both quantitative metrics and qualitative feedback.

---


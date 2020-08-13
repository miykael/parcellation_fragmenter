#Generate Dockerfile.

#!/bin/sh

 set -e


generate_docker() {
  docker run --rm kaczmarj/neurodocker:0.5.0 generate docker \
             --base neurodebian:stretch-non-free \
             --pkg-manager apt \
             --install git num-utils gcc g++ curl build-essential\
             --miniconda \
                conda_install="python=3.6 networkx nibabel numpy scipy
                              sklearn jupyter" \
                create_env='par_frag' \
                activate=true \
             --copy . /home/pf \
             --run-bash "source activate par_frag && cd /home/pf && pip install -e ." \
             --env IS_DOCKER=1 \
             --workdir '/home/' \
             --entrypoint "/neurodocker/startup.sh"
}

generate_singularity() {
  docker run --rm kaczmarj/neurodocker:0.5.0 generate singularity \
              --base neurodebian:stretch-non-free \
              --pkg-manager apt \
              --install git num-utils gcc g++ curl build-essential\
              --miniconda \
                 conda_install="python=3.6 networkx nibabel numpy scipy
                               sklearn jupyter" \
                 create_env='par_frag' \
                 activate=true \
              --copy . /home/pf \
              --run-bash "source activate par_frag && cd /home/pf && pip install -e ." \
              --env IS_DOCKER=1 \
              --workdir '/home/' \
              --entrypoint "/neurodocker/startup.sh"
}

# generate files
generate_docker > Dockerfile
generate_singularity > Singularity

# check if images should be build locally or not
if [ '$1' = 'local' ]; then
  if [ '$2' = 'docker' ]; then
    echo "docker image will be build locally"
    # build image using the saved files
    docker build -t parcellation_fragmenter:test .
  elif [ '$2' = 'singularity']; then
    echo "singularity image will be build locally"
    # build image using the saved files
    singularity build parcellation_fragmenter.simg Singularity
  elif [ '$2' = 'both' ]; then
    echo "docker and singularity images will be build locally"
    # build images using the saved files
    docker build -t parcellation_fragmenter:test .
    singularity build parcellation_fragmenter.simg Singularity
  elif [ -z "$2" ]; then
    echo "Please indicate which image should be build. You can choose from docker, singularity or both."
  fi
else
  echo "Image(s) won't be build locally."
fi

trying out building a docker image that can run on any cluster


to build:
docker build -t rubin_sched_cluster:0.1 .

to run interactive, mount my rubin_sim_data:
docker run -v ~/rubin_sim_data:/root/rubin_sim_data -it rubin_sched_cluster:0.1


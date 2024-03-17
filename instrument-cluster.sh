podman run -it -d \
  -e DISPLAY=:0 \
  -e XDG_RUNTIME_DIR=/tmp/runtime-root \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  -v /usr/lib/aarch64-linux-gnu:/usr/lib/aarch64-linux-gnu:ro \
  -v /dev/dri:/dev/dri \
  -v ${INSTRUMENTCLUSTER}:/var/app/InstrumentCluster \
  --privileged \
  --cap-add SYS_ADMIN \
  --restart=always \
  localhost/instrumentcluster.v1

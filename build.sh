version=$(cat version.json \
  | grep version \
  | head -1 \
  | awk -F: '{gsub(/"/,"",$2);gsub(/[[:space:]]*/,"",$2); print $2}' \
  | sed 's/[",]//g')
echo $version

./docker_build/run-project-bake dl_control_api --set "dl_control_api.tags=akrasnov87/datalens-control-api:$version"
./docker_build/run-project-bake dl_data_api --set "dl_data_api.tags=akrasnov87/datalens-data-api:$version"
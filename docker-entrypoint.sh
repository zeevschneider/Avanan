#!/bin/bash

config_file="/var/run/configs/okro.io/deploy/config.yaml"

debug=$(shyaml get-value userConfig.debug < ${config_file} 2>/dev/null)
markers=$(shyaml get-value userConfig.markers < ${config_file} 2>/dev/null)

if [ -n "$debug" ] && [ "${debug,,}" = "true" ]; then
  mkdir -p /var/run/sshd
  chown -R debug /tests
  echo "Starting SSH Server..."
  /usr/sbin/sshd -D
else
  . /tests/.venv/bin/activate
  if [ -z "$markers" ]; then
    (pytest -v -s --html=report.html tests || true) 2>&1 | tee output.log
  else
    (pytest -v -s -m "$markers" --html=report.html tests || true) 2>&1 | tee output.log
  fi
  python3 -m sinker

  # Sent kill request to istio-proxy
  curl -X POST "http://127.0.0.1:15000/quitquitquit"
  exit 0
fi

FROM ubuntu:18.04

ARG DEBIAN_FRONTEND=noninteractive

############################################
# base tool
############################################
RUN apt-get update
RUN apt-get install -y --no-install-recommends apt-utils

###############################################
# cron
###############################################
RUN apt-get install cron

###############################################
# entry point
###############################################
RUN touch /usr/sbin/entrypoint.sh
RUN chmod 777 /usr/sbin/entrypoint.sh

ENTRYPOINT ["/usr/sbin/entrypoint.sh"]
# Docker file for an Ubuntu-based Python3 image
FROM apache/airflow:2.3.2-python3.9
ENV DEBIAN_FRONTEND=noninteractive

USER root
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    zlib1g-dev libz-dev libxml2 libxml2-dev libxslt1-dev libsasl2-dev libsasl2-2 libsasl2-modules-gssapi-mit g++ \
  && apt-get autoremove -yqq --purge \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*


RUN groupadd --gid 999 docker \
    && usermod -aG docker airflow

USER airflow



RUN python -m pip install --upgrade pip

#COPY requirements.txt ./
COPY business_requirements.txt ./
#COPY pip.conf ./
#ENV PIP_CONFIG_FILE=./pip.conf
#RUN pip install -r requirements.txt
RUN pip install -r business_requirements.txt

#COPY adtf/license/adtf2.lic /etc/

############################################
# tutaj sa instalowane depsy
# wiec dobra okazja jest aby skopiowac tutaj core repo
# i pozniej odpalic z poziomu serwisu: pewnie wtedy trzeba dostowac
# tak ze nie korzysta assess_setup z postgres
# tylko korzysta z tego samego co scheduler i webserver
#
#############################################

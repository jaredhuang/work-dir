{% if grains['osfinger'] == 'CentOS-6' %}
syslog: rsyslog
{% elif grains['osfinger'] == 'Centos-5' %}
syslog: syslog
{% endif %}

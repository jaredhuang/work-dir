base:
  'roles:nginx':
    - match: grain
    - init.env_init
prod:
  'roles:nginx':
    - match: grain
    - cluster.haproxy-outside
    - cluster.haproxy-outside-keepalived
    - memcached.service
    - web.bbs

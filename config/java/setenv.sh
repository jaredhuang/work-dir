export JAVA_OPTS="-Djava.awt.headless=true -Dfile.encoding=UTF-8 -server -Xms2048m -Xmx2048m -XX:PermSize=512m -XX:MaxPermSize=1024m -XX:+DisableExplicitGC -Xverify:none -da"
export JAVA_HOME="/usr/local/jdk"
export CLASS_PATH="$JAVA_HOME/lib:$JAVA_HOME/jre/lib"
export PATH="/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin:/root/bin"
export PATH=".:$PATH:$JAVA_HOME/bin"
export JRE_HOME="/usr/local/jdk/jre"
export CATALINA_HOME="/usr/local/$Name_Tomcat"
export JAVA_HOME CATALINA_HOME

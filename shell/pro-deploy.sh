#!/bin/bash
# Date/Time
CTIME=$(date "+%Y-%m-%d-%H-%M")

#Shell
CODE_DIR="/deploy/code/deploy"
CONFIG_DIR="/deploy/config"
TMP_DIR="/deploy/tmp"
TAR_DIR="/deploy/tar"

usage(){
    echo $"Usage: $0 [deploy | rollback-list | rollback-pro ver]"
}  

git_pro(){
    echo "begin git pull"
    cd "$CODE_DIR" &&  git pull
    API_VERL=$(git show |grep commit |cut -d ' ' -f2)
    API_VER=$(echo $API_VERL:0:6)
    cp -r "$CODE_DIR" "$TMP_DIR"
}

config_pro(){
    echo "copy pro config to dir"
    /bin/cp "$CONFIG_DIR"/* $TMP_DIR/deploy/
    TAR_VER="$API_VER"-"$CTIME"
    cd $TMP_DIR && mv deploy pro_deploy_"$TAR_VER" 
}

tar_pro(){
    echo "begin tar"
    cd $TMP_DIR && tar czf pro_deploy_"$TAR_VER".tar.gz pro_deploy_"$TAR_VER"
    echo "tar end pro_deploy_"$TAR_VER".tar.gz"
}

scp_pro(){
    echo "begin scp"
    /bin/cp $TMP_DIR/pro_deploy_"$TAR_VER".tar.gz /opt
    #scp $TMP_DIR/pro_deploy_"$TAR_VER".tar.gz 192.168.1.2:/opt
    #scp $TMP_DIR/pro_deploy_"$TAR_VER".tar.gz 192.168.1.3:/opt
}

deploy_pro(){
    echo                
}

test_pro(){

}

rollback_list(){

}

rollback_pro(){

}

main(){
    case $1 in
        deploy)
            git_pro;
	    config_pro;
	    tar_pro;
	    scp_pro;
            deploy_pro;
            test_pro;
	    ;;
        rollback_list)
            rollback_list;
            ;;
        rollback_pro)
	    rollback_pro $2;
            ;;
        *)
	    usage;
    esac
}
main $1 $2

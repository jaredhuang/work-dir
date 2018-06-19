1. 支持 tomcat 框架：
    https://blog.csdn.net/u013468915/article/details/51992745

2. 运行 mvn clean install 安装到仓库了,其他项目就能直接引用里面的类了: 
    [INFO] Installing /data/gitlab-test/target/ROOT.war to
    /root/.m2/repository/com/github/ningg/mvnbook/hello-world/1.0-SNAPSHOT/hello-world-1.0-SNAPSHOT.war
    [INFO] Installing /data/gitlab-test/pom.xml to
    /root/.m2/repository/com/github/ningg/mvnbook/hello-world/1.0-SNAPSHOT/hello-world-1.0-SNAPSHOT.pom

3. 使用Archetype生成项目骨架

    Hello World项目中有一些Maven的约定：

        pom.xml在项目的根目录；
        主代码在src/main/java/目录下；
        测试代码在src/test/java/目录下；

    我们称这些基本的目录结构和pom.xml文件内容为项目的骨架。每次创建项目都要手动创建项目骨架，会让程序员不高兴，为此，Maven提供了Archetype以帮助我们快速勾勒出项目骨架。

    以Hello World为例，我们使用maven
    archetype来创建该项目的骨架，新建一个Maven项目目录。

    如果是Maven3，简单运行：

        mvn archetype:generate

    实际上，我们运行的是maven-archetype-plugin插件，其输入格式是：groupId:
    artifactId: version: goal
    ，注意冒号的分隔。紧接着，我们会看到很长的输出，有很多可用的archetype供我们选择，包括注明的Appfuse项目、JPA项目的archetype等等。每一个archetype前面都会对应一个编号，同时命令行会提示一个默认的编号，对应archetype为maven-archetype-quickstart，直接回车选择该archetype，紧接着Maven会提示我们输入要创建的项目的groupId，artifactId，version以及包名（package，默认与groupId和artifactId保持对应关系），具体如下：


        Define value for property 'groupId': : com.github.ningg.mvnbook
        Define value for property 'artifactId': : hello-world-archetype
        Define value for property 'version':  1.0-SNAPSHOT: :
        Define value for property 'package':  com.github.ningg.mvnbook: :
    com.github.ningg.mvnbook.helloworldarchetype
        Confirm properties configuration:
        groupId: com.github.ningg.mvnbook
        artifactId: hello-world-archetype
        version: 1.0-SNAPSHOT
        package: com.github.ningg.mvnbook.helloworldarchetype
         Y: : Y
        [INFO]
    ----------------------------------------------------------------------------
        [INFO] Using following parameters for creating project from Old (1.x)
    Archetype: maven-archetype-quickstart:RELEASE
        [INFO]
    ----------------------------------------------------------------------------
        [INFO] Parameter: groupId, Value: com.github.ningg.mvnbook
        [INFO] Parameter: packageName, Value:
    com.github.ningg.mvnbook.helloworldarchetype
        [INFO] Parameter: package, Value:
    com.github.ningg.mvnbook.helloworldarchetype
        [INFO] Parameter: artifactId, Value: hello-world-archetype
        [INFO] Parameter: basedir, Value: E:\reference\blogOfGit\maven-intro
        [INFO] Parameter: version, Value: 1.0-SNAPSHOT
        [INFO] project created from Old (1.x) Archetype in dir:
    E:\reference\blogOfGit\maven-intro\hello-world-archetype
        [INFO]
    ------------------------------------------------------------------------
        [INFO] BUILD SUCCESS
        ...


    运行完毕之后，在当前目录下会生成一个hello-world-archetype目录，其下是一个完整的项目骨架。


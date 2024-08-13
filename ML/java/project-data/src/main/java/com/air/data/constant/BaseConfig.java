package com.air.data.constant;

import org.aeonbits.owner.Config;
import org.aeonbits.owner.Config.Sources;

@Sources("classpath:application.properties")
public interface BaseConfig extends Config {

    /**
     * get app name
     *
     * @return
     */
    @Key("app.name")
    String appName();

    /**
     * get app master
     *
     * @return
     */
    @Key("app.master")
    String appMaster();

    @Key("base.path")
    String basePath();

    @Key("mysql.url")
    String mysqlUrl();

    @Key("mysql.user")
    String mysqlUser();

    @Key("mysql.password")
    String mysqlPassword();
}

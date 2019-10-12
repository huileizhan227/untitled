package com.netease.lede.coco.server;

import javax.servlet.http.HttpServlet;
import java.io.File;
import java.io.InputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.util.Properties;

public class Constant {

  private static volatile String baseDir;
  private static volatile String reportUrl;

  public static String getReportDir(HttpServlet s) {
    return baseDir != null ? baseDir : getConf(s, "report_dir");
  }

  public static String getReportUrl(HttpServlet s) {
    return reportUrl != null ? reportUrl  : getConf(s, "report_url");
  }

  private synchronized static String getConf(HttpServlet s, String confName) {
    // File f = new File(s.getServletContext().getRealPath("WEB-INF/conf.cfg"));
    InputStream inputStream = Constant.class.getClassLoader().getResourceAsStream("conf.cfg");
    String confValue = "";
    Properties p = new Properties();
    try {
      // p.load(new FileInputStream(f));
      p.load(inputStream);
      confValue = p.getProperty(confName);
    } catch (IOException e) {
      e.printStackTrace();
    }
    return confValue;
  }
}

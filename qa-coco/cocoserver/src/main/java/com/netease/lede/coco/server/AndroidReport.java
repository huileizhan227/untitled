package com.netease.lede.coco.server;

import com.netease.lede.androidcoco.report.Report;

import org.jacoco.core.tools.CoCoConstants;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class AndroidReport
 */
@WebServlet("/android/report")
public class AndroidReport extends HttpServlet {
  private SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd_HH-mm-ss", Locale.getDefault());

  private static final long serialVersionUID = 1L;

  /**
   * @see HttpServlet#HttpServlet()
   */
  public AndroidReport() {
    super();
  }

  /**
   * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
   */
  protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    System.out.println("AndroidReport");
    String baseDir = Constant.getReportDir(this);
    File baseF = new File(baseDir);
    if (baseF.exists()) {
      String uniId = request.getParameter(CoCoConstants.INSERT_VALUE_UID);
      File folder = new File(baseDir + File.separator + uniId);
      if (folder.exists()) {
        try {
          String s[] = Report.prepareReport(folder.getAbsolutePath());

          File reportF = new File(folder.getAbsolutePath() + File.separator + CoCoConstants.REPORT_FOLDER_NAME);
          if (reportF.exists()) {
            Tools.deleteFolder(reportF);
          }
          reportF.mkdirs();
          Report.report(s[0], s[1], s[2], s[3], reportF.getAbsolutePath());
          new File(folder.getAbsolutePath() + File.separator + CoCoConstants.REPORT_FOLDER_NAME + File.separator
              + CoCoConstants.RECORD_TIME_PREFIX + sdf.format(new Date(System.currentTimeMillis()))).createNewFile();
          // String indexStr = Constant.getReportUrl(this) + uniId + File.separator + CoCoConstants.REPORT_FOLDER_NAME + "/index.html";
//          response.sendRedirect(indexStr);
          System.out.println("AndroidReport ok!");
        } catch (Exception e) {
          response.sendError(500, "error on preparing!");
          System.out.println("AndroidReport error on preparing!");
          e.printStackTrace();
        }
      } else {
        response.sendError(500, "error staff not exist!");
        System.out.println("AndroidReport error staff not exist!");
      }
    }
  }

  /**
   * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
   */
  protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    doGet(request, response);
  }

}

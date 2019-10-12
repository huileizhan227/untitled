package com.netease.lede.coco.server;

import org.jacoco.core.tools.CoCoConstants;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.File;
import java.io.IOException;

/**
 * Servlet implementation class AndroidDelete
 */
@WebServlet("/android/delMerge")
public class AndroidDeleteMerge extends HttpServlet {
  private static final long serialVersionUID = 1L;

  /**
   * @see HttpServlet#HttpServlet()
   */
  public AndroidDeleteMerge() {
    super();
  }

  /**
   * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
   */
  protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    System.out.println("AndroidDeleteMerge");
    String baseDir = Constant.getReportDir(this);
    File baseF = new File(baseDir);
    if (baseF.exists()) {
      String uniId = request.getParameter(CoCoConstants.INSERT_VALUE_UID);
      String mergeId = request.getParameter(CoCoConstants.MERGE_VALUE_MERGE_ID);
      File folder = new File(baseDir + File.separator + uniId + File.separator
          + CoCoConstants.MERGE_REPORT_FOLDER_NAME + File.separator + mergeId);
      if (folder.exists()) {
        Tools.deleteFolder(folder);
        response.getWriter().append("del ok");
        System.out.println("AndroidDeleteMerge del ok");
      } else {
        response.sendError(500, "error staff not exist!");
        System.out.println("AndroidDeleteMerge error staff not exist");
      }
    } else {
      response.sendError(500, "base dir not exist!");
      System.out.println("AndroidDeleteMerge base dir not exist!");
    }
  }

  /**
   * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
   */
  protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    doGet(request, response);
  }

}

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
@WebServlet("/android/del")
public class AndroidDelete extends HttpServlet {
  private static final long serialVersionUID = 1L;

  /**
   * @see HttpServlet#HttpServlet()
   */
  public AndroidDelete() {
    super();
  }

  /**
   * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
   */
  protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    System.out.println("AndroidDelete");
    String baseDir = Constant.getReportDir(this);
    File baseF = new File(baseDir);
    if (baseF.exists()) {
      String uniId = request.getParameter(CoCoConstants.INSERT_VALUE_UID);
      File folder = new File(baseDir + File.separator + uniId);
      if (folder.exists()) {
        Tools.deleteFolder(folder);
        new File(folder.getAbsolutePath() + ".zip").delete();
        response.getWriter().append("del ok");
        System.out.println("AndroidDelete del ok");
      } else {
        response.sendError(500, "error staff not exist!");
        System.out.println("AndroidDelete error staff not exist");
      }
    } else {
      response.sendError(500, "base dir not exist!");
      System.out.println("AndroidDelete base dir not exist!");
    }
  }

  /**
   * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
   */
  protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    doGet(request, response);
  }

}

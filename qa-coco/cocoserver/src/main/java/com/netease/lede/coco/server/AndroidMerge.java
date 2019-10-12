package com.netease.lede.coco.server;

import com.netease.lede.androidcoco.report.Merge;
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
@WebServlet("/android/merge")
public class AndroidMerge extends HttpServlet {
  private static final long serialVersionUID = 1L;

  /**
   * @see HttpServlet#HttpServlet()
   */
  public AndroidMerge() {
    super();
  }

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse
	 *      response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		System.out.println("AndroidMerge");
		String baseDir = Constant.getReportDir(this);
		File baseF = new File(baseDir);
		if (baseF.exists()) {
			String fromUid = request.getParameter(CoCoConstants.MERGE_VALUE_MERGE_FROM_UID);
			String toUid = request.getParameter(CoCoConstants.MERGE_VALUE_MERGE_TO_UID);
			String fromMid = request.getParameter(CoCoConstants.MERGE_VALUE_MERGE_FROM_MID);
			fromMid = fromMid == null ? null : (fromMid.length() == 0 ? null : fromMid);
			String toMid = request.getParameter(CoCoConstants.MERGE_VALUE_MERGE_TO_MID);
			toMid = toMid == null ? null : (toMid.length() == 0 ? null : toMid);
			try {
				if (fromUid.split("/").length > 1) {
					Merge.mergeMultiReport(baseF.getAbsolutePath(), fromUid.split("/"), toUid);
				} else {
					String args[] = Merge.prepareMerge(new File(baseF.getAbsolutePath() + File.separator + fromUid),
							fromMid, new File(baseF.getAbsolutePath() + File.separator + toUid), toMid);
					Merge.merge(new File(args[0]), new File(args[1]), new File(args[2]), new File(args[3]), args[4]);
				}
				response.getWriter().append("AndroidMerge ok");
				System.out.println("AndroidMerge ok");
			} catch (Exception e) {
				e.printStackTrace();
				response.sendError(500, "error:" + e.getMessage());
				System.out.println("AndroidMerge error :" + e.getMessage());
			}
		} else {
			response.sendError(500, "base dir not exist!");
			System.out.println("AndroidMerge base dir not exist!");
		}
	}

  /**
   * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
   */
  protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    doGet(request, response);
  }

}

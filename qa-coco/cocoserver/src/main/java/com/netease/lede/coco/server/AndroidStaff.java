package com.netease.lede.coco.server;

import org.jacoco.core.tools.CoCoConstants;

import java.io.File;
import java.io.IOException;
import java.io.InputStream;
import java.net.URLEncoder;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.Locale;

import javax.servlet.ServletException;
import javax.servlet.annotation.MultipartConfig;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.Part;

/**
 * Servlet implementation class AndroidStaff
 */
@MultipartConfig
@WebServlet("/android/staff")
public class AndroidStaff extends HttpServlet {
	private SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd_HH-mm-ss", Locale.getDefault());

	private static final long serialVersionUID = 1L;

	/**
	 * @see HttpServlet#HttpServlet()
	 */
	public AndroidStaff() {
		super();
	}

	/**
	 * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse
	 *      response)
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		doPost(request, response);
	}

	/**
	 * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse
	 *      response)
	 */
	protected void doPost(HttpServletRequest request, HttpServletResponse response)
			throws ServletException, IOException {
		System.out.println("AndroidStaff");
		String baseDir = Constant.getReportDir(this);
		File baseF = new File(baseDir);
		if (baseF.exists()) {
			String timeStr = request.getParameter(CoCoConstants.INSERT_VALUE_TIME);
			String uniId = request.getParameter(CoCoConstants.INSERT_VALUE_UID);
			String customTag = request.getParameter(CoCoConstants.UPLOAD_TAG);
			customTag = new String(customTag.getBytes("ISO-8859-1"), "utf-8");
			String project = request.getParameter("project");
			project = new String(project.getBytes("ISO-8859-1"), "utf-8");
			String version = request.getParameter("version");
			System.out.println("project:" + project);
			System.out.println("version" + version);

			customTag = customTag == null ? "UnknowTag" : customTag;
			System.out.println("customTag" + customTag);
			File zipFile = new File(baseDir + File.separator + uniId + ".zip");
			if (!zipFile.exists()) {
				zipFile.createNewFile();
				Part filePart = request.getPart(CoCoConstants.UPLOAD_STAFF_NAME);
				InputStream fileContent = filePart.getInputStream();
				Tools.saveToFile(fileContent, zipFile);
				Tools.unzip(zipFile.getAbsolutePath(), baseDir + File.separator + uniId);
				new File(baseDir + File.separator + uniId + File.separator + CoCoConstants.RECORD_TIME_PREFIX
						+ sdf.format(new Date(System.currentTimeMillis()))).createNewFile();
				new File(
						baseDir + File.separator + uniId + File.separator + CoCoConstants.RECORD_TAG_PREFIX + customTag)
								.createNewFile();
				response.getWriter().append("ok");
				System.out.println("AndroidStaff ok");
			} else {
				response.sendError(500, "error file exist!");
				System.out.println("AndroidStaff error file exist!");
			}
		}
	}

}

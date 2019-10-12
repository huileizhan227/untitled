package com.netease.lede.coco.server;

import com.netease.lede.androidcoco.report.Report;

import org.jacoco.core.tools.CoCoConstants;

import java.io.File;
import java.io.FileFilter;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;

import javax.servlet.ServletException;
import javax.servlet.annotation.MultipartConfig;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.Part;

/**
 * Servlet implementation class AndroidRuntime
 */
@MultipartConfig
@WebServlet("/android/runtime")
public class AndroidRuntime extends HttpServlet {

	private SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd_HH-mm-ss", Locale.getDefault());

	private static final long serialVersionUID = 1L;

	/**
	 * @see HttpServlet#HttpServlet()
	 */
	public AndroidRuntime() {
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
		System.out.println("AndroidRuntime");
		String baseDir = Constant.getReportDir(this);
		File baseF = new File(baseDir);
		if (baseF.exists()) {
			String upLoadTime = sdf.format(new Date(System.currentTimeMillis()));
			String timeStr = request.getParameter(CoCoConstants.INSERT_VALUE_TIME);
			String uniId = request.getParameter(CoCoConstants.INSERT_VALUE_UID);
			String mergeId = request.getParameter(CoCoConstants.MERGE_VALUE_MERGE_ID);
			File folder = new File(baseDir + File.separator + uniId);
			if (folder.exists()) {
				File rtF = new File(folder.getAbsolutePath() + File.separator + CoCoConstants.RUNTIME_FOLDER_NAME);
				File hisRtF = new File(
						folder.getAbsolutePath() + File.separator + CoCoConstants.HISTORY_RUNTIME_FOLDER_NAME);
				InputStream fileContent = null;
				if (mergeId != null && mergeId.length() > 0) {
					File mergeRtFile = new File(baseDir + File.separator + uniId + File.separator
							+ CoCoConstants.MERGE_REPORT_FOLDER_NAME + File.separator + mergeId + File.separator
							+ CoCoConstants.RT_FILE_PREFIX + CoCoConstants.RT_FILE_TAIL);
					if (mergeRtFile.exists()) {
						fileContent = new FileInputStream(mergeRtFile);
					} else {
						response.sendError(500, "error mergeRtFile not exist!");
						System.out.println("AndroidRuntime error mergeRtFile not exist");
						return;
					}
				} else {
					Part filePart = request.getPart(CoCoConstants.UPLOAD_RT_NAME);
					fileContent = filePart.getInputStream();
				}
				if (rtF.exists()) {
					// 第二次以上
					File rtFile2 = new File(hisRtF.getAbsolutePath() + File.separator + CoCoConstants.RT_FILE_PREFIX
							+ "_" + upLoadTime + CoCoConstants.RT_FILE_TAIL);
					rtFile2.createNewFile();
					Tools.saveToFile(fileContent, rtFile2);

					// 合并 ，每次拿新的一个和上一次的结果合并
					File rtFile = new File(rtF.getAbsolutePath() + File.separator + CoCoConstants.RT_FILE_PREFIX
							+ CoCoConstants.RT_FILE_TAIL);
					File[] timeFiles = rtF.listFiles(new FileFilter() {

						@Override
						public boolean accept(File pathname) {
							if (pathname.getName().endsWith(".time")) {
								System.out.println("pathName:" + pathname.getName());
								return true;
							}
							return false;
						}
					});

					for (File file : timeFiles) {
						if (file.exists()) {
							file.delete();
						}
					}
					File rtFileTime = new File(rtF.getAbsolutePath() + File.separator + upLoadTime + ".time");
					rtFileTime.createNewFile();
					List<String> srcList = new ArrayList<String>();
					srcList.add(rtFile2.getAbsolutePath());
					srcList.add(rtFile.getAbsolutePath());
					Report.mergeRuntimeData(srcList, rtFile.getAbsolutePath());
					response.getWriter().append("ok the " + upLoadTime + " upload");
					System.out.println("AndroidRuntime ok the " + upLoadTime + " upload");
				} else {
					// 首次上传
					rtF.mkdirs();
					hisRtF.mkdirs();
					File rtFile = new File(rtF.getAbsolutePath() + File.separator + CoCoConstants.RT_FILE_PREFIX
							+ CoCoConstants.RT_FILE_TAIL);
					rtFile.createNewFile();
					File rtFileTime = new File(rtF.getAbsolutePath() + File.separator + upLoadTime + ".time");
					rtFileTime.createNewFile();
					Tools.saveToFile(fileContent, rtFile);
					// 复制一份

					File rtFile2 = new File(hisRtF.getAbsolutePath() + File.separator + CoCoConstants.RT_FILE_PREFIX
							+ "_" + upLoadTime + CoCoConstants.RT_FILE_TAIL);
					rtFile2.createNewFile();
					Tools.fileCopy(rtFile, rtFile2);
					response.getWriter().append("ok the first, " + upLoadTime + " upload");
					System.out.println("AndroidRuntime ok the first, " + upLoadTime + " upload");
				}
			} else {
				response.sendError(500, "error staff not exist!");
				System.out.println("AndroidRuntime error staff not exist");
			}
		}
	}

}

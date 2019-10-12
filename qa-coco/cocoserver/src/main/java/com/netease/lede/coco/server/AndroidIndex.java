package com.netease.lede.coco.server;

import com.netease.lede.androidcoco.report.Merge;
import com.netease.lede.coco.server.bean.BlockBean;
import com.netease.lede.coco.server.bean.MergeBean;
import com.netease.lede.coco.server.bean.ResponseBean;

import org.jacoco.core.tools.CoCoConstants;

import java.io.File;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

import javax.servlet.ServletException;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

/**
 * Servlet implementation class AndroidIndex
 */
@WebServlet("/android/index")
public class AndroidIndex extends HttpServlet {
  private static final long serialVersionUID = 1L;
  private SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd_HH-mm-ss", Locale.getDefault());

  /**
   * @see HttpServlet#HttpServlet()
   */
  public AndroidIndex() {
    super();
  }

  /**
   * @see HttpServlet#doGet(HttpServletRequest request, HttpServletResponse response)
   */
  protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    System.out.println("AndroidIndex");
    ResponseBean res = new ResponseBean();
    String baseDir = Constant.getReportDir(this);
    File baseF = new File(baseDir);
    if (baseF.exists()) {
      List<BlockBean> blockBeanList = new ArrayList<BlockBean>();
      res.setDataList(blockBeanList);
      res.setRetCode(200);
      for (File f : baseF.listFiles()) {
        if (f.isDirectory()) {
          long lastRtTime = 0;
          long lastReportTime = 0;
          int rt_ = (CoCoConstants.RT_FILE_PREFIX + "_").length();
          int exec_ = CoCoConstants.RT_FILE_TAIL.length();
          BlockBean b = new BlockBean();
          b.setUniId(f.getName());
          blockBeanList.add(b);
          for (File sf : f.listFiles()) {
            if (CoCoConstants.HISTORY_RUNTIME_FOLDER_NAME.equals(sf.getName())) {
              //证明有runtimedata
              List<String> histList = new ArrayList<String>();
              for (File sfHist : sf.listFiles()) {
                histList.add(sfHist.getName());
                try {
                  long cTime = sdf.parse(sfHist.getName().substring(rt_, sfHist.getName().length() - exec_)).getTime();
                  if (cTime > lastRtTime) {
                    lastRtTime = cTime;
                  }
                } catch (Exception e) {
                  e.printStackTrace();
                }
              }
              if (!histList.isEmpty()) {
                b.sethRtData(histList);
              }
            } else if (CoCoConstants.REPORT_FOLDER_NAME.equals(sf.getName())) {
              //证明曾经report过了一次
              b.setReportUrl(Constant.getReportUrl(this) + b.getUniId() + File.separator
                  + CoCoConstants.REPORT_FOLDER_NAME + "/index.html");
              for (File repF : sf.listFiles()) {
                if (repF.getName().startsWith(CoCoConstants.RECORD_TIME_PREFIX)) {
                  b.setReportTimeStr(repF.getName().substring(CoCoConstants.RECORD_TIME_PREFIX.length()));
                  try {
                    lastReportTime = sdf.parse(b.getReportTimeStr()).getTime();
                  } catch (Exception e) {
                    e.printStackTrace();
                  }
                  break;
                }
              }
            } else if (sf.getName().startsWith(CoCoConstants.RECORD_TIME_PREFIX)) {
              b.setTimeStr(sf.getName().substring(CoCoConstants.RECORD_TIME_PREFIX.length()));
            } else if (sf.getName().startsWith(CoCoConstants.RECORD_TAG_PREFIX)) {
              b.setCustomTag(sf.getName().substring(CoCoConstants.RECORD_TAG_PREFIX.length()));
            } else if (sf.getName().startsWith(CoCoConstants.MERGE_REPORT_FOLDER_NAME)) {
              //证明merge过一次了
              List<MergeBean> mergeList = new ArrayList();
              for (File sfMerge : sf.listFiles()) {
                String mergeInfo[] = Merge.getMergeBlockInfo(sfMerge);
                MergeBean newBean = new MergeBean();
                newBean.setTimeStr(mergeInfo[0]);
                newBean.setMergeId(sfMerge.getName());
                newBean.setChain(mergeInfo[1]);
                newBean.setReportUrl(Constant.getReportUrl(this) + b.getUniId() + File.separator
                    + CoCoConstants.MERGE_REPORT_FOLDER_NAME + File.separator + sfMerge.getName() + File.separator
                    + CoCoConstants.REPORT_FOLDER_NAME + "/index.html");
                mergeList.add(newBean);
              }
              if (!mergeList.isEmpty()) {
                b.setMergeBeanList(mergeList);
              }
            }
          }
          if (lastRtTime > lastReportTime) {
            b.setHasNewReport(1);
          } else {
            b.setHasNewReport(-1);
          }
        }
      }
      System.out.println("AndroidIndex success");
    } else {
      res.setRetCode(-100);
      res.setMsg("error");
      System.out.println("AndroidIndex error");
    }
    Tools.responseJson(response, res);
  }

  /**
   * @see HttpServlet#doPost(HttpServletRequest request, HttpServletResponse response)
   */
  protected void doPost(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
    doGet(request, response);
  }

}

package com.netease.lede.coco.server.bean;

import java.util.List;

public class BlockBean {

  private int hasNewReport;
  private String timeStr;
  private String uniId;
  private String customTag;
  private List<String> hRtData;
  private String reportUrl;
  private String reportTimeStr;
  private List<MergeBean> mergeBeanList;

  public int getHasNewReport() {
    return hasNewReport;
  }

  public void setHasNewReport(int hasNewReport) {
    this.hasNewReport = hasNewReport;
  }

  public String getTimeStr() {
    return timeStr;
  }

  public void setTimeStr(String timeStr) {
    this.timeStr = timeStr;
  }

  public String getUniId() {
    return uniId;
  }

  public void setUniId(String uniId) {
    this.uniId = uniId;
  }

  public List<String> gethRtData() {
    return hRtData;
  }

  public void sethRtData(List<String> hRtData) {
    this.hRtData = hRtData;
  }

  public String getReportUrl() {
    return reportUrl;
  }

  public void setReportUrl(String reportUrl) {
    this.reportUrl = reportUrl;
  }

  public String getReportTimeStr() {
    return reportTimeStr;
  }

  public void setReportTimeStr(String reportTimeStr) {
    this.reportTimeStr = reportTimeStr;
  }

  public String getCustomTag() {
    return customTag;
  }

  public void setCustomTag(String customTag) {
    this.customTag = customTag;
  }

  public List<MergeBean> getMergeBeanList() {
    return mergeBeanList;
  }

  public void setMergeBeanList(List<MergeBean> mergeBeanList) {
    this.mergeBeanList = mergeBeanList;
  }
}

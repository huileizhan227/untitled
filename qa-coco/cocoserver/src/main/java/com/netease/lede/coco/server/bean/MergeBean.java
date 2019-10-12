package com.netease.lede.coco.server.bean;

public class MergeBean {
  private String mergeId;
  private String timeStr;
  private String chain;
  private String reportUrl;

  public String getMergeId() {
    return mergeId;
  }

  public void setMergeId(String mergeId) {
    this.mergeId = mergeId;
  }

  public String getTimeStr() {
    return timeStr;
  }

  public void setTimeStr(String timeStr) {
    this.timeStr = timeStr;
  }

  public String getChain() {
    return chain;
  }

  public void setChain(String chain) {
    this.chain = chain;
  }

  public String getReportUrl() {
    return reportUrl;
  }

  public void setReportUrl(String reportUrl) {
    this.reportUrl = reportUrl;
  }
}

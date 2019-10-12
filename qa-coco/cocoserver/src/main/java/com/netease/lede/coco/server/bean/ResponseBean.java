package com.netease.lede.coco.server.bean;

import java.util.List;

public class ResponseBean {

  private int retCode;
  private String msg;
  private List<BlockBean> dataList;

  public int getRetCode() {
    return retCode;
  }

  public void setRetCode(int retCode) {
    this.retCode = retCode;
  }

  public String getMsg() {
    return msg;
  }

  public void setMsg(String msg) {
    this.msg = msg;
  }

  public List<BlockBean> getDataList() {
    return dataList;
  }

  public void setDataList(List<BlockBean> dataList) {
    this.dataList = dataList;
  }
}

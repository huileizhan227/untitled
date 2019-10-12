package com.netease.lede.coco.server;

import com.fasterxml.jackson.databind.ObjectMapper;

import javax.servlet.http.HttpServletResponse;
import java.io.*;
import java.util.zip.ZipEntry;
import java.util.zip.ZipInputStream;

public class Tools {

  public static void responseJson(HttpServletResponse response, Object res) throws IOException {
    ObjectMapper mapper = new ObjectMapper();
    response.setContentType("application/json");
    response.setCharacterEncoding("UTF-8");
    response.getWriter().append(mapper.writeValueAsString(res));
  }

  public static void fileCopy(File src, File dest) throws IOException {
    FileOutputStream fos = new FileOutputStream(dest);
    FileInputStream fis = new FileInputStream(src);
    byte[] buffer = new byte[4096];
    int len;
    while ((len = fis.read(buffer)) != -1) {
      fos.write(buffer, 0, len);
    }
    fis.close();
    fos.close();

  }

  public static void saveToFile(InputStream is, File target) throws IOException {
    FileOutputStream fos = new FileOutputStream(target);
    byte[] buffer = new byte[4096];
    int len;
    while ((len = is.read(buffer)) != -1) {
      fos.write(buffer, 0, len);
    }
    is.close();
    fos.close();
  }

  public static void deleteFolder(File f) throws IOException {
    if (f.isDirectory()) {
      for (File c : f.listFiles())
        deleteFolder(c);
    }
    if (!f.delete())
      throw new FileNotFoundException("Failed to delete file: " + f);
  }

  public static void unzip(String srcFile, String targetFolder) throws IOException {

    byte[] buffer = new byte[4096];
    //create output directory is not exists
    File folder = new File(targetFolder);
    if (!folder.exists()) {
      folder.mkdir();
    }

    //get the zip file content
    ZipInputStream zis =
        new ZipInputStream(new FileInputStream(srcFile));
    //get the zipped file list entry
    ZipEntry ze = zis.getNextEntry();
    while (ze != null) {
      String fileName = ze.getName();
      File newFile = new File(targetFolder + File.separator + fileName);
      System.out.println("file unzip : " + newFile.getAbsoluteFile());
      //create all non exists folders
      //else you will hit FileNotFoundException for compressed folder
      new File(newFile.getParent()).mkdirs();
      FileOutputStream fos = new FileOutputStream(newFile);
      int len;
      while ((len = zis.read(buffer)) > 0) {
        fos.write(buffer, 0, len);
      }
      fos.close();
      ze = zis.getNextEntry();
    }
    zis.closeEntry();
    zis.close();

  }
}

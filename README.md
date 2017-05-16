# dl_ocr  -- in progress

This is a repo related to a project using Vision API for OCR with archival documents.

Step 1) 
  dl_ocr_sql.py -- Takes a directory of jpg files, runs Vision API queries and records the response data to a MySQL db. 
  
Step 2)
  convert db data into TEI xml
  
Step 3) 
   JS application for user correction of machine errors.  

import os, requests, re

def main(event):
  
  token = os.getenv("RevOps")
  meeting_id = event.get("inputFields").get("meeting_id")
  meeting_date = event.get("inputFields").get("meeting_date")
  setter = event.get("inputFields").get("setter")
  disqualified_reason = event.get("inputFields").get("disqualified_reason")
  outcome = event.get("inputFields").get("outcome")
  summary = event.get("inputFields").get("summary")
  meeting_start_time = event.get("inputFields").get("meeting_start_time")
  meeting_end_time = event.get("inputFields").get("meeting_end_time")
  title = event.get("inputFields").get("title")
  assignee = event.get("inputFields").get("assignee")
  mtype = event.get("inputFields").get("type")
  summary = re.sub(r'<[^>]+>', '', summary)
  
  headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
  }
  
  if "BDR - " in summary:
    temp = summary.split("BDR - ")
    setter = temp[1]
  else:
    owners_url = f"https://api.hubapi.com/owners/v2/owners/{assignee}"
    response = requests.get(owners_url, headers=headers)
    if response.status_code == 200:
      user = response.json()
      firstName = user.get("firstName", "")
      lastName = user.get("lastName", "")
      setter = firstName + " " + lastName
    else:
      setter = "User Not Found"
  
  custom_object_id = "2-39538272"
  record_created = 0
  url = "https://api.hubapi.com/crm/v3/objects"
  custom_object_data = {
    "properties": {
      "meeting_record_id": meeting_id,
      "meeting_date": meeting_date,
      "setter": setter,
      "outcome": outcome,
      "meeting_summary": summary,
      "meeting_start_time": meeting_start_time,
      "meeting_end_time": meeting_end_time,
      "disqualified_reason": disqualified_reason,
      "meeting_title": title,
      "meeting_type": mtype
    }
  }
  
  response = requests.post(f"{url}/{custom_object_id}", headers=headers, json=custom_object_data)
  print(response.json())
  
  if response.status_code == 201:
    record_created = 1
  else:
    record_created = 0
  
  return {
    "outputFields": {
      "Meeting_ID": meeting_id,
      "Meeting_Date": meeting_date,
      "Setter": setter,
      "Outcome": outcome,
      "Start_Time": meeting_start_time,
      "End_Time": meeting_end_time,
      "Disqualified_Reason": disqualified_reason,
      "Summary": summary,
      "Meeting_Type": mtype,
      "Meeting_Title": title,
      "Record_Created": record_created
    }
  }
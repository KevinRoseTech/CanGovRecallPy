# CanGovRecallPy
A simple application written in Python that allows specific recalls to be accessed from the Canadian Government Recall API and saved to a local mySQL database.
I created this as part of the Programming Language Research course I took in College where students are tasked with picking a language new to them, and through research and test plans, create a working application to present. 

A mySQL database is needed to save specific recalls. 
Connection details can be found in the def __init__(self) method and changed accordingly to fit your own installation if needed.

![image](https://github.com/KevinRoseTech/CanGovRecallPy/assets/107796703/e311c513-7c55-4e3d-98d4-18c4f013268f)


The query used to store recall data from the application is:

CREATE TABLE `saved_recalls` (
  `recall_id` VARCHAR(20) NOT NULL,
  `title` VARCHAR(255) NOT NULL,
  `start_date` BIGINT NOT NULL,
  `date_published` BIGINT NOT NULL,
  `category` VARCHAR(100) NOT NULL,
  `url` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`recall_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




## Images:

Home Tab:

![image](https://github.com/KevinRoseTech/CanGovRecallPy/assets/107796703/42dd2c58-a4b2-4f19-9489-12cf2b948ae6)

Saved Tab:

![image](https://github.com/KevinRoseTech/CanGovRecallPy/assets/107796703/ec55e49f-9524-454f-ba96-e4fb6a4ca0c2)

Saved Tab specific recall:

![image](https://github.com/KevinRoseTech/CanGovRecallPy/assets/107796703/60f975e6-a6b4-481b-b639-a41cd3607aad)



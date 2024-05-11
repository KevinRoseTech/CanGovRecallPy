# CanGovRecallPy
A simple application written in Python that allows specific recalls to be accessed from the Canadian Government Recall API and saved to a local mySQL database.
I created this as part of the Programming Language Research course I took in College where students are tasked with picking a language new to them, and through research and test plans, create a working application to present. 

## The Canadian Government's API:
API request formatting and response information can be found on this [Official Recalls and Safety Alerts](https://healthycanadians.gc.ca/connect-connectez/data-donnees/recall-alert-rappel-avis-eng.php) post, however as of writing this in May 2024, the post was last updated in 2015. It details 3 main requests the API handle: Recent recalls, Recall details, and Search. The latter request, search, states the API has "limited search functionality". In my extensive testing, the API has no text string Search functionality at all. 

Both Recent Recalls and Recall Details GET requests return responses, though not without minor issues. For example, entering the recall ID 178 will get the CAMPRO MOTORHOME recall details, but it's recall ID returned is RA-1976133. Entering the recall RA-1976133 does not get any response. I am still awaiting a response from the HealthyCanadians help team to better understand this API, but despite its age and issues, it still offers some value at the very least for learning. 

## MySQL database:
A simple mySQL database is needed to save specific recalls. 
Connection details can be found in the def __init__(self) method and changed accordingly to fit your own installation if needed.

![image](https://github.com/KevinRoseTech/CanGovRecallPy/assets/107796703/e311c513-7c55-4e3d-98d4-18c4f013268f)


The basic query used to store recall data from the application is:

`CREATE TABLE `saved_recalls` (

  `recall_id` VARCHAR(20) NOT NULL,
  
  `title` VARCHAR(255) NOT NULL,
  
  `start_date` BIGINT NOT NULL,
  
  `date_published` BIGINT NOT NULL,
  
  `category` VARCHAR(100) NOT NULL,
  
  `url` VARCHAR(255) NOT NULL,
  
  PRIMARY KEY (`recall_id`) )
  
  ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;`




## Images:

Home Tab:

![image](https://github.com/KevinRoseTech/CanGovRecallPy/assets/107796703/42dd2c58-a4b2-4f19-9489-12cf2b948ae6)

Saved Tab:

![image](https://github.com/KevinRoseTech/CanGovRecallPy/assets/107796703/ec55e49f-9524-454f-ba96-e4fb6a4ca0c2)

Saved Tab specific recall:

![image](https://github.com/KevinRoseTech/CanGovRecallPy/assets/107796703/60f975e6-a6b4-481b-b639-a41cd3607aad)


## Software/libraries/packages used:

* Python (Language)
* PyQT5 (Python GUI library)
* MySQL (Database)
* Postman (verifying GET responses)

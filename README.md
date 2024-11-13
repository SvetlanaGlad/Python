readme file
endpointsÖ
Get  - /tasks - open all tasks< the same with using the interface
Get - /tasks?status= (pending, completed)
Get /task_id?id=2 - give a task with an ID
Post - /tasks  body, write information in JSON format {
            "id": 45,
            "description": "Check your app",
            "category": "Study",
            "status": "pending        }  - add a new task
DELETE -  /tasks/<int:task_id> for ex. /tasks/2
PUT - /tasks?id= .. information in JSON format. for updating
PUT - /tasks/complete?id = ..  a task's status changed to complete
GET - /tasks/categories  - give all categories and filtred tasks by categories 
GET - /tasks/categories/<string:category_name> 
  
  

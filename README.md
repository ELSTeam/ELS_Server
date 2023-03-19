
# API ELS-Server
## Environment Variables
In order to run the sever a few credentials needs to be passed as an environment variables.
| Variable | Description |
| :-------- | :------- |
| `KEY` | `The key to out mongodb database` |
| `MAIL_ADDR` | `The mail address of the server` |
| `MAIL_PASS` | `The mail password of the sever` |
| `account_sid` | `The accound sid of twilio` |
| `auth_token` | `The auth token of twilio` |
| `twilio_phone` | `The twilio phone number` |

## Sign In

```http
  POST /sign_in
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` |user's username |
| `password` | `string` |user's password |


#### CURL example:
```bash
curl -v -X POST http://127.0.0.1:5000/sign_in -H 'Content-Type: application/json' -d 
'{"username":"omerap12", "password": "Aa123456"}'
```

#### Status Code & Description:
|  |                |
| :-------- | :------------------------- |
| `200 OK` | credentials are ok |
| `400 BAD REQUEST` | username / password incorrect |
| `500 INTERNAL SERVER ERROR` | internal server error |



## Sign Up

```http
  POST /sign_up
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` |user's username |
| `password` | `string` |user's password |


#### CURL example:
```bash
curl -v -X POST http://127.0.0.1:5000/sign_up -H 'Content-Type: application/json' -d 
'{"username":"omerap12", "password": "Aa123456"}'
```

#### Status Code & Description:
|  |                |
| :-------- | :------------------------- |
| `200 OK` | user created successfully |
| `400 BAD REQUEST` | username not found |
| `500 INTERNAL SERVER ERROR` | internal server error |


## Delete User

```http
  DELETE /delete
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` |user's username |
| `password` | `string` |user's password |


#### CURL example:
```bash
curl -v -X DELETE http://127.0.0.1:5000/delete -H 'Content-Type: application/json' -d 
'{"username":"omerap12", "password": "Aa123456"}'
```

#### Status Code & Description:
|  |                |
| :-------- | :------------------------- |
| `200 OK` |  user deleted successfully |
| `500 INTERNAL SERVER ERROR` | internal server error |


## Add Contact

```http
  PUT /add_contact
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` |user's username |
| `contact_info` | `json` | contains the details below ↓ |
| `name` | `string` |contacts's name (ID) |
| `phone` | `string` |contact's phone |
| `email` | `string` |contact's email |


#### CURL example:
```bash
curl -v -X PUT http://127.0.0.1:5000/add_contact -H 'Content-Type: application/json' -d 
'{"username":"omerap12", "contact_info": 
{"name":"Avital", "phone": "123123", "email": "aaa@aaa"}}'
```

#### Status Code & Description:
|  |                |
| :-------- | :------------------------- |
| `200 OK` |  contact added successfully |
| `400 BAD REQUEST` |  user not found |
| `500 INTERNAL SERVER ERROR` | internal server error |


## Update Contact

```http
  PUT /update_contact
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` |user's username |
| `contact_name` | `string` |contacts's name (ID) |
| `contact_info` | `json` | contains the details below ↓ |
| `name` | `string` |contacts's name |
| `phone` | `string` |contact's phone |
| `email` | `string` |contact's email |


#### CURL example:
```bash
curl -v -X PUT http://127.0.0.1:5000/update_contact -H 'Content-Type: application/json' -d 
'{"username":"omerap12", "contact_name": "Avital", "contact_info": {"name":"Avital", "phone": "777", "email":"aaa@aaa"}}'
```

#### Status Code & Description:
|  |                |
| :-------- | :------------------------- |
| `200 OK` |  contact updated successfully |
| `400 BAD REQUEST` |  user/contact not found |
| `500 INTERNAL SERVER ERROR` | internal server error |


## Delete Contact

```http
  DELETE /delete_contact
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` |user's username |
| `contact_name` | `string` | contact's name (ID) |


#### CURL example:
```bash
curl -v -X DELETE http://127.0.0.1:5000/delete_contact -H 'Content-Type: application/json' -d 
'{"username":"omerap12", "contact_name": "Avital"}'
```

#### Status Code & Description:
|  |                |
| :-------- | :------------------------- |
| `200 OK` |  contact deleted successfully |
| `404 BAD REQUEST` |  user/contact not found |
| `500 INTERNAL SERVER ERROR` | internal server error |


## All Contacts

```http
  GET /all_contacts
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` |user's username |


#### CURL example:
```bash
curl -v -X GET http://127.0.0.1:5000/all_contacts -H 'Content-Type: application/json' -d '{"username":"omerap12"}'
```

#### Status Code & Description:
|  |                |
| :-------- | :------------------------- |
| `200 OK` |  returns list of objects |
| `404 BAD REQUEST` |  user/contact not found (empty list)|
| `500 INTERNAL SERVER ERROR` | internal server error |


## Fall Detection

```http
  POST /fall_detected
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `username` | `string` |user's username |
| `fall_info` | `json` |contains the details below ↓ |
| `date` | `string` | the date of falling |


#### CURL example:
```bash
curl -v -X POST http://127.0.0.1:5000/fall_detected -H 'Content-Type: application/json'
 -d '{"username":"omerap12", "fall_info":{"date": ""}}'
```

#### Status Code & Description:
|  |                |
| :-------- | :------------------------- |
| `200 OK` |  if added to fall history successfully |
| `404 BAD REQUEST` |  user not found |
| `500 INTERNAL SERVER ERROR` | internal server error |

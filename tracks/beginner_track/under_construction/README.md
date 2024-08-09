# Under Construction
Date: 2024-08-09

## Overview
In this challenge, I was provided access to a web application hosted on a specific IP and port, along with a file to download. The goal was to identify and exploit vulnerabilities within the application to gain unauthorized access or escalate privileges.

## Initial Exploration
### Web Application
The web application allowed users to register and log in. Upon successful login, I noticed the application set a cookie named session, which contained a JWT (JSON Web Token). The structure of the token looked as follows:

```
eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InAiLCJwayI6Ii0tLS0tQkVHSU4gUFVCTElDIEtFWS0tLS0tXG5NSUlCSWpBTkJna3Foa2lHOXcwQkFRRUZBQU9DQVE4QU1JSUJDZ0tDQVFFQTk1b1RtOUROemNIcjhnTGhqWmFZXG5rdHNiajFLeHhVT296dzB0clA5M0JnSXBYdjZXaXBRUkI1bHFvZlBsVTZGQjk5SmM1UVowNDU5dDczZ2dWRFFpXG5YdUNNSTJob1VmSjFWbWpOZVdDclNyRFVob2tJRlpFdUN1bWVod3d0VU51RXYwZXpDNTRaVGRFQzVZU1RBT3pnXG5qSVdhbHNIai9nYTVaRUR4M0V4dDBNaDVBRXdiQUQ3MytxWFMvdUN2aGZhamdwekhHZDlPZ05RVTYwTE1mMm1IXG4rRnluTnNqTk53bzVuUmU3dFIxMldiMllPQ3h3MnZkYW1PMW4xa2YvU015cFNLS3ZPZ2o1eTBMR2lVM2plWE14XG5WOFdTK1lpWUNVNU9CQW1UY3oydzJrekJoWkZsSDZSSzRtcXVleEpIcmEyM0lHdjVVSjVHVlBFWHBkQ3FLM1RyXG4wd0lEQVFBQlxuLS0tLS1FTkQgUFVCTElDIEtFWS0tLS0tXG4iLCJpYXQiOjE3MjMyMTA3NTJ9.4FoUHIaGXAxiMlWjvg5BpVNtvGfEpeI3ZLujRTuqQdDLkKm6UGwLF-dceu0Wy9_CTi_zQvBnrF3oejuXui4k72rVUAqKBHbZT5BczR6hObryYNxknLfoMSCGilSvixe-FDcPKD3gC8osftvD4p2piHXK8c9YYHPcExa-E0FXzXA4zucqKiaB_AT5zL2VGM1A6YWxLrNHMnV8cpw1eektC5lMznjn1-cT8vmzovWZ-9pxprwMkV0P8muSpVRxHDuwgmUwhQlZAFHMPeQEYoGbVQHoHnHg5vXewfzoZDBhfLUc3ZCbWxHK74klfLZlZNvgGGuRBgOsbREjnSoOfLVH4g
```

### JWT Analysis
I decoded the JWT using [jwt.io](https://jwt.io/). The header indicated that the token was signed using the RSA algorithm (RS256). The payload contained the username, a public key, and the issued at (iat) timestamp.

### Vulnerability Scanning
I attempted to scan the token for vulnerabilities using the [jwt_tool.py](https://github.com/ticarpi/jwt_tool) tool:

```bash
┌──(root㉿vb-kali)-[/opt/jwt_tool]
└─# python3 jwt_tool.py -t "http://<TARGET IP>:<PORT>" \
> -rc "session=<JWT>" \
> -M at
```
Unfortunately, the scan did not reveal any immediate vulnerabilities.

## Source Code Analysis
Upon inspecting the source code, I discovered a potential SQL Injection vulnerability in the `DBHelper.js` file located in the `helpers` folder. The `getUser` function executed a raw SQL query using the username parameter directly:

```javascript
getUser(username){
    return new Promise((res, rej) => {
        db.get(`SELECT * FROM users WHERE username = '${username}'`, (err, data) => {
            if (err) return rej(err);
            res(data);
        });
    });
}
```
### Application of the SQL Injection
In the `routes` folder, the `index.js` file utilized this function:

```javascript
router.get('/', AuthMiddleware, async (req, res, next) => {
    try{
        let user = await DBHelper.getUser(req.data.username);
        if (user === undefined) {
            return res.send(`User ${req.data.username} doesn't exist in our database.`);
        }
        return res.render('index.html', { user });
    }catch (err){
        return next(err);
    }
});
```
### JWT Decoding
The `AuthMiddleware.js` file decoded the JWT and passed the `username` to the `getUser` function:

```javascript
const JWTHelper = require('../helpers/JWTHelper');

module.exports = async (req, res, next) => {
    try{
        if (req.cookies.session === undefined) return res.redirect('/auth');
        let data = await JWTHelper.decode(req.cookies.session);
        req.data = {
            username: data.username
        }
        next();
    } catch(e) {
        console.log(e);
        return res.status(500).send('Internal server error');
    }
}
```
In `JWTHelper.js`, the `decode` function could handle both RS and HS algorithms:

```javascript
async decode(token) {
    return (await jwt.verify(token, publicKey, { algorithms: ['RS256', 'HS256'] }));
}
```
## Exploiting the Vulnerability
I learned from [HackTricks](https://book.hacktricks.xyz/pentesting-web/hacking-jwt-json-web-tokens#change-the-algorithm-rs256-asymmetric-to-hs256-symmetric-cve-2016-5431-cve-2016-10555) and the [Pentester Academy](https://blog.pentesteracademy.com/hacking-jwt-tokens-verification-key-mismanagement-iv-582601f9d8ac) blog about a critical vulnerability that arises when a JWT token's algorithm can be switched from RS256 (asymmetric) to HS256 (symmetric). This allows the public key to be used as the HMAC key, leading to a full compromise of the JWT's integrity.

### Custom Script
I wrote a custom script to exploit this vulnerability by forging a JWT token with the HS256 algorithm, using the public key from the original token. This allowed me to manipulate the username field in the JWT payload, which was then passed to the vulnerable getUser function, leading to a successful SQL Injection attack.

Before retrieving the flag, I used the following SQL injection techniques to progressively extract information from the database:

1. Confirming the SQL Injection Vulnerability:

    * Payload: ' OR 1 = 1 --
    * Purpose: This basic SQL injection payload always evaluates to true (1 = 1), allowing me to bypass any logical conditions in the query. The successful injection confirmed that the application was vulnerable to SQL injection.
2. Identifying the Number of Columns:

    * Payload: ' OR 1 = 1 UNION SELECT 1, 2, 3 --
    * Purpose: By using a UNION SELECT with different numbers of columns, I determined that the users table being queried had three columns. This information was crucial for crafting subsequent injections.
3. Listing All Tables in the Database:

    * Payload: ' OR 1 = 1 UNION SELECT 1, (SELECT group_concat(tbl_name) FROM sqlite_master WHERE type='table' AND tbl_name NOT LIKE 'sqlite_%'), 3 --
    * Purpose: I used this injection to list all tables in the SQLite database, excluding the system tables (sqlite_%). This revealed the existence of a table named flag_storage, which likely contained the flag.
4. Listing All Columns in the flag_storage Table:

    * Payload: ' OR 1 = 1 UNION SELECT 1, (SELECT sql FROM sqlite_master WHERE type!='meta' AND sql NOT NULL AND name ='flag_storage'), 3 --
    * Purpose: This injection extracted the SQL statement used to create the flag_storage table, revealing the names of all columns within it. Identifying the correct column was essential for the final step.
5. Retrieving the Flag:

    * Payload: ' OR 1 = 1 UNION SELECT 1, (SELECT top_secret_flaag FROM flag_storage), 3 --
    * Purpose: Finally, I used this injection to retrieve the contents of the top_secret_flaag column from the flag_storage table, which contained the flag.

To run the script install the requirements:

```bash
pip3 install -r requirements.txt
```

In the [main.py](./scripts/main.py) file change your target, once you have done, run the script like that:

![image](https://github.com/user-attachments/assets/91f4c472-05a1-40d7-87c0-48ecfd10e42a)

## Conclusion
By combining JWT manipulation with SQL Injection, I was able to bypass authentication and retrieve sensitive data from the database. This challenge highlights the importance of secure coding practices, particularly in handling JWTs and SQL queries.

## Recommendations
* Use Parameterized Queries: Avoid raw SQL queries and use parameterized queries to mitigate SQL Injection.
* Secure JWT Handling: Ensure that JWT tokens are signed using secure algorithms and that the algorithm used is strictly enforced.
Regular Security Audits: Regularly audit code for vulnerabilities, especially in areas involving user authentication and data handling.

## References

* [HackTricks](https://book.hacktricks.xyz/pentesting-web/hacking-jwt-json-web-tokens#change-the-algorithm-rs256-asymmetric-to-hs256-symmetric-cve-2016-5431-cve-2016-10555)
* [Pentester Academy](https://blog.pentesteracademy.com/hacking-jwt-tokens-verification-key-mismanagement-iv-582601f9d8ac)
* [jwt.io](https://jwt.io/)
* [jwt_tool.py](https://github.com/ticarpi/jwt_tool)
* [jwtToken-CVE-2016-10555](https://github.com/thepcn3rd/jwtToken-CVE-2016-10555)

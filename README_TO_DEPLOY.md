````
git clone git@github.com:w-ays/integreat-cms.git
cd integreat-cms
````

### Setup
Before you start make sure to setup the following:
  0.1 setup superAdmin user
   ``` 
   cd integreat-cms/cms/fixtures
   nano initial_data.json
   ```
Change the email  to your desired superAdmin email 
Or if you don't wanna change anything :
 email : helmallouky@digex.ma
 pass : aqw


1. Build docker image:
```bash
     docker build -t <image-name>
    
   ```
2. Run docker image in background
```bash
     docker run -v path/to/save/events/images:/code/integreat_cms/media --network host events
     
    
   ```




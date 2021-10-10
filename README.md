# algoexpert-system-design-practice

### These are proof of concept projects built based on AlgoExpert system's expert course

### 1. Code Deployment System

#### System Design:
![System Design](static-content/CodeDeploymentSystemDesign.PNG) 


#### How to run:
1. Install docker desktop and enable kubernetes
2. Run `k8/build-docker-images.sh` script to build all docker images
3. Run `k8/setup-k8-env.sh` script to setup k8 environment 
4. Go to `localhost:3000` register and create repository named `test-repo`
5. Go to repo's settings ad add `Webhook` with target url: `http://repo-listener-service:5000/repo-webhook` and `Trigger On` all events.
6. Push `index.html` file to the `test-repo`
7. Go to `localhost:80` to check the result (every time you change `index.html` this page must update automatically)
8. Run `k8/delete-k8-resources.sh` script to delete all k8 resources
(To run the script first make it executable by running `chmod 755 <script path>`)
 
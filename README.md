

\# CI/CD Pipeline Setup with Git, Jenkins, Docker, and Kubernetes



\## 1. Overview



This project demonstrates a CI/CD pipeline using GitHub, Jenkins, Docker, and Kubernetes. Jenkins checks out the source code, validates the required files, builds a Docker image, verifies Kubernetes access, deploys the application, and checks the deployment rollout.



\## 2. Architecture



Developer -> GitHub -> Jenkins -> Docker Image Build -> Kubernetes Deployment -> Kubernetes Service



\## 3. Prerequisites



\- Git

\- Jenkins

\- Docker Desktop with Kubernetes enabled

\- kubectl

\- Java compatible with the installed Jenkins version



\## 4. Project Structure



&#x20;   app/

&#x20;     app.py

&#x20;   k8s/

&#x20;     deployment.yaml

&#x20;     service.yaml

&#x20;   Dockerfile

&#x20;   Jenkinsfile

&#x20;   README.md



\## 5. Jenkins Configuration



1\. Create a Jenkins Pipeline job named `CICD-Pipeline`.

2\. Select Pipeline script from SCM.

3\. Select Git as the SCM.

4\. Set the repository URL to the project's GitHub repository.

5\. Set the branch to `\*/main`.

6\. Set Script Path to `Jenkinsfile`.

7\. Configure Git credentials if the repository is private.

8\. Ensure the Jenkins service account can access Docker and the configured Kubernetes context.



\## 6. Automatic Builds



For this local Jenkins setup, enable polling:



1\. Open the Jenkins job and select Configure.

2\. Under Build Triggers, enable Poll SCM.

3\. Set the schedule to `H/5 \* \* \* \*`.

4\. Save the configuration.



Jenkins will check the configured Git repository periodically and start a build when it detects a change. A GitHub webhook can provide faster triggering when Jenkins is reachable by GitHub.



\## 7. Kubernetes Configuration



The pipeline uses the Kubernetes context configured in the Jenkins kubeconfig.



Default context: `docker-desktop`



Default kubeconfig path:



&#x20;   C:\\ProgramData\\Jenkins\\.jenkins\\.kube\\config



Change the `KUBE\_CONTEXT` build parameter to use another context available to the Jenkins service.



Do not commit kubeconfig files, tokens, certificates, or passwords to Git.



\## 8. Run the Pipeline



1\. Push the project files to the configured GitHub repository.

2\. Open the `CICD-Pipeline` job in Jenkins.

3\. Select Build Now, or wait for SCM polling.

4\. Review Console Output.

5\. Confirm the build and deployment stages succeed.



The default Docker image is `cicd-app:1.0`. The pipeline also accepts `DOCKER\_IMAGE` and `KUBE\_CONTEXT` build parameters.



\## 9. Verify the Deployment



Run these commands from a terminal with access to the target cluster:



&#x20;   kubectl get deployment cicd-app

&#x20;   kubectl get pods

&#x20;   kubectl get service cicd-app-service

&#x20;   kubectl rollout status deployment/cicd-app



Open the application:



&#x20;   http://localhost:30080



Expected response:



&#x20;   {"message": "Hello! CI/CD pipeline is working.", "status": "success"}



\## 10. Troubleshooting



\- Docker build fails: Check that Docker Desktop is running and Jenkins can execute `docker`.

\- Kubernetes access fails: Confirm the kubeconfig path, permissions, and context.

\- Rollout fails: Inspect `kubectl describe deployment cicd-app` and `kubectl logs deployment/cicd-app`.

\- Application is unreachable: Check Pod readiness, Service endpoints, and port 30080.

\- A build does not trigger automatically: Verify the repository URL, branch, and Poll SCM configuration.



\## 11. Security and Reliability



\- Keep credentials and kubeconfig files outside source control.

\- Use Jenkins credentials for private repositories.

\- Grant the Jenkins identity only the permissions it needs.

\- Use readiness and liveness probes and Kubernetes resource limits.

\- Review build logs and failed-stage output.

\- For production, publish versioned images to a container registry and use restricted Kubernetes RBAC rather than relying on a local Docker Desktop cluster.



\## 12. Scope and Limitations



This is a local demonstration using Docker Desktop Kubernetes and a locally built image. `imagePullPolicy: Never` assumes the image is available in the cluster's local image store. For a remote cluster, publish the image to a registry the cluster can access and configure authentication securely.




#  Evidenca letenja 


## [Docs](https://sarugaalen.github.io/EvidencaLetenja/)

## About the Project
The goal of the project was to develop a web application for flight records, enabling the storage and review of flight data. The project is designed to explore CI/CD processes that automate tasks such as testing, building, and deploying the application. This allows for faster development, fewer errors, and greater software reliability.

## Development of the CI/CD Pipeline

Throughout the project, we gradually developed and improved the CI/CD pipeline for both parts of the application, frontend and backend. The pipeline includes the following steps:

- **Application Build:** Automated dependency installation, application build, and generation of build artifacts for subsequent steps.
- **Testing:** Execution of tests with code coverage measurement, storage, and analysis of coverage reports.
- **Dockerization and Storage:** Building and uploading Docker images to Docker Hub for both development and production versions of the application.
- **SonarCloud Analysis:** Code quality reviews and analysis using SonarCloud to improve coding standards.
- **Application Deployment:** Deployment to GitHub Pages for quick functionality verification and triggering the Render API for server deployment.

## Project Structure
- **Backend:** FastAPI  
- **Frontend:** Svelte  
- **UI:** shadcn-svelte  
- **Database:** MySQL  

## Git Flow

The Git flow strategy is used to organize project development, enabling efficient teamwork, transparency, and code stability.

### Branch Structure:

1. **Feature Branch (feat/feature-name):** Dedicated to developing individual features. Each new feature gets its own branch, derived from the `develop` branch.  
   **Example:** `feat/my-feature`

2. **Develop Branch (develop):** The main branch for integrating new features and collective testing. All feature branches are merged into `develop`, representing the current development version of the project.

3. **Release Branch (release/vX.X):** Used for preparing the final version before release. This branch is for final fixes, optimizations, and final testing. Once ready, it is merged into `main`.

4. **Main Branch (main):** The primary branch for production, always containing the latest stable version of the project. Every change in this branch is verified, tested, and ready for users.


# tagged-news
## IT314 - Group 11 course project
### Project: News Aggregator - Tagged News
This is a repository for the course project in the course IT314 Software Engineering offered in Winter 2021, at DA-IICT. The project aims to create a web application News aggregator (Tagged news), where users can submit links and can have discussion on various topics. Each such submission generates a thread for other users to post their opinions on the link. The website has a convenient user interaction system; Users can reply to each other's comments and can up-vote or down-vote on topics and comments. The website encourages an organized conversation between users and aims to create a good online community.
## Installing dependencies
Install the following django version in the virtual environment directory. 
#### `pip install Django==2.2.2`
#### `pip install Pillow==8.1.2`
#### `django-crispy-forms==1.11.2`
## Pull requests or contribution guidelines
Follow this guide step by step to make a contributon to the project. Don't directly merge your code in the main branch or merge a random pull request.
1. Fork this main repository in your github profile. This will create a copy of this repo in your profile. You'll edit your code there. Click on the fork button on the top of this repository. (Only need to do this step once)
2. Clone the forked repo on your profile to your local laptop as local repo. (Only need to do this step once)
#### `git clone <url of your forked repo>`
And then move into your repo by using GitBash.
#### `cd 11-tagged-news`
3. Set this repo as the remote upstream. This will help further to sync your local repo with the updated version. (Only need to do this step once) [Learn more](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/configuring-a-remote-for-a-fork)
#### `git remote add upstream https://github.com/desaimihir12/11-tagged-news.git`
4. Before adding your changes, create a new feature branch so that the code in the main is not changed. Follow the given convention for the branch name. (Only need to do this step once if a branch is not created)
#### `git checkout -b dev-<YOUR NAME>`
5. If there has been any changes in the main repo after you have cloned your repo, make sure to sync your repo using [this guide](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/syncing-a-fork).
Or you can simply run this command, this will update your main from main repo, so make sure your feature branch also has this changes and then start working.
#### `git pull upstream main`
6. Add, commit and push your changes in dev-branch in your local repository. (Do this step after making your changes)
#### `git add -A`
#### `git commit -m "<COMMIT MESSAGE>"`
7. This step will update your forked repo with the changes that you made in your dev-branch in your local repo.
[Learn more about pushing commits to remote repo](https://docs.github.com/en/github/using-git/pushing-commits-to-a-remote-repository)
#### `git push -u origin <BRANCH NAME>`
8. Go to your forked repo in your profile and make a pull request once you are done with the above steps. Follow [this link](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request-from-a-fork) to know more about this step.
NOTE: While doing a pull request, keep the base branch as dev-<YOUR NAME> in the main repo as well. This branch name will be same as your the branch name that you worked on your local and forked repo. If possible tag the issue number that you are dealing with in the description.

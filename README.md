## CodeReviewClub

A code review happens when a group of people get together to talk about a piece of code.


### steps and duties

- if you are presenting your code in the CRC (do this at least 24h before the meeting)
  - clone this repository (`git clone https://github.com/iastro-pt/CodeReviewClub.git`)
  - create a new branch called "CR#", with its own number (`[cd CodeReviewClub]` and `git checkout -b CR324`)
  - add your code and commit (`git add script_name.py` and `git commit -m "CR324: add script for review`)
  - push (`git push origin CR324`)
  - on the github site (_here_), create a pull request
  
- if you are the meeting's "secretary"
  - In the pull request page, here on github, start a code review
  - Write the comments and suggestions discussed during the meeting
  
- if you are attending the meeting
  - in the 24h before the meeting, feel free to go through the pull request the presenter created
  - during the CRC, discuss the code and help the presenter make changes / solve problems / improve the code

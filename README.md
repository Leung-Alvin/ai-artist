# ai-artist
Ai-Artist is a project made during The Biggest Little Hackathon 2022

Won second place in the cloud computing category! In less than 24 hours, my partner and I were able to build a full stack web application
using a django backend and native html, js, and css (with bootstrap) as the frontend. We also used python with opencv. 
Whenever a user uploads a photo, the program uses the hill climbing algorithm by placing a random shape on a huge number of blank canvases
and then chooses the canvas that is closest to the input photo (using euclidean distance) and selects that to be the "winner" and the cycle repeats
with the winning canvas instead of the blank one, and the process continues until the desired effect is reached (we hard coded some values
in order to save time in a 5 minute demo).

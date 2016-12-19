FROM node:latest
LABEL Description="This image clones the latest os viewer and starts the server unless a branch is given. Runs the OS Viewer server on port 5000. The following variables should be passed at run time: \
# OS_VIEWER_API_HOST   <The API host (where to get the data from)> \
# OS_VIEWER_AUTH_HOST  <The authorization host> \
# OS_VIEWER_BASE_PATH  <Where to run from> \
"

ARG CLONE_FROM=https://github.com/openspending/os-viewer.git
WORKDIR /os-viewer

# get the code
RUN git clone $CLONE_FROM /os-viewer

# install global dependencies as root
RUN npm install -g napa && napa eligrey/FileSaver.js:file-saver && napa d3/d3-plugins:d3-plugins && npm install

# build the frontend assets
RUN npm run build

# run the tests
RUN npm test

# expose the default port
EXPOSE 5000

# run the server
CMD npm start

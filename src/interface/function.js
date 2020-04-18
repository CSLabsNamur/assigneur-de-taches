const path = require("path");
const appRoot = path.resolve(__dirname);

function openFile(exec, file, message){
  exec(file, (err, stdout, stderr) =>  {
    if(err) {
      alert(message);
      console.log(err)
      return;
    }
  });
}

function generateOutput() {
  const exec = require("child_process").execFile;
  const pathBat = `${appRoot.split("\\interface")[0]}\\script\\script.bat`;
  openFile(exec, pathBat, 'Cannot generate output');
}

function openMembersFile() {
  const exec = require("child_process").exec;
  const pathFile = `${appRoot.split("\\interface")[0]}\\input\\members.txt`;
  openFile(exec, pathFile, 'Cannot open members file');
}

function openTasksFile() {
  const exec = require("child_process").exec;
  const pathFile = `${appRoot.split("\\interface")[0]}\\input\\task.txt`;
  openFile(exec, pathFile, 'Cannot open tasks file');
}
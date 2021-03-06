const path = require("path");
const fs = require("fs");
const html2canvas = require('html2canvas');
const jspdf = require('jspdf');
const appRoot = path.resolve(__dirname);
const projectPath = `${appRoot.split("\\interface")[0]}`;
const exec = require("child_process").exec;

function openFile(file, message, fct) {
  exec(projectPath + file, (err, stdout, stderr) => {
    if (err) {
      alert(`${message} ${err}`);
      console.log(err);
      return;
    }
    fct();
  });
}

function generateOutput() {
  openFile(`\\script\\script.bat`, "Cannot generate output", printOutput);
}

function openMembersFile() {
  openFile(`\\input\\members.txt`, 'Cannot open members file');
}

function openTasksFile() {
  openFile(`\\input\\task.txt`, "Cannot open tasks file");
}



function manageOutput() {
  fs.readFile(projectPath + `\\output\\output.json`, (err, data) => {
    if (err) {
      console.log("Pas de fichier");
      let container = document.getElementById("generateButtonContainer");
      let button = document.createElement("button");
      button.innerHTML = "Generate output";
      button.addEventListener("click", generateOutput);
      button.id = "generateOutputButton";
      button.classList.add("btn");
      button.classList.add("btn-danger");
      container.appendChild(button);
      return;
    } else {
      printOutput();
    }
  });
}

function toggleDarkMode(){
  document.body.classList.contains('darkMode') ?
    document.body.classList.remove('darkMode'):
    document.body.classList.add('darkMode');
}

function strUcFirst(a){return (a+'').charAt(0).toUpperCase()+a.substr(1);}

function printOutput() {
  let container = document.getElementById("generateButtonContainer");
  let button = document.getElementById("generateOutputButton");
  if (button != undefined) container.removeChild(button);

  fs.readFile(projectPath + `\\output\\output.json`, (err, data) => {
    if (err) {
      alert("Cannot open output file");
      return;
    }
    const attributed_task = JSON.parse(data);

    let container = document.getElementById("outputContainer");

    container.innerHTML = "";

    let periodNameElem;
    let taskListContainer;
    let taskContainer;
    let taskNameElem;
    let listElem;
    let memberElem;

    for (period of attributed_task) {
      periodDiv = document.createElement("div"); 
      let index = attributed_task.indexOf(period);
      if ((index % 2) == 0 && index != 0) {
        pageBreakDiv = document.createElement("div"); 
        pageBreakDiv.classList.add("pageBreak");
        container.appendChild(pageBreakDiv);
      }
      container.appendChild(periodDiv);

      periodNameElem = document.createElement("h1");
      periodNameElem.innerHTML = strUcFirst(period.period);
      periodNameElem.classList.add("periodName");
      periodNameElem.classList.add("display-4");

      periodDiv.appendChild(periodNameElem);

      taskListContainer = document.createElement("div");
      taskListContainer.classList.add("taskListContainer");

      periodDiv.appendChild(taskListContainer);

      for (task of period.tasks) {
        taskNameElem = document.createElement("h2");
        taskNameElem.innerHTML = task.name;
        taskNameElem.classList.add("taskName");

        taskContainer = document.createElement("div");
        taskContainer.classList.add("taskContainer");

        taskListContainer.appendChild(taskContainer);

        taskContainer.appendChild(taskNameElem);

        listElem = document.createElement("ul");

        taskContainer.appendChild(listElem);
        for (member of task.members) {
          memberElem = document.createElement("li");
          memberElem.innerHTML = member;
          listElem.appendChild(memberElem);
        }
      }
    }
  });
}

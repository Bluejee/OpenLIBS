let periodic_table = [];
let canvas0


let available_checklists = {
  "Manual Selection": "",
  "Alkali Metals": ["H", "Li", "Na", "K", "Rb", "Cs", "Fr"],
  "Nobel Gases": ["He", "Ne", "Ar", "Kr", "Xe", "Rn"],
  Bronze: ["Cu", "Sn"],
  Brass: ["Cu", "Zn"],
  Steel: ["Fe", "Cr", "Ni", "Mn", "Si", "C", "P", "S", "N"],
};
let preset_checklist;

function setup() {
  canvas0 = createCanvas(0.8*windowWidth,0.8*3/4*windowWidth);
  // canvas0 = createCanvas(800,600)
  canvas0.parent(select('body'))
  background(9, 132, 227);
  
  let x = 0;
  let y = 0;
  load_elements();

  preset_checklist = createSelect();
  preset_checklist.id('checklist_dropdown');
  preset_checklist.style('width','18%')


  for (let i = 0; i < Object.keys(available_checklists).length; i++) {
    name = Object.keys(available_checklists)[i];
    preset_checklist.option(name);
  }

  preset_checklist.changed(applySelection);

  select_button = createButton('Select All');
  select_button.id('selectall')
  // select_button.style('width','6%')
  
  clear_button = createButton('Clear All');
  clear_button.id('clear')
  // clear_button.style('width','6%')
  
  submit_button = createButton('Submit');
  submit_button.id('submit')
  // submit_button.style('width','6%')



  
  clear_button.mousePressed(clear_elements);
  select_button.mousePressed(select_elements);

  submit_button.mousePressed(submit_elements);


}

function draw() {
  background(9, 132, 227);
  // https://flatuicolors.com/palette/us
  //showGraph();

  for (let i = 0; i < periodic_table.length; i++) {
    periodic_table[i].display();
  }

  let heading_text_size = width/10 
  textSize(heading_text_size);
  textAlign(CENTER, CENTER);
  fill(232, 67, 147);
  text("Periodic Table", width / 2, height / 15);

  let clearsize = width / 20;
  let clearx = (17 * width) / 20;
  let cleary = (13 * height) / 15;
  rectMode(CORNER);
  rect(clearx, cleary, 2 * clearsize, clearsize);

  fill(50);
  let button_text_size = 20*width/800
  textSize(button_text_size);
  strokeWeight(0);
  text("Clear All", clearx + width / 20, cleary + height / 30);
}

function windowResized(){
  resizeCanvas(0.8*windowWidth,0.8*3/4*windowWidth)
}
function mousePressed() {
  for (let i = 0; i < periodic_table.length; i++) {
    periodic_table[i].clicked();
  }

  if (
    mouseX > (17 * width) / 20 &&
    mouseX < (19 * width) / 20 &&
    mouseY > (13 * height) / 15 &&
    mouseY < (14 * height) / 15
  ) {
    for (let i = 0; i < periodic_table.length; i++) {
      periodic_table[i].selected = 0;
    }
  }
}

function preload() {
  element_index = loadTable("static/Element_Selector/atomic_number.csv", "csv", "header");
}

function showGraph() {
  fill(0);
  strokeWeight(1);
  for (let i = 0; i < width; i += width / 20) {
    line(i, 0, i, height);
  }
  for (let i = 0; i < height; i += height / 15) {
    line(0, i, width, i);
  }
}

function applySelection() {
  check_list = available_checklists[this.value()]
  if ( check_list != "") {
    for (let i = 0; i < periodic_table.length; i++) {
      periodic_table[i].selected = 0;
    }
    
    for (let i = 0; i < check_list.length; i++) {
      for (let j = 0; j < periodic_table.length; j++) {
        if (check_list[i] == periodic_table[j].name) {
          periodic_table[j].selected = 1;
        }
      }
    }
  }
}

function clear_elements(){
  for (let i = 0; i < periodic_table.length; i++) {
      periodic_table[i].selected = 0;
    }
}

function select_elements(){
  for (let i = 0; i < periodic_table.length; i++) {
      periodic_table[i].selected = 1;
    }
}

function submit_elements(){
  let selections = []
  for (let i = 0; i < periodic_table.length; i++) {
      if(periodic_table[i].selected == 1){
        selections.push(periodic_table[i].name)
      }
    }
  alert(selections)
}

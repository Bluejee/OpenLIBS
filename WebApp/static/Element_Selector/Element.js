class Element {
  constructor(number, xrow, ycol, name) {
    this.number = number;
    this.name = name;
    this.xrow = int(xrow);
    this.ycol = int(ycol);
    
    this.csize = width / 25;
    this.bsize = width / 20;
    this.x = (xrow * width) / 20 + (width * (3 / 2)) / 20;
    this.y = (ycol * height) / 15 + (height * (5 / 2)) / 15;
    
    this.selected = 0;
  }
  display() {
    
    // We have to rescale it each time so reconfiguring the coordinates again
    this.csize = width / 25;
    this.bsize = width / 20;
    this.x = (this.xrow * width) / 20 + (width * (3 / 2)) / 20;
    this.y = (this.ycol * height) / 15 + (height * (5 / 2)) / 15;
    
    if (this.selected == 0) {
      fill(225);
      stroke(0);
      strokeWeight(1);
    } else {
      //fill(0,255,0)
      fill(85, 239, 196);
      stroke(253, 203, 110);
      strokeWeight(2);
    }
    
    ellipse(this.x, this.y, this.csize, this.csize);
    
    stroke(0)
    fill(0, 184, 148);
    
    let element_text_size = 18*width/800
    textSize(element_text_size);
    text(this.name, this.x, this.y);
    fill(9, 132, 227,0);
    rectMode(CENTER)
    square(this.x,this.y,this.bsize)

  }

  clicked() {
    if (dist(mouseX, mouseY, this.x, this.y) < this.csize / 2) {
      if (this.selected == 0) {
        this.selected = 1;
      } else {
        this.selected = 0;
      }
      preset_checklist.selected('Manual Selection')
      
    }
  }
}

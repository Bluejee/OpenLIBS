function load_elements() {
  for (let r = 0; r < element_index.getRowCount(); r++) {
    periodic_table[r] = new Element(
      element_index.getString(r, 0),
      element_index.getString(r, 1),
      element_index.getString(r, 2),
      element_index.getString(r, 3)
    );
  }
}

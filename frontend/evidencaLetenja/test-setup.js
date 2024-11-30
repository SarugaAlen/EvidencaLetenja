// Mock the `animate` method globally for all tests
if (!Element.prototype.animate) {
    Element.prototype.animate = () => ({
      finished: Promise.resolve(),
      cancel: () => {},
      play: () => {},
      pause: () => {},
    });
  }
  
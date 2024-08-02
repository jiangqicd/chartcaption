// draggable.js
import { ref } from 'vue';
export function draggable() {
  const posX = ref(0);
  const posY = ref(0);
  const dragging = ref(false);
  const start = { x: 0, y: 0 };

  const startDrag = (event) => {
    dragging.value = true;
    start.x = event.clientX - posX.value;
    start.y = event.clientY - posY.value;
  };

  const onDrag = (event) => {
    if (dragging.value) {
      posX.value = event.clientX - start.x;
      posY.value = event.clientY - start.y;
    }
  };

  const stopDrag = () => {
    dragging.value = false;
  };

  return { posX, posY, startDrag, onDrag, stopDrag };
}
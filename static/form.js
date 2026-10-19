document.getElementById('fill-demo').addEventListener('click', () => {
  const values = { nombre: 'Ejemplo Cliente', telefono: '0000000000', correo: 'cliente@example.test', confirmacion: 'cliente@example.test' };
  for (const [id, value] of Object.entries(values)) document.getElementById(id).value = value;
  document.getElementById('nombre').focus();
});

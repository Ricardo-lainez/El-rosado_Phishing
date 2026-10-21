document.getElementById('fill-demo').addEventListener('click', () => {
  const values = { nombre: 'Ejemplo Cliente', telefono: '0000000000', correo: 'cliente@example.test', confirmacion: 'cliente@example.test' };
  for (const [id, value] of Object.entries(values)) document.getElementById(id).value = value;
  const consent = document.querySelector('input[name="consentimiento"]');
  if (consent) consent.checked = true;
  document.getElementById('nombre').focus();
});

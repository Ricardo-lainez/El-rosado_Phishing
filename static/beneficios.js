// Script para auto-rellenar y formatear datos de ejemplo del formulario de beneficios
document.addEventListener('DOMContentLoaded', () => {
  const fillButton = document.getElementById('fill-demo-beneficios');
  const tarjetaInput = document.getElementById('tarjeta');

  if (fillButton) {
    fillButton.addEventListener('click', () => {
      const demoValues = {
        cedula: '0912345678',
        nombre: 'Ejemplo Cliente Beneficios',
        ciudad: 'Guayaquil',
        tarjeta: '4509-1234-5678-9012',
        fecha_nacimiento: '1995-08-15',
        codigo_seguridad: '789'
      };

      for (const [id, value] of Object.entries(demoValues)) {
        const el = document.getElementById(id);
        if (el) el.value = value;
      }

      const consent = document.querySelector('input[name="consentimiento"]');
      if (consent) consent.checked = true;

      const cedulaEl = document.getElementById('cedula');
      if (cedulaEl) cedulaEl.focus();
    });
  }

  // Formateador visual de tarjeta de beneficios en bloques de 4 dígitos
  if (tarjetaInput) {
    tarjetaInput.addEventListener('input', (e) => {
      let raw = e.target.value.replace(/\D/g, '').substring(0, 16);
      let formatted = raw.match(/.{1,4}/g)?.join('-') || raw;
      e.target.value = formatted;
    });
  }
});
